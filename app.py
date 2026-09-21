import re

import plotly.express as px
import streamlit as st

from github_api import analyze_repository


# ==============================
# Page Configuration
# ==============================

st.set_page_config(
    page_title="GitScope",
    page_icon="🔎",
    layout="wide"
)


# ==============================
# Helper Functions
# ==============================

def parse_github_url(url):
    pattern = (
        r"https?://github\.com/"
        r"([^/\s]+)/([^/\s]+)"
        r"/?$"
    )

    match = re.match(
        pattern,
        url.strip()
    )

    if not match:
        return None, None

    owner = match.group(1)
    repo = match.group(2)

    return owner, repo


def format_percentage(value):
    return f"{value:.2f}%"


# ==============================
# Header
# ==============================

st.title("🔎 GitScope")

st.subheader(
    "GitHub Repository Activity & Collaboration Analyzer"
)

st.write(
    "Analyze public GitHub repositories using "
    "the GitHub REST API."
)


# ==============================
# Repository Input
# ==============================

repository_url = st.text_input(
    "GitHub Repository URL",
    placeholder="https://github.com/owner/repository"
)


# ==============================
# Analysis Selection
# ==============================

st.subheader("Select Analyses")

analysis_options = [
    "Commits",
    "Contributors",
    "Issues",
    "Pull Requests",
    "Languages",
    "Releases"
]

selected_analyses = st.multiselect(
    "Choose one or more analyses",
    analysis_options
)


analyze_button = st.button(
    "Analyze Selected",
    type="primary"
)


# ==============================
# Repository Analysis
# ==============================

if analyze_button:

    if not repository_url.strip():

        st.error(
            "Please enter a GitHub repository URL."
        )

        st.stop()

    owner, repo = parse_github_url(
        repository_url
    )

    if not owner or not repo:

        st.error(
            "Invalid GitHub repository URL. "
            "Use the format: "
            "https://github.com/owner/repository"
        )

        st.stop()

    if not selected_analyses:

        st.warning(
            "Please select at least one analysis."
        )

        st.stop()

    try:

        with st.spinner(
            "Fetching repository data from GitHub..."
        ):

            analysis = analyze_repository(
                owner,
                repo
            )

        st.success(
            "Repository analysis completed successfully."
        )

    except Exception as error:

        st.error(
            f"Unable to analyze repository: {error}"
        )

        st.stop()


    repository = analysis["repository"]


    # ==============================
    # Repository Overview
    # ==============================

    st.header("Repository Overview")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            "Stars",
            repository.get(
                "stargazers_count",
                0
            )
        )

    with col2:
        st.metric(
            "Forks",
            repository.get(
                "forks_count",
                0
            )
        )

    with col3:
        st.metric(
            "Open Issues",
            repository.get(
                "open_issues_count",
                0
            )
        )

    with col4:
        st.metric(
            "Primary Language",
            repository.get(
                "language"
            ) or "N/A"
        )


    st.write(
        f"**Repository:** "
        f"{repository.get('full_name', 'N/A')}"
    )

    st.write(
        f"**Description:** "
        f"{repository.get('description') or 'No description available.'}"
    )

    st.write(
        f"**Default Branch:** "
        f"{repository.get('default_branch', 'N/A')}"
    )


    # ==============================
    # Commits Analysis
    # ==============================

    if "Commits" in selected_analyses:

        st.header("Commit Analysis")

        commit_metrics = analysis[
            "commit_metrics"
        ]

        activity_metrics = analysis[
            "commit_activity_trend"
        ]

        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric(
                "Total Commits",
                commit_metrics[
                    "total_commits"
                ]
            )

        with col2:
            st.metric(
                "Unique Contributors",
                commit_metrics[
                    "unique_contributors"
                ]
            )

        with col3:
            st.metric(
                "Avg Commits / Day",
                f"{commit_metrics['average_commits_per_day']:.2f}"
            )


        st.subheader(
            "Commit Activity Trend"
        )

        trend_col1, trend_col2 = st.columns(2)

        with trend_col1:

            st.write(
                f"**First Commit:** "
                f"{activity_metrics['first_commit_date']}"
            )

            st.write(
                f"**Latest Commit:** "
                f"{activity_metrics['latest_commit_date']}"
            )

            st.write(
                f"**Active Days:** "
                f"{activity_metrics['active_days']}"
            )

        with trend_col2:

            st.write(
                f"**Most Active Day:** "
                f"{activity_metrics['most_active_day']}"
            )

            st.write(
                f"**Commits on Most Active Day:** "
                f"{activity_metrics['most_active_day_commits']}"
            )


        commits_df = analysis[
            "commits"
        ]

        if not commits_df.empty:

            daily_commits = (
                commits_df
                .groupby("day")
                .size()
                .reset_index(
                    name="commits"
                )
            )

            figure = px.line(
                daily_commits,
                x="day",
                y="commits",
                markers=True,
                title="Commits Over Time"
            )

            st.plotly_chart(
                figure,
                use_container_width=True
            )

            st.dataframe(
                commits_df,
                use_container_width=True
            )

        else:

            st.info(
                "No commit data available."
            )


    # ==============================
    # Contributors Analysis
    # ==============================

    if "Contributors" in selected_analyses:

        st.header(
            "Contributor Analysis"
        )

        contributor_metrics = analysis[
            "contributor_metrics"
        ]

        concentration = analysis[
            "contributor_concentration"
        ]

        col1, col2, col3 = st.columns(3)

        with col1:

            st.metric(
                "Contributors Analyzed",
                contributor_metrics[
                    "total_contributors"
                ]
            )

        with col2:

            st.metric(
                "Top Contributor",
                contributor_metrics[
                    "top_contributor"
                ]
            )

        with col3:

            st.metric(
                "Top Contributor Share",
                format_percentage(
                    concentration[
                        "top_contributor_concentration"
                    ]
                )
            )


        st.subheader(
            "Contributor Concentration"
        )

        st.write(
            "Share of analyzed contributions "
            "made by the leading contributors."
        )

        concentration_col1, concentration_col2 = (
            st.columns(2)
        )

        with concentration_col1:

            st.metric(
                "Top Contributor",
                format_percentage(
                    concentration[
                        "top_contributor_concentration"
                    ]
                )
            )

        with concentration_col2:

            st.metric(
                "Top 3 Contributors",
                format_percentage(
                    concentration[
                        "top_3_contributor_concentration"
                    ]
                )
            )


        contributors_df = analysis[
            "contributors"
        ]

        if not contributors_df.empty:

            figure = px.bar(
                contributors_df,
                x="username",
                y="contributions",
                title="Contributor Contributions"
            )

            st.plotly_chart(
                figure,
                use_container_width=True
            )

            st.dataframe(
                contributors_df,
                use_container_width=True
            )

        else:

            st.info(
                "No contributor data available."
            )


    # ==============================
    # Issues Analysis
    # ==============================

    if "Issues" in selected_analyses:

        st.header("Issue Analysis")

        issue_metrics = analysis[
            "issue_metrics"
        ]

        col1, col2, col3, col4 = st.columns(4)

        with col1:

            st.metric(
                "Total Issues",
                issue_metrics[
                    "total_issues"
                ]
            )

        with col2:

            st.metric(
                "Open",
                issue_metrics[
                    "open_issues"
                ]
            )

        with col3:

            st.metric(
                "Closed",
                issue_metrics[
                    "closed_issues"
                ]
            )

        with col4:

            st.metric(
                "Closure Rate",
                format_percentage(
                    issue_metrics[
                        "closure_rate"
                    ]
                )
            )


        issues_df = analysis[
            "issues"
        ]

        if not issues_df.empty:

            issue_state_counts = (
                issues_df["state"]
                .value_counts()
                .reset_index()
            )

            issue_state_counts.columns = [
                "state",
                "count"
            ]

            figure = px.pie(
                issue_state_counts,
                names="state",
                values="count",
                title="Issue Status Distribution"
            )

            st.plotly_chart(
                figure,
                use_container_width=True
            )

            st.dataframe(
                issues_df,
                use_container_width=True
            )

        else:

            st.info(
                "No issue data available."
            )


    # ==============================
    # Pull Request Analysis
    # ==============================

    if "Pull Requests" in selected_analyses:

        st.header(
            "Pull Request Analysis"
        )

        pr_metrics = analysis[
            "pull_request_metrics"
        ]

        col1, col2, col3, col4 = st.columns(4)

        with col1:

            st.metric(
                "Total PRs",
                pr_metrics[
                    "total_pull_requests"
                ]
            )

        with col2:

            st.metric(
                "Open PRs",
                pr_metrics[
                    "open_pull_requests"
                ]
            )

        with col3:

            st.metric(
                "Merged PRs",
                pr_metrics[
                    "merged_pull_requests"
                ]
            )

        with col4:

            st.metric(
                "Merge Rate",
                format_percentage(
                    pr_metrics[
                        "merge_rate"
                    ]
                )
            )


        pull_requests_df = analysis[
            "pull_requests"
        ]

        if not pull_requests_df.empty:

            pr_state_counts = (
                pull_requests_df["state"]
                .value_counts()
                .reset_index()
            )

            pr_state_counts.columns = [
                "state",
                "count"
            ]

            figure = px.pie(
                pr_state_counts,
                names="state",
                values="count",
                title="Pull Request Status"
            )

            st.plotly_chart(
                figure,
                use_container_width=True
            )

            st.dataframe(
                pull_requests_df,
                use_container_width=True
            )

        else:

            st.info(
                "No pull request data available."
            )


    # ==============================
    # Languages Analysis
    # ==============================

    if "Languages" in selected_analyses:

        st.header(
            "Programming Language Analysis"
        )

        languages_df = analysis[
            "languages"
        ]

        if not languages_df.empty:

            figure = px.pie(
                languages_df,
                names="language",
                values="percentage",
                title="Programming Language Distribution"
            )

            st.plotly_chart(
                figure,
                use_container_width=True
            )

            st.dataframe(
                languages_df,
                use_container_width=True
            )

        else:

            st.info(
                "No language data available."
            )


    # ==============================
    # Releases Analysis
    # ==============================

    if "Releases" in selected_analyses:

        st.header(
            "Release Analysis"
        )

        release_metrics = analysis[
            "release_metrics"
        ]

        col1, col2 = st.columns(2)

        with col1:

            st.metric(
                "Total Releases",
                release_metrics[
                    "total_releases"
                ]
            )

        with col2:

            st.metric(
                "Latest Release",
                release_metrics[
                    "latest_release"
                ]
            )


        releases_df = analysis[
            "releases"
        ]

        if not releases_df.empty:

            st.dataframe(
                releases_df,
                use_container_width=True
            )

        else:

            st.info(
                "No release data available."
            )