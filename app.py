import streamlit as st
from github_api import get_repository, get_commits
from data_processor import commits_to_dataframe


st.set_page_config(
    page_title="GitScope",
    page_icon="📊",
    layout="wide"
)


st.title("📊 GitScope")
st.subheader("GitHub Repository Activity & Collaboration Analyzer")

st.write(
    "Enter a public GitHub repository URL to analyze its activity and collaboration data."
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

                df = commits_to_dataframe(commits)

            st.success("Repository analyzed successfully!")

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

            st.subheader("Repository Information")

            st.write(
                f"**Repository:** {repository['full_name']}"
            )

            st.write(
                f"**Description:** {repository['description'] or 'No description available.'}"
            )

            st.write(
                f"**Default Branch:** {repository['default_branch']}"
            )

            st.subheader("Recent Commit Activity")

            st.dataframe(
                df,
                use_container_width=True
            )

        except Exception as e:
            st.error(f"Error analyzing repository: {e}")
