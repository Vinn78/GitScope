warning: in the working copy of 'app.py', LF will be replaced by CRLF the next time Git touches it
[1mdiff --git a/.gitignore b/.gitignore[m
[1mindex 133e9bf..6172349 100644[m
[1m--- a/.gitignore[m
[1m+++ b/.gitignore[m
[36m@@ -216,6 +216,6 @@[m [m__marimo__/[m
 [m
 # Streamlit[m
 .streamlit/secrets.toml[m
[31m-# GitScope project files[m
[32m+[m[32m# RepoMetric project files[m
 .venv/[m
 .env[m
[1mdiff --git a/README.md b/README.md[m
[1mindex ca7021d..71201fa 100644[m
[1m--- a/README.md[m
[1m+++ b/README.md[m
[36m@@ -1,4 +1,4 @@[m
[31m-# GitScope[m
[32m+[m[32m# RepoMetric[m
 GitHub Repository Activity &amp; Collaboration Analyzer[m
 [m
[31m-**Live Demo:** [Open GitScope](https://gitscope-5acuouho9dsd3bvwv2nkfw.streamlit.app/)[m
\ No newline at end of file[m
[32m+[m[32m**Live Demo:** [Open RepoMetric](https://gitscope-5acuouho9dsd3bvwv2nkfw.streamlit.app/)[m
\ No newline at end of file[m
[1mdiff --git a/app.py b/app.py[m
[1mindex 9599f2d..5229d62 100644[m
[1m--- a/app.py[m
[1m+++ b/app.py[m
[36m@@ -1,5 +1,5 @@[m
 """[m
[31m-GitScope - GitHub Repository Activity & Collaboration Analyzer[m
[32m+[m[32mRepoMetric - GitHub Repository Activity & Collaboration Analyzer[m
 ==============================================================[m
 [m
 Streamlit front end. This file only presents data: every number shown comes[m
[36m@@ -37,7 +37,7 @@[m [mfrom github_api import PERIOD_OPTIONS, analyze_repository[m
 # ==============================[m
 [m
 st.set_page_config([m
[31m-    page_title="GitScope",[m
[32m+[m[32m    page_title="RepoMetric",[m
     page_icon="🔎",[m
     layout="wide"[m
 )[m
[36m@@ -1280,7 +1280,7 @@[m [mdef hero():[m
     <div class="gs-hero">[m
         <div class="gs-mark">{icon('search', 26, 2.1)}</div>[m
         <div>[m
[31m-            <h1 class="gs-title">GitScope</h1>[m
[32m+[m[32m            <h1 class="gs-title">RepoMetric</h1>[m
             <div class="gs-subtitle">GitHub Repository Activity &amp; Collaboration Analyzer</div>[m
             <div class="gs-lede">[m
                 Point it at any public repository to pull commit activity, contributor[m
[36m@@ -2376,7 +2376,7 @@[m [mdef render_error(kind, message):[m
         notice([m
             "error",[m
             "GitHub API rate limit reached",[m
[31m-            "GitScope has hit GitHub's API rate limit for this token. "[m
[32m+[m[32m            "RepoMetric has hit GitHub's API rate limit for this token. "[m
             "Add a GITHUB_TOKEN to raise the limit, or try again shortly.",[m
             detail=message,[m
         )[m
[1mdiff --git a/docker-compose.yml b/docker-compose.yml[m
[1mindex 111012b..8505d08 100644[m
[1m--- a/docker-compose.yml[m
[1m+++ b/docker-compose.yml[m
[36m@@ -1,5 +1,5 @@[m
 services:[m
[31m-  gitscope:[m
[32m+[m[32m  repometric:[m
     build: .[m
     ports:[m
       - "8501:8501"[m
[1mdiff --git a/github_api.py b/github_api.py[m
[1mindex 8799cc6..234b946 100644[m
[1m--- a/github_api.py[m
[1m+++ b/github_api.py[m
[36m@@ -1133,7 +1133,7 @@[m [mif __name__ == "__main__":[m
     test_period = "Last 30 Days"[m
 [m
     print("=" * 60)[m
[31m-    print("GitScope Repository Analysis Test")[m
[32m+[m[32m    print("RepoMetric - Repository Analysis Test")[m
     print("=" * 60)[m
 [m
     if GITHUB_TOKEN:[m
