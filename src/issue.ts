import { Octokit } from "@octokit/rest";
import { readFileSync } from "node:fs";
import { join } from "node:path";
import { env } from "node:process";

const api = new Octokit({
  auth: env.GITHUB_TOKEN,
});

(async () => {
})();
