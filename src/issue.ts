import { Octokit } from "@octokit/rest";
import { env } from "node:process";

const owner = "microsoft";
const repo = "winget-pkgs";
const bot_login = "coolplaylinbot";
const owner_login = "CoolPlayLin";

const main = async () => {
  const api = new Octokit({
    auth: env.GITHUB_TOKEN,
  });
  let i = 0;
  const datas = [];
  while (true) {
    i += 1;
    let searchedContent = (
      await api.rest.search.issuesAndPullRequests({
        q: `user:${owner} repo:${repo} author:${bot_login} state:open is:pr`,
        per_page: 100,
        page: i,
      })
    ).data.items;
    if (searchedContent.length == 0) break;
    datas.push(searchedContent);
  }
  datas.forEach((data) => {
    data.forEach(async (obj) => {
      const labels = (
        await api.rest.issues.listLabelsOnIssue({
          repo: repo,
          owner: owner,
          issue_number: obj.number,
        })
      ).data.map((label) => label.name);
      if (labels.includes("No-Recent-Activity")) {
        await api.rest.issues.createComment({
          owner: owner,
          repo: repo,
          issue_number: obj.number,
          body: `Don't close this Pull Request please :)\nCC @CoolPlayLin`,
        });
        console.log(`Prevent #${obj.issue_number} from being stale`);
      }
      const comments = await api.rest.issues.listComments({
        repo: repo,
        owner: owner,
        issue_number: obj.number,
      });
      comments.data.forEach(async (comment) => {
        if (comment.user.login !== owner_login) {
          return;
        }
        const { body } = comment;
        if (body.match(/@[Cc]ool[Pp]lay[Ll]in[Bb]ot [Cc]lose/)) {
          console.log(`Close #${obj.number}`);
          await api.rest.issues.createComment({
            owner: owner,
            repo: repo,
            issue_number: obj.number,
            body: `I've received my owner's request to close this pr, I'll close it right now`,
          });
          await api.rest.pulls.update({
            owner: owner,
            repo: repo,
            pull_number: obj.number,
            state: "closed",
          });
        }
      });
    });
  });
};

main().catch((error) => {
  console.log(error);
});
