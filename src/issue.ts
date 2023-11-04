import { Octokit } from "@octokit/rest";
import { readFileSync } from "node:fs";
import { join } from "node:path";
import { env } from "node:process";

const api = new Octokit({
  auth: env.GITHUB_TOKEN,
});

(async () => {
  const issue_data = readFileSync(
    join(__dirname, "issue.md"),
    "utf-8",
  ) as string;
  if (issue_data.includes("-")) {
    api.rest.issues.create({
      owner: "microsoft",
      repo: "winget-pkgs",
      body: issue_data,
      title: "[Package issue] New Package Report",
    });
  }
})();
