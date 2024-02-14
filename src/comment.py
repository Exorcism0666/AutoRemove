import os
import re
import requests

owner = "microsoft"
repo = "winget-pkgs"
login = "Exorcism0666"

def main():
    github_token = os.environ.get("GITHUB_TOKEN")
    headers = {
        "Authorization": f"token {github_token}"
    }
    with open("./docs/template.md", "r", encoding="utf-8") as f:
        content = f.read()

    datas = []
    i = 0
    while True:
        i += 1
        response = requests.get(
            f"https://api.github.com/search/issues?q=user:microsoft+repo:winget-pkgs+author:Exorcism0666+state:open+is:pr&per_page=100&page={i}",
            headers=headers
        )
        data = response.json().get("items", [])
        if not data:
            break
        datas.extend(data)

    for data in datas:
        issue_number = data["number"]
        comments_response = requests.get(
            f"https://api.github.com/repos/{owner}/{repo}/issues/{issue_number}/comments",
            headers=headers
        )
        comments = comments_response.json()
        for comment in comments:
            if comment["user"]["login"] == "Exorcism0666":
                body = comment["body"]
                if re.search(r"@Exorcism0666 Close", body, re.IGNORECASE):
                    print(f"Close #{issue_number}")
                    close_comment = "I've received my owner's request to close this PR, I'll close it right now"
                    requests.post(
                        f"https://api.github.com/repos/{owner}/{repo}/issues/{issue_number}/comments",
                        headers=headers,
                        json={"body": close_comment}
                    )
                    requests.patch(
                        f"https://api.github.com/repos/{owner}/{repo}/pulls/{issue_number}",
                        headers=headers,
                        json={"state": "closed"}
                    )
        ready_comments = [obj for obj in comments if obj["user"]["login"] == login and "## For moderators" in obj["body"]]
        if not ready_comments:
            create_comment_response = requests.post(
                f"https://api.github.com/repos/{owner}/{repo}/issues/{issue_number}/comments",
                headers=headers,
                json={"body": content}
            )
            print(f"Create #{issue_number}")

if __name__ == "__main__":
    main()