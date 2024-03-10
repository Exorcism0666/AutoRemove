import { Octokit } from "@octokit/rest";
import { env } from "node:process";
import { readFileSync } from "node:fs";

const owner = "microsoft";
const repo = "winget-pkgs";
const login = "coolplaylinbot";

const main = (async () => {
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
      try {
        await api.rest.issues.removeAssignees({
          repo: repo,
          owner: owner,
          issue_number: obj.number,
          assignees: ["coolplaylinbot"],
        });
        await api.rest.issues.createComment({
          owner: owner,
          repo: repo,
          issue_number: obj.number,
          body: `Sorry, currently I can't reply you now, I'll call @CoolPlayLin instead.\n\n**Note: DO NOT ASSIGN TO THIS ACCOUNT AGAIN, ALL ASSIGNEES OF THIS ACCOUNT WILL BE REMOVED AUTOMATICALLY**`,
        });
      } catch (error) {
        console.log("No assignee need to be removed");
      }
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
  });
});

try {
  main()
} catch (error) {
  console.log(error)
}
