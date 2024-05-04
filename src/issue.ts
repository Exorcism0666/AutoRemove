import { Octokit } from "@octokit/rest";
import { env } from "node:process";

const owner = "microsoft";
const repo = "winget-pkgs";
const bot_login = "coolplaylinbot";
const owner_login = "CoolPlayLin";

async function getAllPullRequests(api: Octokit, owner: string, repo: string) {
  let datas = [];
  let total = 0;
  let i = 0;
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
    total += searchedContent.length;
    datas.push(searchedContent);
  }
  return {
    datas: datas,
    total: total,
  };
}

const main = async () => {
  const api = new Octokit({
    auth: env.GITHUB_TOKEN,
  });
  const { total, datas } = await getAllPullRequests(api, owner, repo);

  console.log(
    `${total} ${total === 0 ? "Pull Request" : "Pull Requests"} ${
      total === 0 ? "is" : "are"
    } still opened`,
  );
  for (let data of datas) {
    try {
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
            await api.rest.issues.createComment({
              owner: owner,
              repo: repo,
              issue_number: obj.number,
              body: `The request from my owner require me to close this Pull Request\n\nThis Pull Request will always be closed if the following comment still exist\n> CoolPlayLin \n>${body}`,
            });
            await api.rest.pulls.update({
              owner: owner,
              repo: repo,
              pull_number: obj.number,
              state: "closed",
            });
            console.log(`Closes #${obj.number}`);
          }
        });
      });
    } catch (error) {
      console.log(`Request failed`);
    }
  }
};

main().catch((error) => {
  console.log(error);
});
