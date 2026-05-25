import streamlit as st
import time
from pipeline import run_research_pipeline

# ── Page config ────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="ResearchMind · Multi-Agent Research",
    page_icon="🔬",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ── Custom CSS ─────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Mono:wght@300;400;500&family=DM+Sans:wght@300;400;500&display=swap');

/* ── Root variables ── */
:root {
    --bg:        #0a0c10;
    --surface:   #111318;
    --border:    #1e2230;
    --accent:    #5fffb0;
    --accent2:   #3d8aff;
    --accent3:   #ff6b6b;
    --accent4:   #ffd166;
    --text:      #e8eaf0;
    --muted:     #5a6070;
    --radius:    12px;
}

/* ── Global reset ── */
html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
    background-color: var(--bg) !important;
    color: var(--text) !important;
}

.stApp { background-color: var(--bg) !important; }

/* Hide Streamlit chrome */
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding: 2.5rem 3rem 4rem !important; max-width: 1200px; }

/* ── Hero header ── */
.hero {
    display: flex;
    flex-direction: column;
    align-items: center;
    text-align: center;
    padding: 3rem 0 2.5rem;
    position: relative;
}
.hero-badge {
    font-family: 'DM Mono', monospace;
    font-size: 0.7rem;
    letter-spacing: 0.2em;
    text-transform: uppercase;
    color: var(--accent);
    background: rgba(95,255,176,0.08);
    border: 1px solid rgba(95,255,176,0.2);
    border-radius: 99px;
    padding: 0.3rem 1rem;
    margin-bottom: 1.2rem;
}
.hero-title {
    font-family: 'Syne', sans-serif;
    font-size: clamp(2.8rem, 5vw, 4.5rem);
    font-weight: 800;
    line-height: 1.05;
    letter-spacing: -0.02em;
    margin: 0 0 1rem;
    background: linear-gradient(135deg, #e8eaf0 0%, #5fffb0 50%, #3d8aff 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}
.hero-sub {
    font-size: 1.05rem;
    color: var(--muted);
    max-width: 520px;
    line-height: 1.65;
    margin: 0 auto 2.5rem;
}

/* ── Search bar ── */
div[data-testid="stTextInput"] input {
    background: var(--surface) !important;
    border: 1.5px solid var(--border) !important;
    border-radius: var(--radius) !important;
    color: var(--text) !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 1.05rem !important;
    padding: 0.85rem 1.2rem !important;
    transition: border-color 0.2s;
}
div[data-testid="stTextInput"] input:focus {
    border-color: var(--accent) !important;
    box-shadow: 0 0 0 3px rgba(95,255,176,0.1) !important;
    outline: none !important;
}
div[data-testid="stTextInput"] label {
    color: var(--muted) !important;
    font-family: 'DM Mono', monospace !important;
    font-size: 0.72rem !important;
    letter-spacing: 0.1em !important;
    text-transform: uppercase !important;
}

/* ── Primary button ── */
div[data-testid="stButton"] > button {
    background: var(--accent) !important;
    color: #0a0c10 !important;
    font-family: 'Syne', sans-serif !important;
    font-weight: 700 !important;
    font-size: 0.95rem !important;
    letter-spacing: 0.03em !important;
    border: none !important;
    border-radius: var(--radius) !important;
    padding: 0.75rem 2.5rem !important;
    cursor: pointer !important;
    transition: all 0.2s ease !important;
    width: 100% !important;
}
div[data-testid="stButton"] > button:hover {
    background: #4de89a !important;
    transform: translateY(-1px) !important;
    box-shadow: 0 6px 24px rgba(95,255,176,0.25) !important;
}
div[data-testid="stButton"] > button:disabled {
    opacity: 0.4 !important;
    transform: none !important;
}

/* ── Pipeline steps ── */
.pipeline-track {
    display: flex;
    justify-content: center;
    align-items: center;
    gap: 0;
    margin: 2rem auto 2.5rem;
    max-width: 700px;
}
.step-node {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 0.5rem;
    flex: 1;
    position: relative;
}
.step-node:not(:last-child)::after {
    content: '';
    position: absolute;
    top: 18px;
    left: calc(50% + 20px);
    right: calc(-50% + 20px);
    height: 1px;
    background: var(--border);
    transition: background 0.4s;
}
.step-node.done:not(:last-child)::after { background: var(--accent); }
.step-node.active:not(:last-child)::after { background: var(--border); }

.step-icon {
    width: 36px; height: 36px;
    border-radius: 50%;
    display: flex; align-items: center; justify-content: center;
    font-size: 1rem;
    border: 1.5px solid var(--border);
    background: var(--surface);
    transition: all 0.3s;
    position: relative;
    z-index: 1;
}
.step-icon.done { border-color: var(--accent); background: rgba(95,255,176,0.15); }
.step-icon.active {
    border-color: var(--accent2);
    background: rgba(61,138,255,0.15);
    box-shadow: 0 0 16px rgba(61,138,255,0.3);
    animation: pulse 1.5s ease-in-out infinite;
}
@keyframes pulse {
    0%, 100% { box-shadow: 0 0 16px rgba(61,138,255,0.3); }
    50%       { box-shadow: 0 0 28px rgba(61,138,255,0.6); }
}
.step-label {
    font-family: 'DM Mono', monospace;
    font-size: 0.65rem;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    color: var(--muted);
    text-align: center;
}
.step-label.active { color: var(--accent2); }
.step-label.done   { color: var(--accent); }

/* ── Result cards ── */
.result-card {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 16px;
    padding: 1.6rem 1.8rem;
    margin-bottom: 1.2rem;
    position: relative;
    overflow: hidden;
    transition: border-color 0.2s;
}
.result-card:hover { border-color: #2a3040; }
.result-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 2px;
}
.card-search::before  { background: linear-gradient(90deg, var(--accent2), transparent); }
.card-scrape::before  { background: linear-gradient(90deg, var(--accent4), transparent); }
.card-report::before  { background: linear-gradient(90deg, var(--accent), transparent); }
.card-critic::before  { background: linear-gradient(90deg, var(--accent3), transparent); }

.card-header {
    display: flex;
    align-items: center;
    gap: 0.75rem;
    margin-bottom: 1rem;
}
.card-icon {
    font-size: 1.2rem;
    width: 36px; height: 36px;
    display: flex; align-items: center; justify-content: center;
    border-radius: 8px;
    background: rgba(255,255,255,0.04);
}
.card-title {
    font-family: 'Syne', sans-serif;
    font-weight: 700;
    font-size: 0.95rem;
    margin: 0;
    letter-spacing: 0.01em;
}
.card-meta {
    font-family: 'DM Mono', monospace;
    font-size: 0.68rem;
    color: var(--muted);
    margin-left: auto;
}
.card-body {
    font-size: 0.92rem;
    line-height: 1.75;
    color: #b0b8cc;
    white-space: pre-wrap;
    word-break: break-word;
}

/* ── Expander override ── */
details > summary {
    font-family: 'DM Mono', monospace !important;
    font-size: 0.75rem !important;
    color: var(--muted) !important;
    letter-spacing: 0.08em !important;
    text-transform: uppercase !important;
    cursor: pointer !important;
    padding: 0.5rem 0 !important;
}
details > summary:hover { color: var(--text) !important; }

/* ── Status / alerts ── */
div[data-testid="stAlert"] {
    background: rgba(95,255,176,0.06) !important;
    border: 1px solid rgba(95,255,176,0.2) !important;
    border-radius: var(--radius) !important;
    color: var(--accent) !important;
    font-family: 'DM Mono', monospace !important;
    font-size: 0.8rem !important;
}

/* ── Spinner ── */
div[data-testid="stSpinner"] > div {
    border-top-color: var(--accent) !important;
}

/* ── Divider ── */
hr { border-color: var(--border) !important; margin: 2rem 0 !important; }

/* ── Scrollbar ── */
::-webkit-scrollbar { width: 6px; }
::-webkit-scrollbar-track { background: var(--bg); }
::-webkit-scrollbar-thumb { background: var(--border); border-radius: 3px; }
::-webkit-scrollbar-thumb:hover { background: var(--muted); }

/* ── Success flash ── */
.success-banner {
    background: rgba(95,255,176,0.07);
    border: 1px solid rgba(95,255,176,0.25);
    border-radius: var(--radius);
    padding: 1rem 1.4rem;
    display: flex;
    align-items: center;
    gap: 0.75rem;
    margin-bottom: 1.8rem;
}
.success-banner span {
    font-family: 'DM Mono', monospace;
    font-size: 0.8rem;
    color: var(--accent);
    letter-spacing: 0.05em;
}

/* ── Sidebar styling ── */
section[data-testid="stSidebar"] {
    background: var(--surface) !important;
    border-right: 1px solid var(--border) !important;
}
</style>
""", unsafe_allow_html=True)


# ── Session state ──────────────────────────────────────────────────────────────
if "results"      not in st.session_state: st.session_state.results      = None
if "running"      not in st.session_state: st.session_state.running      = False
if "current_step" not in st.session_state: st.session_state.current_step = 0
if "error"        not in st.session_state: st.session_state.error        = None
if "history"      not in st.session_state: st.session_state.history      = []


# ── Hero ───────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero">
    <div class="hero-badge">⬡ Multi-Agent Research System</div>
    <h1 class="hero-title">ResearchMind</h1>
    <p class="hero-sub">
        Four specialized agents work in sequence — searching, scraping,
        writing, and critiquing — to produce a polished research report
        on any topic in seconds.
    </p>
</div>
""", unsafe_allow_html=True)


# ── Pipeline visualiser ────────────────────────────────────────────────────────
STEPS = [
    ("🔍", "Search"),
    ("📄", "Scrape"),
    ("✍️", "Write"),
    ("🎯", "Critique"),
]

def render_pipeline(active: int, done_up_to: int):
    nodes = ""
    for i, (icon, label) in enumerate(STEPS):
        if i < done_up_to:
            cls = "done"
        elif i == active:
            cls = "active"
        else:
            cls = ""
        nodes += f"""
        <div class="step-node {cls}">
            <div class="step-icon {cls}">{icon}</div>
            <div class="step-label {cls}">{label}</div>
        </div>"""
    st.markdown(f'<div class="pipeline-track">{nodes}</div>', unsafe_allow_html=True)


# ── Input area ─────────────────────────────────────────────────────────────────
col_input, col_btn = st.columns([5, 1], gap="medium")

with col_input:
    topic = st.text_input(
        "Research topic",
        placeholder="e.g.  Quantum computing breakthroughs in 2025",
        label_visibility="collapsed",
        disabled=st.session_state.running,
    )

with col_btn:
    run_btn = st.button(
        "Research →" if not st.session_state.running else "Running…",
        disabled=st.session_state.running or not topic.strip(),
        use_container_width=True,
    )

st.markdown("<div style='height:0.5rem'></div>", unsafe_allow_html=True)


# ── Pipeline execution ─────────────────────────────────────────────────────────
if run_btn and topic.strip():
    st.session_state.running      = True
    st.session_state.results      = None
    st.session_state.error        = None
    st.session_state.current_step = 0

    # Step tracker placeholders
    pipeline_ph  = st.empty()
    status_ph    = st.empty()
    progress_ph  = st.empty()

    pipeline_ph.markdown(
        '<div style="margin-bottom:0.5rem"></div>', unsafe_allow_html=True
    )

    step_labels = [
        "🔍  Search agent is gathering sources…",
        "📄  Reader agent is scraping top pages…",
        "✍️  Writer agent is drafting the report…",
        "🎯  Critic agent is reviewing the report…",
    ]

    try:
        # We run the pipeline but hook into it stage by stage via a wrapper
        # that patches progress into session state.
        state = {}
        from agents import build_reader_agent, build_search_agent, writer_chain, critic_chain

        # ── Step 1 · Search ──
        st.session_state.current_step = 0
        with pipeline_ph.container():
            render_pipeline(active=0, done_up_to=0)
        status_ph.info(step_labels[0])

        search_agent  = build_search_agent()
        search_result = search_agent.invoke({
            "messages": [("user",
                f"Find recent, reliable and detailed information about: {topic}"
            )]
        })
        state["search_results"] = search_result["messages"][-1].content

        # ── Step 2 · Scrape ──
        with pipeline_ph.container():
            render_pipeline(active=1, done_up_to=1)
        status_ph.info(step_labels[1])

        reader_agent  = build_reader_agent()
        reader_result = reader_agent.invoke({
            "messages": [("user",
                f"Based on the following search results about '{topic}', "
                f"pick the most relevant URL and scrape it for deeper content.\n\n"
                f"Search Results:\n{state['search_results'][:800]}"
            )]
        })
        state["scraped_content"] = reader_result["messages"][-1].content

        # ── Step 3 · Write ──
        with pipeline_ph.container():
            render_pipeline(active=2, done_up_to=2)
        status_ph.info(step_labels[2])

        research_combined = (
            f"SEARCH RESULTS:\n{state['search_results']}\n\n"
            f"DETAILED SCRAPED CONTENT:\n{state['scraped_content']}"
        )
        state["report"] = writer_chain.invoke({
            "topic":    topic,
            "research": research_combined,
        })

        # ── Step 4 · Critique ──
        with pipeline_ph.container():
            render_pipeline(active=3, done_up_to=3)
        status_ph.info(step_labels[3])

        state["feedback"] = critic_chain.invoke({"report": state["report"]})

        # ── Done ──
        with pipeline_ph.container():
            render_pipeline(active=-1, done_up_to=4)
        status_ph.empty()

        st.session_state.results = state
        st.session_state.history.append({"topic": topic, "state": state})

    except Exception as e:
        st.session_state.error = str(e)
        status_ph.empty()

    finally:
        st.session_state.running = False
    st.rerun()


# ── Results ────────────────────────────────────────────────────────────────────
if st.session_state.error:
    st.markdown(f"""
    <div class="result-card" style="border-color:#ff6b6b33;">
        <div class="card-header">
            <div class="card-icon">⚠️</div>
            <p class="card-title" style="color:#ff6b6b;">Pipeline Error</p>
        </div>
        <div class="card-body" style="color:#ff6b6b88;">{st.session_state.error}</div>
    </div>
    """, unsafe_allow_html=True)

elif st.session_state.results:
    s = st.session_state.results

    # Success banner
    st.markdown(f"""
    <div class="success-banner">
        <span>✓</span>
        <span>Research complete · 4 agents · topic: <strong>{topic or "—"}</strong></span>
    </div>
    """, unsafe_allow_html=True)

    # Pipeline final state (all done)
    render_pipeline(active=-1, done_up_to=4)

    # ── Cards ──
    def card(css_cls, icon, title, content, meta=""):
        # truncate very long raw content behind an expander
        preview   = content[:1200] + ("…" if len(content) > 1200 else "")
        full_html = f"""
        <div class="result-card {css_cls}">
            <div class="card-header">
                <div class="card-icon">{icon}</div>
                <p class="card-title">{title}</p>
                <span class="card-meta">{meta}</span>
            </div>
            <div class="card-body">{preview}</div>
        </div>
        """
        st.markdown(full_html, unsafe_allow_html=True)
        if len(content) > 1200:
            with st.expander("Show full output"):
                st.text(content)

    card("card-search",
         "🔍", "Search Agent — Raw Results",
         s.get("search_results", ""),
         f"{len(s.get('search_results',''))} chars")

    card("card-scrape",
         "📄", "Reader Agent — Scraped Content",
         s.get("scraped_content", ""),
         f"{len(s.get('scraped_content',''))} chars")

    # Report gets its own larger card + download button
    report = s.get("report", "")
    st.markdown(f"""
    <div class="result-card card-report">
        <div class="card-header">
            <div class="card-icon">✍️</div>
            <p class="card-title">Writer Agent — Research Report</p>
            <span class="card-meta">{len(report)} chars</span>
        </div>
        <div class="card-body">{report}</div>
    </div>
    """, unsafe_allow_html=True)

    dl_col, _ = st.columns([1, 3])
    with dl_col:
        st.download_button(
            "⬇  Download Report (.txt)",
            data=report,
            file_name=f"report_{topic[:40].replace(' ','_')}.txt",
            mime="text/plain",
            use_container_width=True,
        )

    card("card-critic",
         "🎯", "Critic Agent — Feedback",
         s.get("feedback", ""),
         f"{len(s.get('feedback',''))} chars")

else:
    # Idle state — show pipeline in rest
    render_pipeline(active=-1, done_up_to=0)


# ── Sidebar — history ──────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <p style="font-family:'Syne',sans-serif;font-weight:700;
              font-size:1rem;margin-bottom:1rem;color:#e8eaf0;">
        Session History
    </p>
    """, unsafe_allow_html=True)

    if not st.session_state.history:
        st.markdown(
            "<p style='font-size:0.8rem;color:#5a6070;font-family:DM Mono,monospace;'>"
            "No research yet.</p>",
            unsafe_allow_html=True,
        )
    else:
        for idx, item in enumerate(reversed(st.session_state.history)):
            st.markdown(
                f"<p style='font-size:0.8rem;color:#b0b8cc;"
                f"font-family:DM Sans,sans-serif;margin:0.3rem 0;'>"
                f"{'🔬'} {item['topic'][:45]}</p>",
                unsafe_allow_html=True,
            )
        if st.button("Clear history", use_container_width=True):
            st.session_state.history = []
            st.rerun()