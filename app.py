import html
import re

import plotly.express as px
import streamlit as st

from github_api import analyze_repository


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="GitScope — GitHub Analytics",
    page_icon="◈",
    layout="wide",
    initial_sidebar_state="collapsed",
)


# ============================================================
# DESIGN SYSTEM
# ============================================================

st.markdown(
    """
<style>
/* ---------- App canvas ---------- */
.stApp {
    background:
        radial-gradient(circle at 5% 0%, rgba(99,102,241,.12), transparent 25%),
        radial-gradient(circle at 95% 5%, rgba(6,182,212,.10), transparent 23%),
        radial-gradient(circle at 50% 100%, rgba(124,58,237,.08), transparent 28%);
}

.block-container {
    max-width: 1500px;
    padding: 1.1rem 2.3rem 4.5rem;
}

/* Hide Streamlit chrome that adds visual noise */
#MainMenu { visibility: hidden; }
footer { visibility: hidden; }
header { visibility: hidden; }

/* ---------- Top navigation ---------- */
.topbar {
    display:flex;
    align-items:center;
    justify-content:space-between;
    padding:.25rem 0 1.15rem;
    margin-bottom:1.35rem;
    border-bottom:1px solid rgba(148,163,184,.15);
}
.brand {
    display:flex;
    align-items:center;
    gap:.7rem;
}
.brand-icon {
    width:38px;
    height:38px;
    display:flex;
    align-items:center;
    justify-content:center;
    border-radius:12px;
    color:#fff;
    font-size:1.2rem;
    font-weight:900;
    background:linear-gradient(135deg,#6366f1,#06b6d4 75%);
    box-shadow:0 10px 28px rgba(79,70,229,.28);
}
.brand-name {
    font-size:1.08rem;
    font-weight:850;
    letter-spacing:-.025em;
}
.brand-sub {
    font-size:.69rem;
    letter-spacing:.13em;
    text-transform:uppercase;
    opacity:.48;
    margin-left:.35rem;
}
.api-pill {
    display:flex;
    align-items:center;
    gap:.45rem;
    border:1px solid rgba(34,197,94,.23);
    background:rgba(34,197,94,.055);
    padding:.38rem .72rem;
    border-radius:999px;
    font-size:.72rem;
    font-weight:750;
}
.api-dot {
    width:7px;
    height:7px;
    border-radius:50%;
    background:#22c55e;
    box-shadow:0 0 0 4px rgba(34,197,94,.10);
}

/* ---------- Hero ---------- */
.hero {
    position:relative;
    overflow:hidden;
    min-height:315px;
    padding:2.65rem 3rem 2.55rem;
    border:1px solid rgba(148,163,184,.18);
    border-radius:30px;
    background:
        linear-gradient(135deg, rgba(79,70,229,.18), rgba(8,145,178,.08) 48%, rgba(124,58,237,.12)),
        rgba(255,255,255,.018);
    box-shadow:0 28px 80px rgba(15,23,42,.10);
    margin-bottom:1.35rem;
}
.hero:before {
    content:"";
    position:absolute;
    width:420px;
    height:420px;
    right:-150px;
    top:-205px;
    border-radius:50%;
    background:radial-gradient(circle, rgba(99,102,241,.24), rgba(99,102,241,0) 68%);
}
.hero:after {
    content:"";
    position:absolute;
    width:260px;
    height:260px;
    right:20%;
    bottom:-210px;
    border-radius:50%;
    background:radial-gradient(circle, rgba(6,182,212,.15), rgba(6,182,212,0) 68%);
}
.hero-content { position:relative; z-index:2; max-width:900px; }
.eyebrow {
    display:inline-flex;
    align-items:center;
    gap:.45rem;
    padding:.35rem .65rem;
    border:1px solid rgba(99,102,241,.20);
    border-radius:999px;
    background:rgba(99,102,241,.06);
    font-size:.68rem;
    font-weight:800;
    letter-spacing:.12em;
    text-transform:uppercase;
    opacity:.76;
}
.hero h1 {
    margin:.85rem 0 .35rem;
    font-size:clamp(3.2rem,6vw,5.8rem);
    line-height:.9;
    font-weight:900;
    letter-spacing:-.065em;
    background:linear-gradient(90deg,#6366f1 0%,#0891b2 53%,#7c3aed 100%);
    -webkit-background-clip:text;
    background-clip:text;
    color:transparent;
}
.hero-title {
    font-size:1.2rem;
    font-weight:750;
    letter-spacing:-.02em;
}
.hero-copy {
    max-width:800px;
    margin-top:.65rem;
    font-size:.93rem;
    line-height:1.7;
    opacity:.62;
}
.hero-tags {
    display:flex;
    flex-wrap:wrap;
    gap:.45rem;
    margin-top:1.15rem;
}
.hero-tag {
    padding:.32rem .62rem;
    border-radius:999px;
    border:1px solid rgba(148,163,184,.17);
    background:rgba(255,255,255,.035);
    font-size:.68rem;
    font-weight:700;
    opacity:.72;
}

/* ---------- Workflow / input ---------- */
.workflow {
    padding:1.35rem 1.45rem 1.45rem;
    border:1px solid rgba(148,163,184,.17);
    border-radius:22px;
    background:rgba(255,255,255,.025);
    box-shadow:0 15px 45px rgba(15,23,42,.055);
    margin-bottom:1.45rem;
}
.workflow-head {
    display:flex;
    justify-content:space-between;
    align-items:center;
    gap:1rem;
    margin-bottom:1.05rem;
}
.workflow-title { font-size:1rem; font-weight:850; }
.workflow-copy { font-size:.74rem; opacity:.5; margin-top:.18rem; }
.workflow-status {
    font-size:.68rem;
    font-weight:800;
    padding:.35rem .62rem;
    border-radius:999px;
    border:1px solid rgba(148,163,184,.18);
    opacity:.65;
}
.step-line {
    display:flex;
    align-items:center;
    gap:.65rem;
    margin-bottom:.55rem;
}
.step-number {
    width:27px;
    height:27px;
    display:flex;
    align-items:center;
    justify-content:center;
    border-radius:9px;
    color:#fff;
    font-size:.68rem;
    font-weight:900;
    background:linear-gradient(135deg,#6366f1,#0891b2);
}
.step-label { font-size:.83rem; font-weight:800; }
.step-note { font-size:.7rem; opacity:.47; margin-left:.15rem; }

/* Streamlit inputs */
div[data-testid="stTextInput"] > div > div {
    min-height:49px;
    border-radius:13px !important;
    border:1px solid rgba(99,102,241,.28) !important;
    background:rgba(255,255,255,.035) !important;
    box-shadow:0 0 0 3px rgba(99,102,241,.025);
}
div[data-testid="stTextInput"] input {
    font-size:.91rem !important;
}
div[data-testid="stMultiSelect"] > div > div {
    min-height:49px;
    border-radius:13px !important;
    background:rgba(255,255,255,.035) !important;
}
div[data-testid="stMultiSelect"] span[data-baseweb="tag"] {
    border-radius:8px !important;
}

/* ---------- Analysis module selector ---------- */
.module-grid {
    display:grid;
    grid-template-columns:repeat(3,1fr);
    gap:.7rem;
    margin:.35rem 0 .8rem;
}
.module-note {
    margin:.2rem 0 .7rem;
    font-size:.66rem;
    opacity:.46;
}
.module-status {
    display:flex;
    align-items:center;
    justify-content:space-between;
    gap:.8rem;
    padding:.72rem .9rem;
    margin:.25rem 0 .85rem;
    border:1px solid rgba(99,102,241,.16);
    border-radius:13px;
    background:linear-gradient(90deg,rgba(99,102,241,.07),rgba(6,182,212,.035));
}
.module-status-main {
    font-size:.72rem;
    font-weight:800;
}
.module-status-sub {
    font-size:.63rem;
    opacity:.46;
}
div[data-testid="stCheckbox"] {
    padding:.25rem .05rem .3rem;
}
div[data-testid="stCheckbox"] label {
    width:100%;
    padding:.65rem .72rem;
    border:1px solid rgba(148,163,184,.14);
    border-radius:13px;
    background:rgba(255,255,255,.018);
    transition:all .15s ease;
}
div[data-testid="stCheckbox"] label:hover {
    border-color:rgba(99,102,241,.32);
    background:rgba(99,102,241,.045);
}
div[data-testid="stCheckbox"] label p {
    font-size:.76rem !important;
    font-weight:800 !important;
}
@media (max-width:850px) {
    .module-grid { grid-template-columns:1fr; }
}
div[data-testid="stButton"] > button {
    min-height:50px;
    border-radius:13px !important;
    border:0 !important;
    font-weight:850 !important;
    letter-spacing:.01em;
    background:linear-gradient(135deg,#4f46e5,#0891b2) !important;
    box-shadow:0 12px 30px rgba(79,70,229,.23);
    transition:all .16s ease;
}
div[data-testid="stButton"] > button:hover {
    transform:translateY(-2px);
    box-shadow:0 17px 34px rgba(79,70,229,.31);
}

/* ---------- Section system ---------- */
.section-wrap {
    margin-top:2.1rem;
    margin-bottom:.85rem;
}
.section-kicker {
    color:#6366f1;
    font-size:.65rem;
    font-weight:900;
    letter-spacing:.14em;
    text-transform:uppercase;
}
.section-title {
    margin-top:.15rem;
    font-size:1.65rem;
    line-height:1.05;
    font-weight:900;
    letter-spacing:-.035em;
}
.section-description {
    margin-top:.28rem;
    font-size:.78rem;
    opacity:.48;
}
.section-rule {
    height:1px;
    margin-top:.9rem;
    background:linear-gradient(90deg,rgba(99,102,241,.42),rgba(148,163,184,.10),transparent);
}

/* ---------- Repository identity ---------- */
.repo-card {
    display:flex;
    align-items:center;
    gap:1rem;
    padding:1.1rem 1.2rem;
    border:1px solid rgba(148,163,184,.17);
    border-radius:19px;
    background:rgba(255,255,255,.025);
    margin-bottom:1rem;
}
.repo-icon {
    width:48px;
    height:48px;
    flex:0 0 48px;
    display:flex;
    align-items:center;
    justify-content:center;
    border-radius:15px;
    background:linear-gradient(135deg,rgba(99,102,241,.17),rgba(6,182,212,.14));
    border:1px solid rgba(99,102,241,.16);
    font-size:1.25rem;
}
.repo-name { font-size:1.05rem; font-weight:850; letter-spacing:-.02em; }
.repo-desc { margin-top:.22rem; font-size:.76rem; opacity:.52; }
.repo-meta { margin-left:auto; text-align:right; font-size:.68rem; opacity:.5; line-height:1.7; }

/* ---------- Metric cards ---------- */
div[data-testid="stMetric"] {
    min-height:105px;
    padding:1rem 1.05rem !important;
    border:1px solid rgba(148,163,184,.16) !important;
    border-radius:17px !important;
    background:rgba(255,255,255,.028) !important;
    box-shadow:0 9px 28px rgba(15,23,42,.045);
}
div[data-testid="stMetricLabel"] { font-size:.7rem !important; opacity:.54; }
div[data-testid="stMetricValue"] { font-weight:900; letter-spacing:-.045em; }
div[data-testid="stMetricDelta"] { font-size:.68rem; }

/* ---------- Insight cards ---------- */
.insight-grid { display:grid; grid-template-columns:repeat(3,1fr); gap:.75rem; margin:.8rem 0 1.15rem; }
.insight {
    padding:.9rem 1rem;
    border-radius:15px;
    border:1px solid rgba(148,163,184,.15);
    background:rgba(255,255,255,.022);
}
.insight-label { font-size:.62rem; font-weight:850; letter-spacing:.1em; text-transform:uppercase; opacity:.45; }
.insight-value { margin-top:.28rem; font-size:.92rem; font-weight:800; }
.insight-copy { margin-top:.18rem; font-size:.68rem; line-height:1.45; opacity:.48; }

/* ---------- Chart + table presentation ---------- */
.chart-card {
    border:1px solid rgba(148,163,184,.14);
    border-radius:19px;
    padding:.45rem .65rem .1rem;
    background:rgba(255,255,255,.018);
}
.data-caption {
    margin:.25rem 0 .45rem;
    font-size:.68rem;
    font-weight:750;
    letter-spacing:.05em;
    text-transform:uppercase;
    opacity:.42;
}

/* ---------- Expander ---------- */
div[data-testid="stExpander"] {
    border:1px solid rgba(148,163,184,.14) !important;
    border-radius:15px !important;
    background:rgba(255,255,255,.018) !important;
}

/* ---------- Status messages ---------- */
div[data-testid="stAlert"] { border-radius:14px !important; }

/* ---------- Footer ---------- */
.footer {
    margin-top:3.5rem;
    padding-top:1rem;
    border-top:1px solid rgba(148,163,184,.12);
    text-align:center;
    font-size:.67rem;
    opacity:.4;
}

@media (max-width: 850px) {
    .block-container { padding-left:1rem; padding-right:1rem; }
    .hero { padding:2rem 1.4rem; min-height:auto; border-radius:22px; }
    .hero h1 { font-size:3.2rem; }
    .brand-sub { display:none; }
    .repo-meta { display:none; }
    .insight-grid { grid-template-columns:1fr; }
}
</style>
""",
    unsafe_allow_html=True,
)


# ============================================================

st.markdown(
    """
    <style>
    .pulse-panel {
        border:1px solid rgba(148,163,184,.15);
        border-radius:18px;
        padding:1rem 1.05rem;
        background:rgba(255,255,255,.022);
        margin:.85rem 0 1.1rem;
    }
    .pulse-head { display:flex; align-items:center; justify-content:space-between; gap:1rem; margin-bottom:.75rem; }
    .pulse-title { font-size:.78rem; font-weight:850; }
    .pulse-note { font-size:.62rem; opacity:.42; }
    .pulse-grid { display:grid; grid-template-columns:repeat(4,1fr); gap:.6rem; }
    .pulse-item { padding:.75rem .8rem; border:1px solid rgba(148,163,184,.14); border-radius:13px; background:rgba(255,255,255,.018); }
    .pulse-label { font-size:.56rem; font-weight:850; letter-spacing:.09em; text-transform:uppercase; opacity:.43; }
    .pulse-value { margin-top:.24rem; font-size:1rem; font-weight:900; letter-spacing:-.025em; }
    .pulse-sub { margin-top:.12rem; font-size:.59rem; opacity:.48; }
    .repo-meta-line { margin:.65rem 0 1rem; font-size:.67rem; line-height:1.65; opacity:.48; }
    @media (max-width:850px) { .pulse-grid { grid-template-columns:repeat(2,1fr); } }
    </style>
    """,
    unsafe_allow_html=True,
)
# HELPERS
# ============================================================

def parse_github_url(url):
    pattern = r"https?://github\.com/([^/\s]+)/([^/\s]+?)/?$"
    match = re.match(pattern, url.strip())
    if not match:
        return None, None
    return match.group(1), match.group(2)


def format_percentage(value):
    return f"{value:.2f}%"


def section_header(number, title, description):
    st.markdown(
        f"""
        <div class="section-wrap">
            <div class="section-kicker">{number:02d} / Analysis module</div>
            <div class="section-title">{title}</div>
            <div class="section-description">{description}</div>
            <div class="section-rule"></div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def insight_card(label, value, copy):
    # Keep each card as one continuous HTML block. Blank lines inside
    # Streamlit's Markdown HTML can cause later cards to render as raw text.
    return (
        f'<div class="insight">'
        f'<div class="insight-label">{label}</div>'
        f'<div class="insight-value">{value}</div>'
        f'<div class="insight-copy">{copy}</div>'
        f'</div>'
    )


def plot_layout(figure, title=None):
    figure.update_layout(
        title=title,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=10, r=10, t=48 if title else 15, b=10),
        font=dict(size=12),
        legend=dict(bgcolor="rgba(0,0,0,0)"),
        hoverlabel=dict(bordercolor="rgba(148,163,184,.25)"),
    )
    return figure


def show_dataframe(df, label="View analyzed data"):
    with st.expander(label, expanded=False):
        st.dataframe(df, width="stretch", hide_index=True)


# ============================================================

def esc(value):
    return html.escape(str(value))


def pct(value):
    return f"{float(value):.2f}%"


def safe_metric(value, fallback="—"):
    if value is None or value == "":
        return fallback
    return value


def pulse_item(label, value, sub=""):
    return f"""
    <div class="pulse-item">
        <div class="pulse-label">{esc(label)}</div>
        <div class="pulse-value">{esc(value)}</div>
        <div class="pulse-sub">{esc(sub)}</div>
    </div>
    """


def pulse_panel(items, note="Based on the selected analysis modules"):
    cells = "".join(pulse_item(*item) for item in items)
    st.markdown(
        f"""
        <div class="pulse-panel">
            <div class="pulse-head">
                <div class="pulse-title">Repository pulse</div>
                <div class="pulse-note">{esc(note)}</div>
            </div>
            <div class="pulse-grid">{cells}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def styled_chart(fig, title=None, height=380):
    fig.update_layout(
        title=None,
        height=height,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=12, r=12, t=18 if not title else 42, b=12),
        font=dict(size=11),
        hoverlabel=dict(bordercolor="rgba(148,163,184,.22)", bgcolor="rgba(22,27,34,.98)"),
        legend=dict(bgcolor="rgba(0,0,0,0)"),
        xaxis=dict(gridcolor="rgba(148,163,184,.10)", zerolinecolor="rgba(148,163,184,.12)"),
        yaxis=dict(gridcolor="rgba(148,163,184,.10)", zerolinecolor="rgba(148,163,184,.12)"),
    )
    if title:
        fig.add_annotation(
            x=0, y=1.08, xref="paper", yref="paper",
            text=esc(title), showarrow=False, xanchor="left",
            font=dict(size=13),
        )
    return fig


def donut_chart(df, names, values, title):
    fig = px.pie(df, names=names, values=values, hole=.72)
    fig.update_traces(
        textposition="inside",
        textinfo="percent",
        textfont=dict(size=12),
        marker=dict(line=dict(width=2, color="rgba(15,23,42,.65)")),
        hovertemplate="%{label}<br>%{value} records · %{percent}<extra></extra>",
    )
    fig.update_layout(
        showlegend=True,
        legend=dict(
            orientation="v",
            yanchor="middle",
            y=0.5,
            xanchor="left",
            x=1.02,
            font=dict(size=10),
        ),
    )
    fig.add_annotation(
        x=.5, y=.5, xref="paper", yref="paper",
        text="<b>Distribution</b>",
        showarrow=False,
        font=dict(size=12),
    )
    return styled_chart(fig, title, 310)
# TOP BAR + HERO
# ============================================================

st.markdown(
    """
    <div class="topbar">
        <div class="brand">
            <div class="brand-icon">◈</div>
            <div class="brand-name">GitScope <span class="brand-sub">Open-source analytics</span></div>
        </div>
        <div class="api-pill"><span class="api-dot"></span> GitHub REST API</div>
    </div>

    <section class="hero">
        <div class="hero-content">
            <div class="eyebrow">Repository intelligence · Collaboration · Activity</div>
            <h1>GitScope</h1>
            <div class="hero-title">GitHub Repository Activity &amp; Collaboration Analyzer</div>
            <div class="hero-copy">
                Turn a public GitHub repository into a focused analytical workspace.
                Explore development activity, contributor behavior, issues, pull requests,
                languages, releases and derived collaboration signals — all from one dashboard.
            </div>
            <div class="hero-tags">
                <span class="hero-tag">Python</span>
                <span class="hero-tag">Pandas</span>
                <span class="hero-tag">NumPy</span>
                <span class="hero-tag">Plotly</span>
                <span class="hero-tag">GitHub REST API</span>
                <span class="hero-tag">Docker-ready</span>
            </div>
        </div>
    </section>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# INPUT WORKFLOW
# ============================================================

st.markdown(
    """
    <div class="workflow">
        <div class="workflow-head">
            <div>
                <div class="workflow-title">Build your repository analysis</div>
                <div class="workflow-copy">Select the analysis modules you need — GitScope fetches only those datasets and keeps the dashboard focused.</div>
            </div>
            <div class="workflow-status">LIVE ANALYSIS</div>
        </div>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    '<div class="step-line"><div class="step-number">01</div><div class="step-label">Repository</div><div class="step-note">Public GitHub URL</div></div>',
    unsafe_allow_html=True,
)

repository_url = st.text_input(
    "GitHub Repository URL",
    placeholder="https://github.com/owner/repository",
    label_visibility="collapsed",
)

st.markdown(
    '<div style="height:.85rem"></div><div class="step-line"><div class="step-number">02</div><div class="step-label">Analysis modules</div><div class="step-note">Select one or more</div></div>',
    unsafe_allow_html=True,
)

analysis_options = [
    "Commits",
    "Contributors",
    "Issues",
    "Pull Requests",
    "Languages",
    "Releases",
]

# Persistent selection cards: avoids the misleading "No results" state
# that Streamlit multiselect shows when every option is selected.
slug_map = {
    "Commits": "commits",
    "Contributors": "contributors",
    "Issues": "issues",
    "Pull Requests": "pull_requests",
    "Languages": "languages",
    "Releases": "releases",
}

if "analysis_selection_initialized" not in st.session_state:
    for name in analysis_options:
        st.session_state[f"analysis_{slug_map[name]}"] = False
    st.session_state["analysis_selection_initialized"] = True

control_cols = st.columns([1, 1, 6])
with control_cols[0]:
    if st.button("Select all", key="select_all_analyses", width="stretch"):
        for name in analysis_options:
            st.session_state[f"analysis_{slug_map[name]}"] = True
        st.rerun()
with control_cols[1]:
    if st.button("Clear", key="clear_all_analyses", width="stretch"):
        for name in analysis_options:
            st.session_state[f"analysis_{slug_map[name]}"] = False
        st.rerun()

help_text = {
    "Commits": "Commit volume and activity trends",
    "Contributors": "Contributor activity and concentration",
    "Issues": "Open/closed issue activity",
    "Pull Requests": "PR status and merge activity",
    "Languages": "Repository language composition",
    "Releases": "Release history and latest release",
}

module_status_placeholder = st.empty()

checkbox_cols = st.columns(3)
for index, name in enumerate(analysis_options):
    with checkbox_cols[index % 3]:
        st.checkbox(
            name,
            key=f"analysis_{slug_map[name]}",
            help=help_text[name],
        )

selected_analyses = [
    name for name in analysis_options
    if st.session_state[f"analysis_{slug_map[name]}"]
]
selected_set = set(selected_analyses)

if selected_analyses:
    selected_label = " · ".join(selected_analyses)
    module_status_placeholder.markdown(
        f'''
        <div class="module-status">
            <div>
                <div class="module-status-main">{len(selected_analyses)} analysis module{"s" if len(selected_analyses) != 1 else ""} selected</div>
                <div class="module-status-sub">{esc(selected_label)}</div>
            </div>
            <div class="module-status-sub">Only selected data will be fetched</div>
        </div>
        ''',
        unsafe_allow_html=True,
    )
else:
    module_status_placeholder.markdown(
        '''
        <div class="module-status">
            <div>
                <div class="module-status-main">No analysis modules selected</div>
                <div class="module-status-sub">Select at least one module to continue</div>
            </div>
            <div class="module-status-sub">Ready</div>
        </div>
        ''',
        unsafe_allow_html=True,
    )

st.markdown('<div style="height:.15rem"></div>', unsafe_allow_html=True)
analyze_button = st.button("Analyze Repository  →", type="primary", width="stretch")

st.markdown('</div>', unsafe_allow_html=True)

if selected_analyses:
    labels = "  ·  ".join(selected_analyses)
    st.markdown(
        f'<div style="margin:.65rem 0 0;text-align:center;font-size:.68rem;opacity:.48;">'
        f'<b>{len(selected_analyses)} modules selected</b>&nbsp;&nbsp; {labels}</div>',
        unsafe_allow_html=True,
    )


# ============================================================
# RUN ANALYSIS
# ============================================================

if analyze_button:
    if not repository_url.strip():
        st.error("Please enter a GitHub repository URL.")
        st.stop()

    owner, repo = parse_github_url(repository_url)

    if not owner or not repo:
        st.error("Invalid GitHub repository URL. Use: https://github.com/owner/repository")
        st.stop()

    if not selected_analyses:
        st.warning("Please select at least one analysis module.")
        st.stop()

    try:
        with st.spinner("Fetching repository data from GitHub and building your insights…"):
            analysis = analyze_repository(owner, repo, selected_analyses)
    except Exception as error:
        st.error(f"Unable to analyze repository: {error}")
        st.stop()

    repository = analysis["repository"]
    full_name = repository.get("full_name", f"{owner}/{repo}")
    description = repository.get("description") or "No repository description available."
    default_branch = repository.get("default_branch", "N/A")
    language = repository.get("language") or "N/A"
    topics = repository.get("topics") or []
    updated_at = repository.get("updated_at") or "N/A"
    license_info = repository.get("license") or {}
    license_name = (
        license_info.get("spdx_id") or license_info.get("name") or "N/A"
        if isinstance(license_info, dict) else "N/A"
    )

    st.success(f"Analysis complete for {full_name}")

    section_header(
        1,
        "Repository overview",
        "Essential repository information stays visible before the deeper insight modules.",
    )

    st.markdown(
        f"""
        <div class="repo-card">
            <div class="repo-icon">⌘</div>
            <div>
                <div class="repo-name">{esc(full_name)}</div>
                <div class="repo-desc">{esc(description)}</div>
            </div>
            <div class="repo-meta">
                <div>Default branch · <b>{esc(default_branch)}</b></div>
                <div>Primary language · <b>{esc(language)}</b></div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    o1, o2, o3, o4, o5 = st.columns(5)
    with o1: st.metric("Stars", repository.get("stargazers_count", 0))
    with o2: st.metric("Forks", repository.get("forks_count", 0))
    with o3: st.metric("Open issues", repository.get("open_issues_count", 0))
    with o4: st.metric("Primary language", language)
    with o5: st.metric("Default branch", default_branch)

    meta_bits = [
        f"Updated: {updated_at}",
        f"License: {license_name}",
        f"Owner: {owner}",
    ]
    if topics:
        meta_bits.append("Topics: " + ", ".join(str(x) for x in topics[:6]))
    st.markdown(
        f'<div class="repo-meta-line">{esc(" · ".join(meta_bits))}</div>',
        unsafe_allow_html=True,
    )

    pulse_items = []
    if "Commits" in selected_set:
        cm, tr = analysis["commit_metrics"], analysis["commit_activity_trend"]
        pulse_items.append(("Commits", f"{cm['total_commits']:,}", f"{tr['active_days']} active days"))
    if "Contributors" in selected_set:
        con, cc = analysis["contributor_metrics"], analysis["contributor_concentration"]
        pulse_items.append(("Contributors", f"{con['total_contributors']:,}", f"Top 1: {pct(cc['top_contributor_concentration'])}"))
    if "Issues" in selected_set:
        im = analysis["issue_metrics"]
        pulse_items.append(("Issues", f"{im['total_issues']:,}", f"{im['open_issues']:,} open"))
    if "Pull Requests" in selected_set:
        pm = analysis["pull_request_metrics"]
        pulse_items.append(("Pull requests", f"{pm['total_pull_requests']:,}", f"{pm['merged_pull_requests']:,} merged"))
    if "Languages" in selected_set:
        ldf = analysis["languages"]
        if not ldf.empty:
            pulse_items.append(("Languages", f"{len(ldf):,}", f"Top: {ldf.iloc[0]['language']}"))
    if "Releases" in selected_set:
        rm = analysis["release_metrics"]
        pulse_items.append(("Releases", f"{rm['total_releases']:,}", f"Latest: {rm['latest_release']}"))
    if pulse_items:
        pulse_panel(pulse_items[:4], "Descriptive snapshot based on selected modules")

    # COMMITS
    if "Commits" in selected_set:
        section_header(2, "Commit activity", "Development activity over the analyzed commit window, inspired by GitHub's commit-frequency view.")
        metrics = analysis["commit_metrics"]
        trend = analysis["commit_activity_trend"]
        commits_df = analysis["commits"]

        c1, c2, c3, c4 = st.columns(4)
        with c1: st.metric("Commits analyzed", metrics["total_commits"])
        with c2: st.metric("Unique contributors", metrics["unique_contributors"])
        with c3: st.metric("Average / active day", f"{metrics['average_commits_per_day']:.2f}")
        with c4: st.metric("Most active day", trend["most_active_day_commits"])

        if not commits_df.empty:
            daily = commits_df.groupby("day").size().reset_index(name="commits")
            daily["day"] = daily["day"].astype(str)
            fig = px.area(daily, x="day", y="commits")
            fig.update_traces(
                line=dict(color="#6366f1", width=2),
                fillcolor="rgba(99,102,241,.16)",
                hovertemplate="%{x}<br>%{y} commits<extra></extra>",
            )
            fig.update_xaxes(type="category", nticks=10)
            st.plotly_chart(styled_chart(fig, "Commit activity by day", 390), width="stretch", config={"displayModeBar": False})
            st.markdown(
                '<div class="insight-grid">'
                + insight_card("First returned commit", trend["first_commit_date"], "Earliest commit in the analyzed window.")
                + insight_card("Latest returned commit", trend["latest_commit_date"], "Most recent commit in the analyzed window.")
                + insight_card("Peak day", trend["most_active_day"], f"{trend['most_active_day_commits']} commits on that day.")
                + '</div>',
                unsafe_allow_html=True,
            )
            show_dataframe(commits_df, f"View {len(commits_df):,} analyzed commits")
        else:
            st.info("No commit data available.")

    # CONTRIBUTORS
    if "Contributors" in selected_set:
        section_header(3, "Contributor activity", "Contribution distribution and concentration, inspired by the contributor views in GitHub Insights.")
        metrics = analysis["contributor_metrics"]
        concentration = analysis["contributor_concentration"]
        contributors_df = analysis["contributors"]

        c1, c2, c3, c4 = st.columns(4)
        with c1: st.metric("Contributors analyzed", metrics["total_contributors"])
        with c2: st.metric("Top contributor", metrics["top_contributor"])
        with c3: st.metric("Top 1 share", pct(concentration["top_contributor_concentration"]))
        with c4: st.metric("Top 3 share", pct(concentration["top_3_contributor_concentration"]))

        if not contributors_df.empty:
            chart_df = contributors_df.head(15).copy().sort_values("contributions")
            chart_df["share"] = chart_df["contributions"] / contributors_df["contributions"].sum() * 100
            fig = px.bar(chart_df, x="contributions", y="username", orientation="h", custom_data=["share"])
            fig.update_traces(
                marker_color="#0891b2",
                hovertemplate="%{y}<br>%{x} contributions · %{customdata[0]:.2f}%<extra></extra>",
            )
            fig.update_yaxes(title=None)
            fig.update_xaxes(title="Contributions")
            st.plotly_chart(styled_chart(fig, "Top contributors", 430), width="stretch", config={"displayModeBar": False})
            st.markdown(
                '<div class="insight-grid">'
                + insight_card("Top 1", pct(concentration["top_contributor_concentration"]), "Share attributed to the leading analyzed contributor.")
                + insight_card("Top 3", pct(concentration["top_3_contributor_concentration"]), "Combined share attributed to the three leading contributors.")
                + insight_card("Interpretation", "Contribution spread", "A descriptive concentration signal, not a health score.")
                + '</div>',
                unsafe_allow_html=True,
            )
            show_dataframe(contributors_df, f"View {len(contributors_df):,} analyzed contributors")
        else:
            st.info("No contributor data available.")

    # ISSUES
    if "Issues" in selected_set:
        section_header(4, "Issue activity", "Compare open and closed issue activity in the analyzed issue sample.")
        metrics = analysis["issue_metrics"]
        issues_df = analysis["issues"]

        c1, c2, c3, c4 = st.columns(4)
        with c1: st.metric("Issues analyzed", metrics["total_issues"])
        with c2: st.metric("Open", metrics["open_issues"])
        with c3: st.metric("Closed", metrics["closed_issues"])
        with c4: st.metric("Closure rate", pct(metrics["closure_rate"]))

        if not issues_df.empty:
            counts = issues_df["state"].value_counts().reset_index()
            counts.columns = ["state", "count"]

            chart_col, detail_col = st.columns([1.25, .75], gap="large")
            with chart_col:
                st.plotly_chart(
                    donut_chart(counts, "state", "count", "Issue status distribution"),
                    width="stretch",
                    config={"displayModeBar": False},
                )
            with detail_col:
                st.markdown('<div class="data-caption">Status breakdown</div>', unsafe_allow_html=True)
                for _, row in counts.iterrows():
                    label = str(row["state"]).title()
                    count = int(row["count"])
                    share = (count / len(issues_df) * 100) if len(issues_df) else 0
                    st.markdown(
                        f'''
                        <div class="pulse-item" style="margin-bottom:.55rem">
                            <div class="pulse-label">{esc(label)}</div>
                            <div class="pulse-value">{count:,}</div>
                            <div class="pulse-sub">{share:.1f}% of analyzed issues</div>
                        </div>
                        ''',
                        unsafe_allow_html=True,
                    )
                st.caption("The chart and counts describe the analyzed issue sample.")
            show_dataframe(issues_df, f"View {len(issues_df):,} analyzed issues")
        else:
            st.info("No issue data available.")

    # PULL REQUESTS
    if "Pull Requests" in selected_set:
        section_header(5, "Pull request activity", "Inspect open, closed and merged pull-request activity in the analyzed sample.")
        metrics = analysis["pull_request_metrics"]
        prs_df = analysis["pull_requests"]

        c1, c2, c3, c4 = st.columns(4)
        with c1: st.metric("PRs analyzed", metrics["total_pull_requests"])
        with c2: st.metric("Open PRs", metrics["open_pull_requests"])
        with c3: st.metric("Merged PRs", metrics["merged_pull_requests"])
        with c4: st.metric("Merge rate", pct(metrics["merge_rate"]))

        if not prs_df.empty:
            counts = prs_df["state"].value_counts().reset_index()
            counts.columns = ["state", "count"]

            chart_col, detail_col = st.columns([1.25, .75], gap="large")
            with chart_col:
                st.plotly_chart(
                    donut_chart(counts, "state", "count", "Pull request status distribution"),
                    width="stretch",
                    config={"displayModeBar": False},
                )
            with detail_col:
                st.markdown('<div class="data-caption">Status breakdown</div>', unsafe_allow_html=True)
                for _, row in counts.iterrows():
                    label = str(row["state"]).title()
                    count = int(row["count"])
                    share = (count / len(prs_df) * 100) if len(prs_df) else 0
                    st.markdown(
                        f'''
                        <div class="pulse-item" style="margin-bottom:.55rem">
                            <div class="pulse-label">{esc(label)}</div>
                            <div class="pulse-value">{count:,}</div>
                            <div class="pulse-sub">{share:.1f}% of analyzed PRs</div>
                        </div>
                        ''',
                        unsafe_allow_html=True,
                    )
                st.caption("Merged PRs are a subset of closed PRs in the analyzed sample.")
            show_dataframe(prs_df, f"View {len(prs_df):,} analyzed pull requests")
        else:
            st.info("No pull request data available.")

    # LANGUAGES
    if "Languages" in selected_set:
        section_header(6, "Programming languages", "Explore the language composition returned by the GitHub repository API.")
        languages_df = analysis["languages"]

        if not languages_df.empty:
            l1, l2 = st.columns([1.25, 1])
            with l1:
                chart_df = languages_df.head(10).sort_values("percentage")
                fig = px.bar(chart_df, x="percentage", y="language", orientation="h")
                fig.update_traces(marker_color="#7c3aed", hovertemplate="%{y}<br>%{x:.2f}%<extra></extra>")
                fig.update_xaxes(title="Share (%)")
                fig.update_yaxes(title=None)
                st.plotly_chart(styled_chart(fig, "Language composition", 390), width="stretch", config={"displayModeBar": False})
            with l2:
                fig = px.pie(languages_df.head(8), names="language", values="percentage", hole=.68)
                fig.update_traces(textposition="inside", textinfo="percent", hovertemplate="%{label}<br>%{value:.2f}%<extra></extra>")
                st.plotly_chart(styled_chart(fig, "Language mix", 390), width="stretch", config={"displayModeBar": False})
            show_dataframe(languages_df, f"View {len(languages_df):,} analyzed languages")
        else:
            st.info("No language data available.")

    # RELEASES
    if "Releases" in selected_set:
        section_header(7, "Release activity", "Review release volume, latest release and the release timeline returned by the repository API.")
        metrics = analysis["release_metrics"]
        releases_df = analysis["releases"]

        c1, c2, c3 = st.columns(3)
        with c1: st.metric("Releases analyzed", metrics["total_releases"])
        with c2: st.metric("Latest release", safe_metric(metrics["latest_release"]))
        with c3: st.metric("Release records", len(releases_df))

        if not releases_df.empty:
            date_col = next((col for col in ["published_at", "created_at"] if col in releases_df.columns), None)
            if date_col:
                release_chart = releases_df.copy()
                release_chart[date_col] = release_chart[date_col].astype(str)
                release_chart = release_chart.sort_values(date_col)
                release_chart["release_count"] = range(1, len(release_chart) + 1)
                hover_cols = [c for c in ["name", "tag_name"] if c in release_chart.columns]
                fig = px.scatter(release_chart, x=date_col, y="release_count", hover_data=hover_cols)
                fig.update_traces(marker=dict(color="#d29922", size=8))
                fig.update_yaxes(title="Cumulative releases")
                fig.update_xaxes(title=None, type="category", nticks=10)
                st.plotly_chart(styled_chart(fig, "Release timeline", 350), width="stretch", config={"displayModeBar": False})
            show_dataframe(releases_df, f"View {len(releases_df):,} analyzed releases")
        else:
            st.info("No release data available.")
    # FOOTER
    # ========================================================

    st.markdown(
        """
        <div class="footer">
            GitScope · GitHub Repository Activity &amp; Collaboration Analyzer ·
            Built with Python, Pandas, Plotly, Streamlit &amp; the GitHub REST API
        </div>
        """,
        unsafe_allow_html=True,
    )
