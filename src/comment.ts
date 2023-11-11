import { Octokit } from "@octokit/rest";
import { env } from "node:process";
import { readFileSync } from "node:fs";
import colors from "@colors/colors";

const owner = "microsoft";
const repo = "winget-pkgs";
const login = "coolplaylinbot";

(async () => {
  console.log(
    colors.underline(
      colors.green(
        "Hello everyone, I am going to post comment automatically. But I will check something before doing it.",
      ),
    ),
  );
  console.log(colors.underline(colors.yellow("Try to login.....")));
  const api = new Octokit({
    auth: env.GITHUB_TOKEN,
  });
  const user = await api.request("GET /user", {
    headers: {
      "X-GitHub-Api-Version": "2022-11-28",
    },
  });
  console.log(
    `${colors.green("Login succeed: Hello")} ${colors.underline(
      colors.green(user.data.name as string),
    )}`,
  );
  let content = readFileSync("./docs/template.md", "utf-8");
  let i = 0;
  while (true) {
    i += 1
    const data = (
      await api.rest.search.issuesAndPullRequests({
        q: "user:microsoft repo:winget-pkgs author:coolplaylinbot state:open is:pr",
        per_page: 100,
        page: i
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
      break
    }
    data.forEach(async (obj) => {
      const comments = await api.rest.issues.listComments({
        repo: repo,
        owner: owner,
        issue_number: obj.number,
      });
      const ready = comments.data.filter((obj) => {
        if (obj.user?.login == login && obj.body?.includes("## For moderators")) {
          return obj;
        }
      });
      console.log(
        `${colors.underline(
          colors.green(`[${data.indexOf(obj) + 1}/${data.length}]`),
        )} ${colors.blue("issue")} ${colors.yellow(`#${obj.number}`)}`,
      );
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
          )} ${colors.green(`posts succeed`)}`,
        );
      } else {
        console.log(
          `${colors.blue(`Comment in issue`)} ${colors.yellow(
            `#${obj.number}`,
          )} ${colors.blue("has been already posted.")}`,
        );
      }
    });
  }
})();
