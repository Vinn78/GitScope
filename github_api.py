import os

import requests
from dotenv import load_dotenv

from data_processor import (
    commits_to_dataframe,
    issues_to_dataframe,
    pull_requests_to_dataframe,
    languages_to_dataframe,
    releases_to_dataframe,
    contributors_to_dataframe,
    calculate_commit_metrics,
    calculate_commit_activity_trend,
    calculate_issue_metrics,
    calculate_pull_request_metrics,
    calculate_contributor_metrics,
    calculate_contributor_concentration,
    calculate_release_metrics
)


# ==============================
# Environment Configuration
# ==============================

load_dotenv()

GITHUB_API_URL = "https://api.github.com"

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")


# ==============================
# GitHub API Headers
# ==============================

HEADERS = {
    "Accept": "application/vnd.github+json",
    "X-GitHub-Api-Version": "2022-11-28"
}

if GITHUB_TOKEN:
    HEADERS["Authorization"] = f"Bearer {GITHUB_TOKEN}"


# ==============================
# Shared API Request Function
# ==============================

def github_get(url, params=None):

    response = requests.get(
        url,
        params=params,
        headers=HEADERS,
        timeout=30
    )

    # Rate limit handling
    if response.status_code == 403:

        remaining = response.headers.get(
            "X-RateLimit-Remaining"
        )

        reset_time = response.headers.get(
            "X-RateLimit-Reset"
        )

        if remaining == "0":

            raise Exception(
                "GitHub API rate limit reached. "
                f"Rate limit reset timestamp: {reset_time}. "
                "Please try again after the limit resets."
            )

    # General API error handling
    if response.status_code != 200:

        raise Exception(
            f"GitHub API error: "
            f"{response.status_code} - "
            f"{response.text}"
        )

    return response.json()


# ==============================
# Controlled Pagination
# ==============================

def github_get_all(
    url,
    params=None,
    per_page=100,
    max_records=500
):

    if params is None:
        params = {}

    all_data = []

    page = 1

    while len(all_data) < max_records:

        page_params = params.copy()

        page_params["per_page"] = per_page
        page_params["page"] = page

        data = github_get(
            url,
            page_params
        )

        if not data:
            break

        remaining_records = (
            max_records - len(all_data)
        )

        all_data.extend(
            data[:remaining_records]
        )

        if len(data) < per_page:
            break

        page += 1

    return all_data


# ==============================
# Repository API
# ==============================

def get_repository(owner, repo):

    url = (
        f"{GITHUB_API_URL}/repos/"
        f"{owner}/{repo}"
    )

    return github_get(url)


# ==============================
# Commits API
# ==============================

def get_commits(
    owner,
    repo,
    per_page=100,
    max_records=500
):

    url = (
        f"{GITHUB_API_URL}/repos/"
        f"{owner}/{repo}/commits"
    )

    return github_get_all(
        url,
        per_page=per_page,
        max_records=max_records
    )


# ==============================
# Contributors API
# ==============================

def get_contributors(
    owner,
    repo,
    per_page=100,
    max_records=500
):

    url = (
        f"{GITHUB_API_URL}/repos/"
        f"{owner}/{repo}/contributors"
    )

    return github_get_all(
        url,
        per_page=per_page,
        max_records=max_records
    )


# ==============================
# Issues API
# ==============================

def get_issues(
    owner,
    repo,
    state="all",
    per_page=100,
    max_records=500
):

    url = (
        f"{GITHUB_API_URL}/repos/"
        f"{owner}/{repo}/issues"
    )

    params = {
        "state": state
    }

    return github_get_all(
        url,
        params=params,
        per_page=per_page,
        max_records=max_records
    )


# ==============================
# Pull Requests API
# ==============================

def get_pull_requests(
    owner,
    repo,
    state="all",
    per_page=100,
    max_records=500
):

    url = (
        f"{GITHUB_API_URL}/repos/"
        f"{owner}/{repo}/pulls"
    )

    params = {
        "state": state
    }

    return github_get_all(
        url,
        params=params,
        per_page=per_page,
        max_records=max_records
    )


# ==============================
# Languages API
# ==============================

def get_languages(owner, repo):

    url = (
        f"{GITHUB_API_URL}/repos/"
        f"{owner}/{repo}/languages"
    )

    return github_get(url)


# ==============================
# Releases API
# ==============================

def get_releases(
    owner,
    repo,
    per_page=100,
    max_records=500
):

    url = (
        f"{GITHUB_API_URL}/repos/"
        f"{owner}/{repo}/releases"
    )

    return github_get_all(
        url,
        per_page=per_page,
        max_records=max_records
    )


# ==============================
# Complete Repository Analysis
# ==============================

def analyze_repository(
    owner,
    repo,
    selected_analyses=None
):

    # ==========================
    # Fetch Repository Data
    # ==========================

    repository = get_repository(
        owner,
        repo
    )

    # If no selections are provided,
    # analyze all available sections.
    if selected_analyses is None:

        selected_analyses = [
            "Commits",
            "Contributors",
            "Issues",
            "Pull Requests",
            "Languages",
            "Releases"
        ]

    selected_analyses = set(
        selected_analyses
    )

    # ==========================
    # Initialize Empty Data
    # ==========================

    commits = []
    contributors = []
    issues = []
    pull_requests = []
    languages = {}
    releases = []

    # ==========================
    # Fetch Selected Data Only
    # ==========================

    if "Commits" in selected_analyses:

        commits = get_commits(
            owner,
            repo
        )

    if "Contributors" in selected_analyses:

        contributors = get_contributors(
            owner,
            repo
        )

    if "Issues" in selected_analyses:

        issues = get_issues(
            owner,
            repo
        )

    if "Pull Requests" in selected_analyses:

        pull_requests = get_pull_requests(
            owner,
            repo
        )

    if "Languages" in selected_analyses:

        languages = get_languages(
            owner,
            repo
        )

    if "Releases" in selected_analyses:

        releases = get_releases(
            owner,
            repo
        )

    # ==========================
    # Convert API Data
    # ==========================

    commits_df = commits_to_dataframe(
        commits
    )

    contributors_df = contributors_to_dataframe(
        contributors
    )

    issues_df = issues_to_dataframe(
        issues
    )

    pull_requests_df = pull_requests_to_dataframe(
        pull_requests
    )

    languages_df = languages_to_dataframe(
        languages
    )

    releases_df = releases_to_dataframe(
        releases
    )

    # ==========================
    # Calculate Metrics
    # ==========================

    commit_metrics = calculate_commit_metrics(
        commits_df
    )

    commit_activity_trend = (
        calculate_commit_activity_trend(
            commits_df
        )
    )

    contributor_metrics = (
        calculate_contributor_metrics(
            contributors_df
        )
    )

    contributor_concentration = (
        calculate_contributor_concentration(
            contributors_df
        )
    )

    issue_metrics = calculate_issue_metrics(
        issues_df
    )

    pull_request_metrics = (
        calculate_pull_request_metrics(
            pull_requests_df
        )
    )

    release_metrics = calculate_release_metrics(
        releases_df
    )

    # ==========================
    # Return Complete Analysis
    # ==========================

    return {
        "repository": repository,

        "commits": commits_df,

        "contributors": contributors_df,

        "issues": issues_df,

        "pull_requests": pull_requests_df,

        "languages": languages_df,

        "releases": releases_df,

        "commit_metrics": commit_metrics,

        "commit_activity_trend": (
            commit_activity_trend
        ),

        "contributor_metrics": (
            contributor_metrics
        ),

        "contributor_concentration": (
            contributor_concentration
        ),

        "issue_metrics": issue_metrics,

        "pull_request_metrics": (
            pull_request_metrics
        ),

        "release_metrics": release_metrics
    }


# ==============================
# Testing
# ==============================

if __name__ == "__main__":

    owner = "pandas-dev"
    repo = "pandas"

    print("=" * 60)
    print("GitScope Repository Analysis Test")
    print("=" * 60)

    if GITHUB_TOKEN:

        print(
            "\nGitHub authentication: ENABLED"
        )

    else:

        print(
            "\nGitHub authentication: "
            "NOT CONFIGURED"
        )

    print(
        "\nFetching repository data..."
    )

    analysis = analyze_repository(
        owner,
        repo
    )

    repository = analysis["repository"]

    print("\nRepository:")

    print(
        f"Name: {repository['full_name']}"
    )

    print(
        f"Stars: {repository['stargazers_count']}"
    )

    print(
        f"Forks: {repository['forks_count']}"
    )

    print(
        f"Open Issues: "
        f"{repository['open_issues_count']}"
    )

    print(
        f"Language: "
        f"{repository['language']}"
    )

    # ==========================
    # Record Counts
    # ==========================

    print("\nRecord Counts:")

    print(
        f"Commits: "
        f"{len(analysis['commits'])}"
    )

    print(
        f"Contributors: "
        f"{len(analysis['contributors'])}"
    )

    print(
        f"Issues: "
        f"{len(analysis['issues'])}"
    )

    print(
        f"Pull Requests: "
        f"{len(analysis['pull_requests'])}"
    )

    print(
        f"Releases: "
        f"{len(analysis['releases'])}"
    )

    # ==========================
    # Metrics
    # ==========================

    print("\nCommit Metrics:")

    print(
        analysis["commit_metrics"]
    )

    print("\nCommit Activity Trend:")

    print(
        analysis["commit_activity_trend"]
    )

    print("\nContributor Metrics:")

    print(
        analysis["contributor_metrics"]
    )

    print("\nContributor Concentration:")

    print(
        analysis["contributor_concentration"]
    )

    print("\nIssue Metrics:")

    print(
        analysis["issue_metrics"]
    )

    print("\nPull Request Metrics:")

    print(
        analysis["pull_request_metrics"]
    )

    print("\nRelease Metrics:")

    print(
        analysis["release_metrics"]
    )

    print("\nLanguages:")

    print(
        analysis["languages"].head()
    )

    print("\nReleases:")

    print(
        analysis["releases"].head()
    )

    print(
        "\n" + "=" * 60
    )

    print(
        "Analysis completed successfully."
    )

    print(
        "=" * 60
    )