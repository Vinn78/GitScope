import streamlit as st
import pandas as pd
import plotly.express as px

from github_api import (
    get_repository,
    get_commits,
    get_contributors
)

from data_processor import commits_to_dataframe


st.set_page_config(
    page_title="GitScope",
    page_icon="📊",
    layout="wide"
)


st.title("📊 GitScope")
st.subheader("GitHub Repository Activity & Collaboration Analyzer")

st.write(
    "Enter a public GitHub repository URL to analyze its activity "
    "and collaboration data."
)


repo_url = st.text_input(
    "GitHub Repository URL",
    placeholder="https://github.com/pandas-dev/pandas"
)


if st.button("Analyze Repository"):

    if not repo_url:
        st.warning("Please enter a GitHub repository URL.")

    else:

        try:
            parts = repo_url.rstrip("/").split("/")

            if (
                len(parts) < 5
                or parts[0] != "https:"
                or parts[2] != "github.com"
            ):
                st.error("Please enter a valid GitHub repository URL.")
                st.stop()

            owner = parts[-2]
            repo = parts[-1]

            with st.spinner("Fetching repository data..."):

                repository = get_repository(owner, repo)

                commits = get_commits(owner, repo)

                contributors = get_contributors(owner, repo)

                df = commits_to_dataframe(commits)


            st.success("Repository analyzed successfully!")


            # ==============================
            # REPOSITORY OVERVIEW
            # ==============================

            st.header("Repository Overview")

            col1, col2, col3, col4 = st.columns(4)

            with col1:
                st.metric(
                    "⭐ Stars",
                    repository["stargazers_count"]
                )

            with col2:
                st.metric(
                    "🍴 Forks",
                    repository["forks_count"]
                )

            with col3:
                st.metric(
                    "🐛 Open Issues",
                    repository["open_issues_count"]
                )

            with col4:
                st.metric(
                    "💻 Language",
                    repository["language"] or "N/A"
                )


            # ==============================
            # REPOSITORY INFORMATION
            # ==============================

            st.subheader("Repository Information")

            st.write(
                f"**Repository:** {repository['full_name']}"
            )

            st.write(
                f"**Description:** "
                f"{repository['description'] or 'No description available.'}"
            )

            st.write(
                f"**Default Branch:** {repository['default_branch']}"
            )


            # ==============================
            # COMMIT ACTIVITY
            # ==============================

            st.header("Commit Activity")

            st.dataframe(
                df,
                width="stretch"
            )


            # ==============================
            # CONTRIBUTOR ANALYSIS
            # ==============================

            st.header("Contributor Analysis")

            contributor_rows = []

            for contributor in contributors:

                contributor_rows.append(
                    {
                        "Contributor": contributor.get(
                            "login",
                            "Unknown"
                        ),
                        "Contributions": contributor.get(
                            "contributions",
                            0
                        )
                    }
                )


            if contributor_rows:

                contributor_df = pd.DataFrame(
                    contributor_rows
                ).sort_values(
                    "Contributions",
                    ascending=False
                )


                col1, col2 = st.columns(2)


                with col1:

                    st.subheader("Top Contributors")

                    st.dataframe(
                        contributor_df,
                        width="stretch"
                    )


                with col2:

                    st.subheader("Contribution Distribution")

                    chart = px.bar(
                        contributor_df.head(10),
                        x="Contributions",
                        y="Contributor",
                        orientation="h",
                        title="Top 10 Contributors"
                    )

                    chart.update_layout(
                        yaxis={
                            "categoryorder": "total ascending"
                        }
                    )

                    st.plotly_chart(
                        chart,
                        width="stretch"
                    )


            else:

                st.info(
                    "No contributor data was available "
                    "for this repository."
                )


        except Exception as e:

            st.error(
                f"Error analyzing repository: {e}"
            )
