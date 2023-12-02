import { Octokit } from "@octokit/rest";
import { env } from "node:process";
import { readFileSync } from "node:fs";

const owner = "microsoft";
const repo = "winget-pkgs";
const login = "coolplaylinbot";

(async () => {
  const api = new Octokit({
    auth: env.GITHUB_TOKEN,
  });
  const user = await api.request("GET /user", {
    headers: {
      "X-GitHub-Api-Version": "2022-11-28",
    },
  });
  let content = readFileSync("./docs/template.md", "utf-8");
  let i = 0;
  while (true) {
    i += 1;
    const data = (
      await api.rest.search.issuesAndPullRequests({
        q: "user:microsoft repo:winget-pkgs author:coolplaylinbot state:open is:pr",
        per_page: 100,
        page: i,
      })
    ).data.items;
    if (data.length >= 1) {
      data.forEach(async (obj) => {
        const comments = await api.rest.issues.listComments({
          repo: repo,
          owner: owner,
          issue_number: obj.number,
        });
        comments.data.forEach(async (comment) => {
          if (comment.user.login !== "CoolPlayLin") {
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
        const ready = comments.data.filter((obj) => {
          if (
            obj.user?.login == login &&
            obj.body?.includes("## For moderators")
          ) {
            return obj;
          }
        });
        if (ready.length === 0) {
          const res = await api.issues.createComment({
            repo: repo,
            owner: owner,
            issue_number: obj.number,
            body: content,
          });
          console.log(`Create #${obj.number}`);
        }
      });
    }
  }
})();
