import { Octokit } from "@octokit/rest";
import { env } from "node:process";
import { readFileSync } from "node:fs";
import colors from "@colors/colors";

const owner = "microsoft";
const repo = "winget-pkgs";

(async () => {
  const api = new Octokit({
    auth: env.GITHUB_TOKEN,
  });
  let content = readFileSync("./docs/template.md", "utf-8");
  const data = (
    await api.rest.search.issuesAndPullRequests({
      q: "user:microsoft repo:winget-pkgs author:coolplaylinbot state:open is:pr",
    })
  ).data.items;
  if (data.length >= 1) {
    console.log(
      `${colors.green(
        `We've found ${data.length} pull request(s) that opened by coolplaylinbot`,
      )}`,
    );
  } else {
    console.log(
      `${colors.green(
        `We haven't found pull request that opened by coolplaylinbot`,
      )}`,
    );
  }
  data.forEach(async (obj) => {
    console.log(
      `[${data.indexOf(obj) + 1}/${data.length}] ${colors.blue(
        "issue",
      )} ${colors.yellow(`#${obj.number}`)}`,
    );
    const commets = await api.rest.issues.listComments({
      repo: repo,
      owner: owner,
      issue_number: obj.number,
    });
    const ready = commets.data.filter((obj) => {
      if (
        obj.user?.login == "coolplaylinbot" &&
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
      console.log(
        `${colors.green(`Comment in issue`)} ${colors.yellow(
          `#${obj.number}`,
        )} ${colors.green(`posts successfully`)}`,
      );
    } else {
      console.log(
        `${colors.blue(`Comment in issue`)} ${colors.yellow(
          `#${obj.number}`,
        )} ${colors.blue("has already posted comment.")}`,
      );
    }
  });
})();
