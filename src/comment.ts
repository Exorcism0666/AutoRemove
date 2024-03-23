import { Octokit } from "@octokit/rest";
import { env } from "node:process";
import { readFileSync } from "node:fs";

const owner = "microsoft";
const repo = "winget-pkgs";
const login = "coolplaylinbot";

const main = async () => {
  const api = new Octokit({
    auth: env.GITHUB_TOKEN,
  });
  let content = readFileSync("./docs/template.md", "utf-8");
  let i = 0;
  const datas: any[] = [];
  while (true) {
    i += 1;
    let _ = (
      await api.rest.search.issuesAndPullRequests({
        q: "user:microsoft repo:winget-pkgs author:coolplaylinbot state:open is:pr",
        per_page: 100,
        page: i,
      })
    ).data.items;
    if (_.length == 0) break;
    datas.push(_);
  }
  datas.forEach((data) => {
    data.forEach(async (obj) => {
      const comments = await api.rest.issues.listComments({
        repo: repo,
        owner: owner,
        issue_number: obj.number,
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
        console.log(`Create tip for #${obj.number}`);
      }
    });
  });
};

main().catch((error) => {
  console.log(error);
});
