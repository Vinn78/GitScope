import requests

GITHUB_API_URL = "https://api.github.com"


def get_repository(owner, repo):
    url = f"{GITHUB_API_URL}/repos/{owner}/{repo}"

    response = requests.get(url)

    if response.status_code != 200:
        raise Exception(
            f"GitHub API error: {response.status_code} - {response.text}"
        )

    return response.json()


if __name__ == "__main__":
    data = get_repository("pandas-dev", "pandas")

    print("Repository:", data["full_name"])
    print("Description:", data["description"])
    print("Stars:", data["stargazers_count"])
    print("Forks:", data["forks_count"])
    print("Open Issues:", data["open_issues_count"])
    print("Language:", data["language"])
