import pandas as pd


def commits_to_dataframe(commits):
    rows = []

    for commit in commits:
        commit_data = commit["commit"]

        rows.append(
            {
                "sha": commit["sha"],
                "author": commit_data["author"]["name"],
                "date": commit_data["author"]["date"],
                "message": commit_data["message"].split("\n")[0],
            }
        )

    df = pd.DataFrame(rows)

    if not df.empty:
        df["date"] = pd.to_datetime(df["date"])
        df["day"] = df["date"].dt.date

    return df
