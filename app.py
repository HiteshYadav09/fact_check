"""
app.py - Main Streamlit application for AI Fact Checker.
Professional UI with real-time fact verification, animated verdict cards,
search history, and downloadable reports.
"""

import streamlit as st
import json
import os
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Import core modules
from verifier import verify_claim, VERDICT_CONFIG

# ─── Page Configuration ────────────────────────────────────────────────────────
st.set_page_config(
    page_title="AI Fact Checker",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─── Custom CSS Styling ────────────────────────────────────────────────────────
def inject_css():
    st.markdown("""
    <style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Sans:wght@300;400;500&display=swap');

    /* Global Reset */
    *, *::before, *::after { box-sizing: border-box; }

    /* Root variables */
    :root {
        --bg-primary: #080c14;
        --bg-secondary: #0d1525;
        --bg-card: #111827;
        --bg-card-hover: #161f30;
        --border: #1e2d45;
        --border-accent: #2d4a6e;
        --text-primary: #f1f5f9;
        --text-secondary: #94a3b8;
        --text-muted: #4b6080;
        --accent: #3b82f6;
        --accent-glow: rgba(59, 130, 246, 0.15);
    }

    /* Main background */
    .stApp {
        background: var(--bg-primary) !important;
        font-family: 'DM Sans', sans-serif !important;
    }

    /* Hide Streamlit chrome */
    #MainMenu, footer, header { visibility: hidden; }
    .block-container { padding: 2rem 2rem 4rem !important; max-width: 900px !important; margin: 0 auto; }

    /* Hero header */
    .hero-section {
        text-align: center;
        padding: 3rem 1rem 2rem;
        position: relative;
    }
    .hero-section::before {
        content: '';
        position: absolute;
        top: 0; left: 50%; transform: translateX(-50%);
        width: 600px; height: 300px;
        background: radial-gradient(ellipse at center, rgba(59,130,246,0.08) 0%, transparent 70%);
        pointer-events: none;
    }
    .hero-badge {
        display: inline-block;
        background: rgba(59,130,246,0.1);
        border: 1px solid rgba(59,130,246,0.3);
        color: #60a5fa;
        font-family: 'DM Sans', sans-serif;
        font-size: 0.7rem;
        font-weight: 500;
        letter-spacing: 0.15em;
        text-transform: uppercase;
        padding: 0.3rem 1rem;
        border-radius: 100px;
        margin-bottom: 1.2rem;
    }
    .hero-title {
        font-family: 'Syne', sans-serif;
        font-size: clamp(2rem, 5vw, 3.5rem);
        font-weight: 800;
        color: var(--text-primary);
        line-height: 1.1;
        margin: 0 0 1rem;
        letter-spacing: -0.03em;
    }
    .hero-title span {
        background: linear-gradient(135deg, #3b82f6 0%, #60a5fa 50%, #93c5fd 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    .hero-desc {
        font-family: 'DM Sans', sans-serif;
        font-size: 1rem;
        color: var(--text-secondary);
        max-width: 520px;
        margin: 0 auto;
        line-height: 1.7;
        font-weight: 300;
    }

    /* Stats row */
    .stats-row {
        display: flex;
        justify-content: center;
        gap: 2rem;
        margin: 2rem 0;
        flex-wrap: wrap;
    }
    .stat-item {
        text-align: center;
    }
    .stat-value {
        font-family: 'Syne', sans-serif;
        font-size: 1.4rem;
        font-weight: 700;
        color: #60a5fa;
    }
    .stat-label {
        font-size: 0.72rem;
        color: var(--text-muted);
        letter-spacing: 0.08em;
        text-transform: uppercase;
    }

    /* Input area */
    .input-section {
        background: var(--bg-card);
        border: 1px solid var(--border);
        border-radius: 16px;
        padding: 1.8rem;
        margin: 1.5rem 0;
        transition: border-color 0.3s ease;
    }
    .input-section:hover { border-color: var(--border-accent); }
    .input-label {
        font-family: 'Syne', sans-serif;
        font-size: 0.8rem;
        font-weight: 600;
        color: var(--text-secondary);
        letter-spacing: 0.1em;
        text-transform: uppercase;
        margin-bottom: 0.6rem;
    }

    /* Streamlit textarea override */
    .stTextArea textarea {
        background: var(--bg-secondary) !important;
        border: 1px solid var(--border) !important;
        border-radius: 10px !important;
        color: var(--text-primary) !important;
        font-family: 'DM Sans', sans-serif !important;
        font-size: 0.95rem !important;
        line-height: 1.6 !important;
        resize: vertical !important;
        transition: border-color 0.2s ease, box-shadow 0.2s ease !important;
    }
    .stTextArea textarea:focus {
        border-color: var(--accent) !important;
        box-shadow: 0 0 0 3px var(--accent-glow) !important;
        outline: none !important;
    }
    .stTextArea label { display: none !important; }

    /* Button */
    .stButton > button {
        background: linear-gradient(135deg, #2563eb 0%, #3b82f6 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 10px !important;
        font-family: 'Syne', sans-serif !important;
        font-size: 0.9rem !important;
        font-weight: 600 !important;
        letter-spacing: 0.05em !important;
        padding: 0.7rem 2.5rem !important;
        width: 100% !important;
        transition: all 0.2s ease !important;
        cursor: pointer !important;
    }
    .stButton > button:hover {
        background: linear-gradient(135deg, #1d4ed8 0%, #2563eb 100%) !important;
        transform: translateY(-1px) !important;
        box-shadow: 0 8px 25px rgba(59,130,246,0.35) !important;
    }
    .stButton > button:active { transform: translateY(0) !important; }

    /* Verdict card */
    .verdict-card {
        border-radius: 16px;
        padding: 2rem;
        margin: 1.5rem 0;
        border: 1px solid;
        position: relative;
        overflow: hidden;
        animation: fadeInUp 0.5s ease forwards;
    }
    .verdict-card::before {
        content: '';
        position: absolute;
        top: 0; right: 0;
        width: 200px; height: 200px;
        border-radius: 50%;
        opacity: 0.04;
        transform: translate(40%, -40%);
    }
    @keyframes fadeInUp {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }
    .verdict-header {
        display: flex;
        align-items: center;
        justify-content: space-between;
        flex-wrap: wrap;
        gap: 1rem;
        margin-bottom: 1rem;
    }
    .verdict-badge {
        font-family: 'Syne', sans-serif;
        font-size: 1.6rem;
        font-weight: 800;
        letter-spacing: 0.05em;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }
    .confidence-ring {
        text-align: center;
        min-width: 80px;
    }
    .confidence-value {
        font-family: 'Syne', sans-serif;
        font-size: 2rem;
        font-weight: 800;
        line-height: 1;
    }
    .confidence-label {
        font-size: 0.65rem;
        text-transform: uppercase;
        letter-spacing: 0.1em;
        color: var(--text-muted);
        margin-top: 0.2rem;
    }
    .verdict-summary {
        font-family: 'DM Sans', sans-serif;
        font-size: 1rem;
        line-height: 1.7;
        color: var(--text-secondary);
        margin-top: 0.5rem;
    }

    /* Info cards */
    .info-card {
        background: var(--bg-card);
        border: 1px solid var(--border);
        border-radius: 12px;
        padding: 1.4rem;
        margin: 1rem 0;
        transition: border-color 0.2s ease;
        animation: fadeInUp 0.5s ease forwards;
    }
    .info-card:hover { border-color: var(--border-accent); }
    .card-title {
        font-family: 'Syne', sans-serif;
        font-size: 0.75rem;
        font-weight: 600;
        color: var(--text-muted);
        letter-spacing: 0.12em;
        text-transform: uppercase;
        margin-bottom: 0.8rem;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }
    .card-content {
        font-family: 'DM Sans', sans-serif;
        font-size: 0.92rem;
        color: var(--text-secondary);
        line-height: 1.75;
    }

    /* Evidence bullets */
    .evidence-item {
        display: flex;
        gap: 0.75rem;
        align-items: flex-start;
        padding: 0.6rem 0;
        border-bottom: 1px solid rgba(30,45,69,0.5);
        animation: fadeInUp 0.4s ease forwards;
    }
    .evidence-item:last-child { border-bottom: none; }
    .evidence-dot {
        width: 6px; height: 6px;
        border-radius: 50%;
        background: #3b82f6;
        margin-top: 0.45rem;
        flex-shrink: 0;
    }
    .evidence-text {
        font-size: 0.88rem;
        color: var(--text-secondary);
        line-height: 1.6;
    }

    /* Reasoning steps */
    .step-item {
        display: flex;
        gap: 1rem;
        align-items: flex-start;
        padding: 0.7rem 0;
        border-bottom: 1px solid rgba(30,45,69,0.4);
    }
    .step-item:last-child { border-bottom: none; }
    .step-num {
        width: 24px; height: 24px;
        border-radius: 50%;
        background: rgba(59,130,246,0.1);
        border: 1px solid rgba(59,130,246,0.3);
        color: #60a5fa;
        font-family: 'Syne', sans-serif;
        font-size: 0.7rem;
        font-weight: 700;
        display: flex; align-items: center; justify-content: center;
        flex-shrink: 0;
        margin-top: 0.1rem;
    }
    .step-text {
        font-size: 0.88rem;
        color: var(--text-secondary);
        line-height: 1.6;
    }

    /* Source cards */
    .source-card {
        background: var(--bg-secondary);
        border: 1px solid var(--border);
        border-radius: 10px;
        padding: 1rem 1.2rem;
        margin: 0.6rem 0;
        transition: all 0.2s ease;
        animation: fadeInUp 0.4s ease forwards;
    }
    .source-card:hover {
        border-color: var(--border-accent);
        background: var(--bg-card-hover);
    }
    .source-title {
        font-family: 'Syne', sans-serif;
        font-size: 0.88rem;
        font-weight: 600;
        color: var(--text-primary);
        margin-bottom: 0.3rem;
        line-height: 1.4;
    }
    .source-url {
        font-size: 0.78rem;
        color: #60a5fa;
        text-decoration: none;
        word-break: break-all;
    }
    .source-snippet {
        font-size: 0.8rem;
        color: var(--text-muted);
        margin-top: 0.4rem;
        line-height: 1.5;
        display: -webkit-box;
        -webkit-line-clamp: 2;
        -webkit-box-orient: vertical;
        overflow: hidden;
    }

    /* History item */
    .history-item {
        background: var(--bg-card);
        border: 1px solid var(--border);
        border-radius: 10px;
        padding: 0.9rem 1rem;
        margin: 0.4rem 0;
        cursor: pointer;
        transition: all 0.2s ease;
    }
    .history-item:hover { border-color: var(--border-accent); }
    .history-verdict { font-size: 0.7rem; font-weight: 600; }
    .history-claim { font-size: 0.82rem; color: var(--text-secondary); margin-top: 0.2rem; line-height: 1.4; }
    .history-time { font-size: 0.7rem; color: var(--text-muted); margin-top: 0.3rem; }

    /* Divider */
    .section-divider {
        border: none;
        border-top: 1px solid var(--border);
        margin: 1.5rem 0;
    }

    /* Streamlit expander override */
    .streamlit-expanderHeader {
        background: var(--bg-card) !important;
        border: 1px solid var(--border) !important;
        border-radius: 10px !important;
        color: var(--text-primary) !important;
        font-family: 'Syne', sans-serif !important;
        font-size: 0.85rem !important;
        font-weight: 600 !important;
    }
    .streamlit-expanderContent {
        background: var(--bg-secondary) !important;
        border: 1px solid var(--border) !important;
        border-top: none !important;
        border-radius: 0 0 10px 10px !important;
    }

    /* Scrollbar */
    ::-webkit-scrollbar { width: 6px; }
    ::-webkit-scrollbar-track { background: var(--bg-primary); }
    ::-webkit-scrollbar-thumb { background: var(--border-accent); border-radius: 3px; }

    /* Sidebar */
    section[data-testid="stSidebar"] {
        background: var(--bg-secondary) !important;
        border-right: 1px solid var(--border) !important;
    }
    section[data-testid="stSidebar"] * { color: var(--text-secondary) !important; }

    /* Error/warning */
    .stAlert { border-radius: 10px !important; }

    /* Download button */
    .stDownloadButton > button {
        background: var(--bg-card) !important;
        color: var(--text-secondary) !important;
        border: 1px solid var(--border) !important;
        border-radius: 8px !important;
        font-family: 'DM Sans', sans-serif !important;
        font-size: 0.82rem !important;
        width: 100% !important;
        transition: all 0.2s ease !important;
    }
    .stDownloadButton > button:hover {
        border-color: var(--border-accent) !important;
        color: var(--text-primary) !important;
    }
    </style>
    """, unsafe_allow_html=True)


# ─── UI Components ─────────────────────────────────────────────────────────────

def render_hero():
    """Render the hero header section."""
    st.markdown("""
    <div class="hero-section">
        <div class="hero-badge">🔍 AI-Powered Verification</div>
        <h1 class="hero-title">
            Stop Misinformation.<br><span>Know What's True.</span>
        </h1>
        <p class="hero-desc">
            Paste any claim, headline, or rumor. Our AI searches the web in real time,
            analyzes evidence, and delivers a verdict you can trust.
        </p>
    </div>
    """, unsafe_allow_html=True)


def render_verdict_card(result: dict):
    """Render the main verdict card."""
    cfg = result.get("verdict_config", VERDICT_CONFIG["UNVERIFIED"])
    verdict = result.get("verdict", "UNVERIFIED")
    confidence = result.get("confidence_score", 0)
    summary = result.get("summary", "")

    card_html = f"""
    <div class="verdict-card" style="
        background: {cfg['bg']};
        border-color: {cfg['border']};
    ">
        <div class="verdict-header">
            <div class="verdict-badge" style="color: {cfg['color']};">
                {cfg['emoji']} {verdict}
            </div>
            <div class="confidence-ring">
                <div class="confidence-value" style="color: {cfg['color']};">{confidence}%</div>
                <div class="confidence-label">Confidence</div>
            </div>
        </div>
        <p class="verdict-summary">{summary}</p>
    </div>
    """
    st.markdown(card_html, unsafe_allow_html=True)


def render_explanation(result: dict):
    """Render detailed explanation card."""
    explanation = result.get("detailed_explanation", "")
    if not explanation:
        return
    st.markdown(f"""
    <div class="info-card">
        <div class="card-title">📋 Detailed Analysis</div>
        <div class="card-content">{explanation}</div>
    </div>
    """, unsafe_allow_html=True)


def render_evidence(result: dict):
    """Render key evidence bullets."""
    evidence = result.get("key_evidence", [])
    if not evidence:
        return

    items_html = "".join([
        f'<div class="evidence-item"><div class="evidence-dot"></div><div class="evidence-text">{e}</div></div>'
        for e in evidence
    ])

    st.markdown(f"""
    <div class="info-card">
        <div class="card-title">🔑 Key Evidence</div>
        {items_html}
    </div>
    """, unsafe_allow_html=True)


def render_reasoning(result: dict):
    """Render reasoning steps inside expander."""
    steps = result.get("reasoning_steps", [])
    if not steps:
        return

    with st.expander("🧠 AI Reasoning Chain", expanded=False):
        steps_html = "".join([
            f'<div class="step-item"><div class="step-num">{i+1}</div><div class="step-text">{s}</div></div>'
            for i, s in enumerate(steps)
        ])
        st.markdown(f"""
        <div style="padding: 0.5rem 0;">
            {steps_html}
        </div>
        """, unsafe_allow_html=True)


def render_source_reliability(result: dict):
    """Render source reliability assessment."""
    reliability = result.get("source_reliability", "")
    conclusion = result.get("final_conclusion", "")

    if not reliability and not conclusion:
        return

    st.markdown(f"""
    <div class="info-card">
        <div class="card-title">🛡️ Source Reliability</div>
        <div class="card-content">{reliability}</div>
        {'<hr style="border-color: #1e2d45; margin: 0.8rem 0;" />' if conclusion else ''}
        {'<div class="card-title">🎯 Final Conclusion</div><div class="card-content">' + conclusion + '</div>' if conclusion else ''}
    </div>
    """, unsafe_allow_html=True)


def render_sources(sources: list):
    """Render clickable source cards."""
    if not sources:
        return

    with st.expander(f"🌐 Sources ({len(sources)} found)", expanded=True):
        for src in sources:
            title = src.get("title", "Untitled Source")
            url = src.get("url", "#")
            snippet = src.get("content", "")[:150]
            domain = url.split("/")[2] if url.startswith("http") else url

            st.markdown(f"""
            <div class="source-card">
                <div class="source-title">{title}</div>
                <a href="{url}" target="_blank" class="source-url">{domain}</a>
                <div class="source-snippet">{snippet}...</div>
            </div>
            """, unsafe_allow_html=True)


def generate_report(claim: str, result: dict) -> str:
    """Generate a downloadable text report."""
    cfg = result.get("verdict_config", {})
    lines = [
        "=" * 60,
        "AI FACT CHECKER — VERIFICATION REPORT",
        "=" * 60,
        f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        f"Claim: {claim}",
        "",
        f"VERDICT: {result.get('verdict', 'UNKNOWN')}",
        f"CONFIDENCE: {result.get('confidence_score', 0)}%",
        "",
        "SUMMARY:",
        result.get("summary", ""),
        "",
        "DETAILED EXPLANATION:",
        result.get("detailed_explanation", ""),
        "",
        "KEY EVIDENCE:",
    ]
    for e in result.get("key_evidence", []):
        lines.append(f"  • {e}")

    lines += [
        "",
        "SOURCE RELIABILITY:",
        result.get("source_reliability", ""),
        "",
        "FINAL CONCLUSION:",
        result.get("final_conclusion", ""),
        "",
        "SOURCES:",
    ]
    for src in result.get("sources", []):
        lines.append(f"  • {src.get('title', '')} — {src.get('url', '')}")

    lines += ["", "=" * 60, "Generated by AI Fact Checker", "=" * 60]
    return "\n".join(lines)


# ─── Sidebar ────────────────────────────────────────────────────────────────────

def render_sidebar():
    """Render sidebar with history and info."""
    with st.sidebar:
        st.markdown("""
        <div style="padding: 1rem 0 0.5rem;">
            <div style="font-family: 'Syne', sans-serif; font-size: 1rem; font-weight: 700; color: #f1f5f9;">
                📜 History
            </div>
            <div style="font-size: 0.75rem; color: #4b6080; margin-top: 0.2rem;">
                Recent verifications
            </div>
        </div>
        """, unsafe_allow_html=True)

        history = st.session_state.get("history", [])

        if not history:
            st.markdown("""
            <div style="font-size:0.82rem; color:#4b6080; padding:0.8rem 0;">
                No checks yet. Verify a claim to see history here.
            </div>
            """, unsafe_allow_html=True)
        else:
            for i, item in enumerate(reversed(history[-10:])):
                cfg = VERDICT_CONFIG.get(item["verdict"], VERDICT_CONFIG["UNVERIFIED"])
                truncated = item["claim"][:60] + "..." if len(item["claim"]) > 60 else item["claim"]
                st.markdown(f"""
                <div class="history-item">
                    <div class="history-verdict" style="color:{cfg['color']};">
                        {cfg['emoji']} {item['verdict']} · {item['confidence']}%
                    </div>
                    <div class="history-claim">{truncated}</div>
                    <div class="history-time">{item['timestamp']}</div>
                </div>
                """, unsafe_allow_html=True)

        st.markdown("<hr class='section-divider' />", unsafe_allow_html=True)

        # Legend
        st.markdown("""
        <div style="font-family:'Syne',sans-serif; font-size:0.72rem; font-weight:600;
                    color:#4b6080; letter-spacing:0.1em; text-transform:uppercase; margin-bottom:0.8rem;">
            Verdict Guide
        </div>
        """, unsafe_allow_html=True)

        for key, cfg in VERDICT_CONFIG.items():
            st.markdown(f"""
            <div style="display:flex; align-items:center; gap:0.5rem; margin:0.4rem 0;">
                <span>{cfg['emoji']}</span>
                <span style="font-size:0.78rem; color:{cfg['color']}; font-weight:600;">{key}</span>
            </div>
            """, unsafe_allow_html=True)


# ─── Main App ──────────────────────────────────────────────────────────────────

def main():
    # Initialize session state
    if "history" not in st.session_state:
        st.session_state.history = []
    if "last_result" not in st.session_state:
        st.session_state.last_result = None
    if "last_claim" not in st.session_state:
        st.session_state.last_claim = ""

    inject_css()
    render_sidebar()
    render_hero()

    # Stats row
    history_len = len(st.session_state.history)
    st.markdown(f"""
    <div class="stats-row">
        <div class="stat-item">
            <div class="stat-value">{history_len}</div>
            <div class="stat-label">Claims Checked</div>
        </div>
        <div class="stat-item">
            <div class="stat-value">6</div>
            <div class="stat-label">Verdict Types</div>
        </div>
        <div class="stat-item">
            <div class="stat-value">Real-time</div>
            <div class="stat-label">Web Search</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Input section
    st.markdown('<div class="input-section">', unsafe_allow_html=True)
    st.markdown('<div class="input-label">🔍 Enter Claim to Verify</div>', unsafe_allow_html=True)

    claim = st.text_area(
        label="claim_input",
        placeholder='Enter a claim, news headline, or statement to verify...\n\nExample: "NASA confirmed aliens landed in India"',
        height=130,
        key="claim_input",
        label_visibility="collapsed",
    )

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        verify_btn = st.button("🔍  Verify Claim", key="verify_btn", use_container_width=True)

    st.markdown('</div>', unsafe_allow_html=True)

    # Example claims
    st.markdown("""
    <div style="display:flex; flex-wrap:wrap; gap:0.5rem; margin-bottom:1.5rem; align-items:center;">
        <span style="font-size:0.75rem; color:#4b6080; text-transform:uppercase;
                     letter-spacing:0.08em; font-weight:600;">Try:</span>
    """, unsafe_allow_html=True)

    examples = [
        "The Great Wall of China is visible from space",
        "Drinking coffee stunts your growth",
        "NASA confirmed water on Mars",
    ]
    ex_cols = st.columns(len(examples))
    for i, (col, ex) in enumerate(zip(ex_cols, examples)):
        with col:
            if st.button(f'"{ex[:35]}..."', key=f"ex_{i}", use_container_width=True):
                st.session_state.claim_input = ex
                st.rerun()

    # ─── Verification Logic ─────────────────────────────────────────────────
    if verify_btn:
        claim_text = claim.strip()

        if not claim_text:
            st.error("⚠️ Please enter a claim to verify.")
        elif len(claim_text) < 10:
            st.error("⚠️ Claim is too short. Please provide more detail.")
        else:
            with st.spinner("🔍 Searching the web for evidence..."):
                try:
                    result = verify_claim(claim_text)

                    # Save to session state
                    st.session_state.last_result = result
                    st.session_state.last_claim = claim_text

                    # Add to history
                    st.session_state.history.append({
                        "claim": claim_text,
                        "verdict": result.get("verdict", "UNVERIFIED"),
                        "confidence": result.get("confidence_score", 0),
                        "timestamp": datetime.now().strftime("%b %d, %H:%M"),
                    })

                except ValueError as e:
                    st.error(f"⚠️ {str(e)}")
                except RuntimeError as e:
                    st.error(f"🚨 API Error: {str(e)}")
                except Exception as e:
                    st.error(f"🚨 Unexpected error: {str(e)}")

    # ─── Results Display ────────────────────────────────────────────────────
    if st.session_state.last_result:
        result = st.session_state.last_result
        claim_text = st.session_state.last_claim

        st.markdown("<hr class='section-divider' />", unsafe_allow_html=True)

        st.markdown(f"""
        <div style="font-size:0.78rem; color:#4b6080; margin-bottom:0.5rem;
                    font-family:'DM Sans',sans-serif;">
            Claim: <span style="color:#94a3b8;">"{claim_text[:120]}{'...' if len(claim_text)>120 else ''}"</span>
        </div>
        """, unsafe_allow_html=True)

        # Verdict card
        render_verdict_card(result)

        # Two-column layout for explanation + evidence
        col_l, col_r = st.columns([3, 2])
        with col_l:
            render_explanation(result)
            render_source_reliability(result)
        with col_r:
            render_evidence(result)

        # Reasoning steps
        render_reasoning(result)

        # Sources
        render_sources(result.get("sources", []))

        # Download report
        st.markdown("<hr class='section-divider' />", unsafe_allow_html=True)
        report_text = generate_report(claim_text, result)
        col_d1, col_d2, col_d3 = st.columns([1, 2, 1])
        with col_d2:
            st.download_button(
                label="⬇️  Download Report",
                data=report_text,
                file_name=f"fact_check_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
                mime="text/plain",
                use_container_width=True,
            )


if __name__ == "__main__":
    main()
