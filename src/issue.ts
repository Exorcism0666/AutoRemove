import { Octokit } from "@octokit/rest";
import { env } from "node:process";

const owner = "microsoft";
const repo = "winget-pkgs";
const bot_login = "Exorcism0666";
const owner_login = "Exorcism0666";

async function getAllPullRequests(token: string, owner: string, repo: string) {
  const api = new Octokit({
    auth: token,
  });
  let results = [];
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
    results.push(...searchedContent);
  }
  return results;
}

const main = async () => {
  const results = await getAllPullRequests(env.GITHUB_TOKEN, owner, repo);
  console.log(
    `${results.length} ${results.length === 0 ? "Pull Request" : "Pull Requests"} ${
      results.length === 0 ? "is" : "are"
    } still opened`,
  );
  const api = new Octokit({
    auth: env.GITHUB_TOKEN,
  });
  for (let r of results) {
    try {
      const labels = (
        await api.rest.issues.listLabelsOnIssue({
          repo: repo,
          owner: owner,
          issue_number: r.number,
        })
      ).data.map((label) => label.name);
      if (labels.includes("No-Recent-Activity")) {
        await api.rest.issues.createComment({
          owner: owner,
          repo: repo,
          issue_number: r.number,
          body: `Don't close this Pull Request please :)\nCC @Exorcism0666`,
        });
        console.log(`Prevent #${r.number} from being stale`);
      }
      const comments = await api.rest.issues.listComments({
        repo: repo,
        owner: owner,
        issue_number: r.number,
      });
      comments.data.forEach(async (comment) => {
        if (comment.user.login !== owner_login) {
          return;
        }
        const { body } = comment;
        if (body.match(/@[Ee]xorcism0666 [Cc]lose/)) {
          await api.rest.issues.createComment({
            owner: owner,
            repo: repo,
            issue_number: r.number,
            body: `The request from my owner requires to close this Pull Request\n\nThis Pull Request will always be closed if the following comment still exists\n>${body}`,
          });
          await api.rest.pulls.update({
            owner: owner,
            repo: repo,
            pull_number: r.number,
            state: "closed",
          });
          console.log(`Closes #${r.number}`);
        }
      });
      await setTimeout(() => {}, 1000 * 5);
    } catch {
      console.log(`Request failed`);
    }
  }
};

main();
