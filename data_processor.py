import pandas as pd


# ==============================
# Commit Processing
# ==============================

def commits_to_dataframe(commits):
    rows = []

    for commit in commits:

        commit_data = commit.get(
            "commit",
            {}
        )

        author_data = (
            commit_data.get("author")
            or {}
        )

        rows.append(
            {
                "sha": commit.get("sha"),
                "author": author_data.get(
                    "name",
                    "Unknown"
                ),
                "date": author_data.get("date"),
                "message": commit_data.get(
                    "message",
                    ""
                ).split("\n")[0],
            }
        )

    df = pd.DataFrame(rows)

    if not df.empty:

        df["date"] = pd.to_datetime(
            df["date"]
        )

        df["day"] = df["date"].dt.date

    return df


# ==============================
# Issue Processing
# ==============================

def issues_to_dataframe(issues):
    rows = []

    for issue in issues:

        # GitHub's Issues API also returns
        # Pull Requests.
        if "pull_request" in issue:
            continue

        user_data = (
            issue.get("user")
            or {}
        )

        rows.append(
            {
                "number": issue.get("number"),
                "title": issue.get("title"),
                "state": issue.get("state"),
                "author": user_data.get(
                    "login",
                    "Unknown"
                ),
                "created_at": issue.get(
                    "created_at"
                ),
                "closed_at": issue.get(
                    "closed_at"
                ),
                "comments": issue.get(
                    "comments",
                    0
                ),
            }
        )

    df = pd.DataFrame(rows)

    if not df.empty:

        df["created_at"] = pd.to_datetime(
            df["created_at"]
        )

        df["closed_at"] = pd.to_datetime(
            df["closed_at"]
        )

    return df


# ==============================
# Pull Request Processing
# ==============================

def pull_requests_to_dataframe(
    pull_requests
):
    rows = []

    for pull_request in pull_requests:

        user_data = (
            pull_request.get("user")
            or {}
        )

        rows.append(
            {
                "number": pull_request.get(
                    "number"
                ),
                "title": pull_request.get(
                    "title"
                ),
                "state": pull_request.get(
                    "state"
                ),
                "author": user_data.get(
                    "login",
                    "Unknown"
                ),
                "created_at": pull_request.get(
                    "created_at"
                ),
                "closed_at": pull_request.get(
                    "closed_at"
                ),
                "merged_at": pull_request.get(
                    "merged_at"
                ),
                "comments": pull_request.get(
                    "comments",
                    0
                ),
            }
        )

    df = pd.DataFrame(rows)

    if not df.empty:

        df["created_at"] = pd.to_datetime(
            df["created_at"]
        )

        df["closed_at"] = pd.to_datetime(
            df["closed_at"]
        )

        df["merged_at"] = pd.to_datetime(
            df["merged_at"]
        )

    return df


# ==============================
# Language Processing
# ==============================

def languages_to_dataframe(languages):
    rows = []

    for language, bytes_count in languages.items():

        rows.append(
            {
                "language": language,
                "bytes": bytes_count
            }
        )

    df = pd.DataFrame(rows)

    if not df.empty:

        total_bytes = df["bytes"].sum()

        if total_bytes > 0:

            df["percentage"] = (
                df["bytes"]
                / total_bytes
            ) * 100

        else:

            df["percentage"] = 0.0

        df = df.sort_values(
            "bytes",
            ascending=False
        ).reset_index(
            drop=True
        )

    return df


# ==============================
# Release Processing
# ==============================

def releases_to_dataframe(releases):
    rows = []

    for release in releases:

        author_data = (
            release.get("author")
            or {}
        )

        rows.append(
            {
                "tag": release.get(
                    "tag_name",
                    "Unknown"
                ),
                "name": (
                    release.get("name")
                    or release.get(
                        "tag_name",
                        "No name"
                    )
                ),
                "author": author_data.get(
                    "login",
                    "Unknown"
                ),
                "created_at": release.get(
                    "created_at"
                ),
                "published_at": release.get(
                    "published_at"
                ),
                "draft": release.get(
                    "draft",
                    False
                ),
                "prerelease": release.get(
                    "prerelease",
                    False
                ),
            }
        )

    df = pd.DataFrame(rows)

    if not df.empty:

        df["created_at"] = pd.to_datetime(
            df["created_at"]
        )

        df["published_at"] = pd.to_datetime(
            df["published_at"]
        )

    return df


# ==============================
# Contributor Processing
# ==============================

def contributors_to_dataframe(
    contributors
):
    rows = []

    for contributor in contributors:

        rows.append(
            {
                "username": contributor.get(
                    "login",
                    "Unknown"
                ),
                "contributions": contributor.get(
                    "contributions",
                    0
                ),
            }
        )

    df = pd.DataFrame(rows)

    if not df.empty:

        total_contributions = (
            df["contributions"].sum()
        )

        if total_contributions > 0:

            df["contribution_percentage"] = (
                df["contributions"]
                / total_contributions
            ) * 100

        else:

            df["contribution_percentage"] = 0.0

        df = df.sort_values(
            "contributions",
            ascending=False
        ).reset_index(
            drop=True
        )

    return df


# ==============================
# Commit Metrics
# ==============================

def calculate_commit_metrics(df):

    metrics = {
        "total_commits": 0,
        "unique_contributors": 0,
        "average_commits_per_day": 0.0
    }

    if df.empty:
        return metrics

    metrics["total_commits"] = int(
        len(df)
    )

    metrics["unique_contributors"] = int(
        df["author"].nunique()
    )

    date_range = (
        df["date"].max()
        - df["date"].min()
    ).days + 1

    if date_range > 0:

        metrics["average_commits_per_day"] = float(
            len(df) / date_range
        )

    return metrics


# ==============================
# Commit Activity Trend
# ==============================

def calculate_commit_activity_trend(df):

    metrics = {
        "first_commit_date": "N/A",
        "latest_commit_date": "N/A",
        "active_days": 0,
        "most_active_day": "N/A",
        "most_active_day_commits": 0
    }

    if df.empty:
        return metrics

    metrics["first_commit_date"] = (
        df["date"]
        .min()
        .strftime("%Y-%m-%d")
    )

    metrics["latest_commit_date"] = (
        df["date"]
        .max()
        .strftime("%Y-%m-%d")
    )

    metrics["active_days"] = int(
        df["day"].nunique()
    )

    daily_activity = (
        df.groupby("day")
        .size()
        .sort_values(
            ascending=False
        )
    )

    if not daily_activity.empty:

        metrics["most_active_day"] = str(
            daily_activity.index[0]
        )

        metrics["most_active_day_commits"] = int(
            daily_activity.iloc[0]
        )

    return metrics


# ==============================
# Issue Metrics
# ==============================

def calculate_issue_metrics(df):

    metrics = {
        "total_issues": 0,
        "open_issues": 0,
        "closed_issues": 0,
        "closure_rate": 0.0
    }

    if df.empty:
        return metrics

    metrics["total_issues"] = int(
        len(df)
    )

    metrics["open_issues"] = int(
        df["state"]
        .eq("open")
        .sum()
    )

    metrics["closed_issues"] = int(
        df["state"]
        .eq("closed")
        .sum()
    )

    if metrics["total_issues"] > 0:

        metrics["closure_rate"] = float(
            (
                metrics["closed_issues"]
                / metrics["total_issues"]
            ) * 100
        )

    return metrics


# ==============================
# Pull Request Metrics
# ==============================

def calculate_pull_request_metrics(df):

    metrics = {
        "total_pull_requests": 0,
        "open_pull_requests": 0,
        "closed_pull_requests": 0,
        "merged_pull_requests": 0,
        "merge_rate": 0.0
    }

    if df.empty:
        return metrics

    metrics["total_pull_requests"] = int(
        len(df)
    )

    metrics["open_pull_requests"] = int(
        df["state"]
        .eq("open")
        .sum()
    )

    metrics["closed_pull_requests"] = int(
        df["state"]
        .eq("closed")
        .sum()
    )

    metrics["merged_pull_requests"] = int(
        df["merged_at"]
        .notna()
        .sum()
    )

    if metrics["total_pull_requests"] > 0:

        metrics["merge_rate"] = float(
            (
                metrics["merged_pull_requests"]
                / metrics["total_pull_requests"]
            ) * 100
        )

    return metrics


# ==============================
# Contributor Metrics
# ==============================

def calculate_contributor_metrics(df):

    metrics = {
        "total_contributors": 0,
        "top_contributor": "N/A",
        "top_contributor_percentage": 0.0,
        "top_3_contributor_percentage": 0.0
    }

    if df.empty:
        return metrics

    metrics["total_contributors"] = int(
        len(df)
    )

    metrics["top_contributor"] = str(
        df.iloc[0]["username"]
    )

    metrics["top_contributor_percentage"] = float(
        df.iloc[0][
            "contribution_percentage"
        ]
    )

    metrics["top_3_contributor_percentage"] = float(
        df.head(3)[
            "contribution_percentage"
        ].sum()
    )

    return metrics


# ==============================
# Contributor Concentration
# ==============================

def calculate_contributor_concentration(df):

    metrics = {
        "top_contributor_concentration": 0.0,
        "top_3_contributor_concentration": 0.0
    }

    if df.empty:
        return metrics

    if (
        "contribution_percentage"
        not in df.columns
    ):
        return metrics

    metrics["top_contributor_concentration"] = float(
        df.iloc[0][
            "contribution_percentage"
        ]
    )

    metrics["top_3_contributor_concentration"] = float(
        df.head(3)[
            "contribution_percentage"
        ].sum()
    )

    return metrics


# ==============================
# Release Metrics
# ==============================

def calculate_release_metrics(df):

    metrics = {
        "total_releases": 0,
        "latest_release": "N/A"
    }

    if df.empty:
        return metrics

    metrics["total_releases"] = int(
        len(df)
    )

    published_releases = (
        df[
            df["published_at"].notna()
        ]
        .sort_values(
            "published_at",
            ascending=False
        )
    )

    if not published_releases.empty:

        metrics["latest_release"] = str(
            published_releases.iloc[0]["tag"]
        )

    return metrics