import feedparser
import requests
import base64
import os

def fetch_arxiv_title(arxiv_id):
    arxiv_api_url = f"http://export.arxiv.org/api/query?id_list={arxiv_id}"
    feed = feedparser.parse(arxiv_api_url)
    if len(feed.entries) == 0:
        return "Not found"
    return feed.entries[0].title


def update_github_readme(token, repo, new_entry):
    api_url = f"https://api.github.com/repos/{repo}/contents/README.md"
    headers = {
        "Authorization": f"token {token}",
    }

    # READMEを取得
    r = requests.get(api_url, headers=headers)
    r.raise_for_status()
    readme_data = r.json()
    readme_content = readme_data['content']
    readme_sha = readme_data['sha']

    # 新しい内容を追加
    readme_text = base64.b64decode(readme_content).decode('utf-8')
    updated_readme_text = readme_text + "\n" + new_entry
    updated_readme_content = base64.b64encode(updated_readme_text.encode('utf-8')).decode('utf-8')

    # 更新
    payload = {
        "message": "Update README.md",
        "content": updated_readme_content,
        "sha": readme_sha
    }

    r = requests.put(api_url, headers=headers, json=payload)
    r.raise_for_status()


if __name__ == "__main__":
    arxiv_url = input("Enter the arXiv URL: ")
    arxiv_id = arxiv_url.split("/")[-1]

    paper_title = fetch_arxiv_title(arxiv_id)
    new_entry = f"- [{paper_title}]({arxiv_url})"

    github_token = os.environ["GITHUB_TOKEN"]
    github_repo = "t46/research-automation-papers"
    
    update_github_readme(github_token, github_repo, new_entry)
