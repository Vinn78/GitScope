import requests
from data_processor import commits_to_dataframe

GITHUB_API_URL = "https://api.github.com"


def get_repository(owner, repo):
    url = f"{GITHUB_API_URL}/repos/{owner}/{repo}"

    response = requests.get(url)

    if response.status_code != 200:
        raise Exception(
            f"GitHub API error: {response.status_code} - {response.text}"
        )

    return response.json()


def get_commits(owner, repo, per_page=30):
    url = f"{GITHUB_API_URL}/repos/{owner}/{repo}/commits"

    params = {
        "per_page": per_page
    }

    response = requests.get(url, params=params)

    if response.status_code != 200:
        raise Exception(
            f"GitHub API error: {response.status_code} - {response.text}"
        )

    return response.json()


if __name__ == "__main__":
    owner = "pandas-dev"
    repo = "pandas"

    data = get_repository(owner, repo)

    print("Repository:", data["full_name"])
    print("Description:", data["description"])
    print("Stars:", data["stargazers_count"])
    print("Forks:", data["forks_count"])
    print("Open Issues:", data["open_issues_count"])
    print("Language:", data["language"])

    commits = get_commits(owner, repo)

    print("\nRecent Commits:")

    for commit in commits[:5]:
        message = commit["commit"]["message"].split("\n")[0]
        author = commit["commit"]["author"]["name"]
        date = commit["commit"]["author"]["date"]

        print(f"- {date} | {author} | {message}")

    df = commits_to_dataframe(commits)

    print("\nCommit DataFrame:")
    print(df.head())
