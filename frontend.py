import os
import streamlit as st
import requests
import plotly.graph_objects as go
import plotly.express as px

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="InsurancePremiumAI",
    page_icon="🛡️",
    layout="wide"
)

st.title("🛡️ InsurancePremiumAI")
st.caption("AI-Powered Insurance Premium Prediction Platform")

# ── Constants ─────────────────────────────────────────────────────────────────
API_URL = os.getenv(
    "API_URL",
    "http://localhost:8000/predict"
)

VALID_CITIES = sorted([
    'Agra', 'Ahmedabad', 'Allahabad', 'Amritsar', 'Bangalore', 'Bhopal',
    'Chennai', 'Delhi', 'Faridabad', 'Ghaziabad', 'Hyderabad', 'Indore',
    'Jaipur', 'Kanpur', 'Kolkata', 'Lucknow', 'Ludhiana', 'Meerut',
    'Mumbai', 'Nagpur', 'Nashik', 'Patna', 'Pune', 'Rajkot', 'Ranchi',
    'Srinagar', 'Surat', 'Vadodara', 'Varanasi', 'Visakhapatnam'
])

VALID_OCCUPATIONS = sorted([
    'Accountant', 'Architect', 'Banker', 'Businessman', 'Carpenter',
    'Chef', 'Civil Servant', 'Consultant', 'Content Writer', 'Data Analyst',
    'Doctor', 'Driver', 'Electrician', 'Engineer', 'Factory Worker',
    'Government Employee', 'HR Manager', 'Insurance Agent', 'Lab Technician',
    'Lawyer', 'Marketing Manager', 'Nurse', 'Pharmacist', 'Plumber',
    'Real Estate Agent', 'Retail Manager', 'Sales Manager', 'Shop Owner',
    'Software Engineer', 'Teacher'
])

PREMIUM_COLORS = {
    "Low":    {"bg": "#d1fae5", "border": "#10b981", "text": "#065f46", "icon": "✅"},
    "Medium": {"bg": "#fef3c7", "border": "#f59e0b", "text": "#78350f", "icon": "⚡"},
    "High":   {"bg": "#fee2e2", "border": "#ef4444", "text": "#7f1d1d", "icon": "🔥"},
}

# ── Global CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Sora:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap');

html, body, [class*="css"] {
    font-family: 'Sora', sans-serif;
}

/* Background */
.stApp {
    background: #0d0f1a;
}

/* Hide default Streamlit chrome */
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding: 2rem 3rem 4rem; max-width: 1300px; }

/* ── Hero banner ── */
.hero {
    background: linear-gradient(135deg, #1a1f3a 0%, #0f172a 60%, #0d1117 100%);
    border: 1px solid rgba(99,102,241,.25);
    border-radius: 20px;
    padding: 2.5rem 3rem;
    margin-bottom: 2rem;
    position: relative;
    overflow: hidden;
}
.hero::before {
    content: '';
    position: absolute;
    top: -60px; right: -60px;
    width: 260px; height: 260px;
    background: radial-gradient(circle, rgba(99,102,241,.18) 0%, transparent 70%);
    border-radius: 50%;
}
.hero-tag {
    display: inline-block;
    background: rgba(99,102,241,.15);
    border: 1px solid rgba(99,102,241,.4);
    color: #818cf8;
    font-size: .72rem;
    font-weight: 600;
    letter-spacing: .1em;
    text-transform: uppercase;
    padding: .3rem .9rem;
    border-radius: 999px;
    margin-bottom: 1rem;
}
.hero h1 {
    font-size: 2.4rem;
    font-weight: 700;
    color: #f1f5f9;
    margin: 0 0 .5rem;
    line-height: 1.15;
}
.hero h1 span { color: #818cf8; }
.hero p {
    color: #94a3b8;
    font-size: .95rem;
    margin: 0;
    max-width: 520px;
}
.hero-badge {
    position: absolute;
    top: 2rem; right: 2.5rem;
    background: rgba(16,185,129,.1);
    border: 1px solid rgba(16,185,129,.3);
    color: #34d399;
    font-size: .75rem;
    font-weight: 600;
    padding: .35rem .9rem;
    border-radius: 999px;
    font-family: 'JetBrains Mono', monospace;
}

/* ── Section cards ── */
.section-card {
    background: #131629;
    border: 1px solid rgba(255,255,255,.07);
    border-radius: 16px;
    padding: 1.6rem 1.8rem 1.8rem;
    margin-bottom: 1.2rem;
}
.section-label {
    font-size: .68rem;
    font-weight: 700;
    letter-spacing: .12em;
    text-transform: uppercase;
    color: #6366f1;
    margin-bottom: .3rem;
}
.section-title {
    font-size: 1.05rem;
    font-weight: 600;
    color: #e2e8f0;
    margin-bottom: 1.2rem;
    display: flex;
    align-items: center;
    gap: .5rem;
}
.section-divider {
    border: none;
    border-top: 1px solid rgba(255,255,255,.06);
    margin: 1rem 0 1.4rem;
}

/* ── Streamlit widget overrides ── */
div[data-testid="stNumberInput"] input,
div[data-testid="stTextInput"] input,
div[data-testid="stSelectbox"] div[data-baseweb="select"] {
    background-color: #0d0f1a !important;
    border: 1px solid rgba(255,255,255,.12) !important;
    border-radius: 8px !important;
    color: #f1f5f9 !important;
    font-family: 'Sora', sans-serif !important;
}
div[data-testid="stNumberInput"] input:focus,
div[data-testid="stSelectbox"] div[data-baseweb="select"]:focus-within {
    border-color: #6366f1 !important;
    box-shadow: 0 0 0 3px rgba(99,102,241,.15) !important;
}
label[data-testid="stWidgetLabel"] p,
.stSelectbox label p,
.stNumberInput label p {
    color: #94a3b8 !important;
    font-size: .82rem !important;
    font-weight: 500 !important;
    font-family: 'Sora', sans-serif !important;
}

/* Toggle (smoker) */
.stToggle label { color: #94a3b8 !important; font-size: .82rem !important; }

/* ── Submit button ── */
div[data-testid="stFormSubmitButton"] button {
    width: 100%;
    background: linear-gradient(135deg, #6366f1, #4f46e5) !important;
    color: white !important;
    border: none !important;
    border-radius: 12px !important;
    padding: .85rem 2rem !important;
    font-size: 1rem !important;
    font-weight: 600 !important;
    font-family: 'Sora', sans-serif !important;
    letter-spacing: .02em;
    cursor: pointer;
    transition: all .2s;
    box-shadow: 0 4px 20px rgba(99,102,241,.35) !important;
}
div[data-testid="stFormSubmitButton"] button:hover {
    background: linear-gradient(135deg, #818cf8, #6366f1) !important;
    box-shadow: 0 6px 28px rgba(99,102,241,.5) !important;
    transform: translateY(-1px);
}

/* ── Result cards ── */
.result-hero {
    border-radius: 16px;
    padding: 2rem 2.2rem;
    margin-bottom: 1.2rem;
    display: flex;
    flex-direction: column;
    gap: .4rem;
}
.result-hero .result-icon { font-size: 2.4rem; }
.result-hero .result-label {
    font-size: .72rem;
    font-weight: 700;
    letter-spacing: .12em;
    text-transform: uppercase;
    opacity: .7;
}
.result-hero .result-value {
    font-size: 2rem;
    font-weight: 700;
    line-height: 1.1;
}
.result-hero .result-sub { font-size: .85rem; opacity: .75; margin-top: .1rem; }

.metric-card {
    background: #131629;
    border: 1px solid rgba(255,255,255,.07);
    border-radius: 14px;
    padding: 1.2rem 1.4rem;
    text-align: center;
}
.metric-card .m-label {
    font-size: .7rem;
    font-weight: 600;
    letter-spacing: .1em;
    text-transform: uppercase;
    color: #64748b;
    margin-bottom: .4rem;
}
.metric-card .m-value {
    font-size: 1.6rem;
    font-weight: 700;
    color: #f1f5f9;
    font-family: 'JetBrains Mono', monospace;
}
.metric-card .m-sub { font-size: .75rem; color: #64748b; margin-top: .2rem; }

/* Prob row */
.prob-row {
    display: flex;
    align-items: center;
    gap: .9rem;
    margin-bottom: .7rem;
}
.prob-name {
    width: 75px;
    font-size: .82rem;
    font-weight: 600;
    color: #cbd5e1;
    flex-shrink: 0;
}
.prob-bar-bg {
    flex: 1;
    background: rgba(255,255,255,.07);
    border-radius: 999px;
    height: 8px;
    overflow: hidden;
}
.prob-bar-fill {
    height: 8px;
    border-radius: 999px;
    transition: width .6s ease;
}
.prob-pct {
    width: 46px;
    text-align: right;
    font-size: .8rem;
    font-weight: 600;
    font-family: 'JetBrains Mono', monospace;
    color: #94a3b8;
}

.input-summary {
    background: #0d0f1a;
    border: 1px solid rgba(255,255,255,.07);
    border-radius: 12px;
    padding: 1rem 1.2rem;
}
.input-summary table { width: 100%; border-collapse: collapse; }
.input-summary td {
    padding: .35rem .1rem;
    font-size: .82rem;
    color: #94a3b8;
    border-bottom: 1px solid rgba(255,255,255,.04);
}
.input-summary td:last-child { color: #e2e8f0; font-weight: 500; text-align: right; }
.input-summary tr:last-child td { border-bottom: none; }

.error-box {
    background: rgba(239,68,68,.08);
    border: 1px solid rgba(239,68,68,.3);
    border-radius: 12px;
    padding: 1rem 1.2rem;
    color: #fca5a5;
    font-size: .88rem;
}
.placeholder-box {
    background: #131629;
    border: 1px dashed rgba(99,102,241,.2);
    border-radius: 16px;
    padding: 3rem 2rem;
    text-align: center;
    color: #334155;
}
.placeholder-box .ph-icon { font-size: 2.8rem; margin-bottom: 1rem; }
.placeholder-box p { font-size: .9rem; color: #475569; margin: 0; }

/* BMI badge */
.bmi-badge {
    display: inline-block;
    padding: .2rem .7rem;
    border-radius: 999px;
    font-size: .72rem;
    font-weight: 700;
    font-family: 'JetBrains Mono', monospace;
    margin-top: .4rem;
}
</style>
""", unsafe_allow_html=True)


# ── Helper: BMI ───────────────────────────────────────────────────────────────
def compute_bmi(weight_kg: float, height_cm: float) -> tuple[float, str, str]:
    if height_cm <= 0:
        return 0.0, "–", "#64748b"
    bmi = weight_kg / ((height_cm / 100) ** 2)
    if bmi < 18.5:
        return round(bmi, 1), "Underweight", "#60a5fa"
    elif bmi < 25:
        return round(bmi, 1), "Normal", "#34d399"
    elif bmi < 30:
        return round(bmi, 1), "Overweight", "#fbbf24"
    else:
        return round(bmi, 1), "Obese", "#f87171"


# ── Helper: API call ──────────────────────────────────────────────────────────
def call_api(payload: dict):
    try:
        resp = requests.post(API_URL, json=payload, timeout=10)
        resp.raise_for_status()
        return resp.json(), None
    except requests.exceptions.ConnectionError:
        return None, "Cannot connect to API at `localhost:8000`. Make sure the FastAPI server is running."
    except requests.exceptions.HTTPError as e:
        try:
            detail = e.response.json().get("detail", str(e))
        except Exception:
            detail = str(e)
        return None, f"API error {e.response.status_code}: {detail}"
    except Exception as e:
        return None, str(e)


# ── Helper: Plotly gauge ──────────────────────────────────────────────────────
def confidence_gauge(value: float) -> go.Figure:
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=value,
        number={"suffix": "%", "font": {"size": 28, "color": "#f1f5f9", "family": "JetBrains Mono"}},
        gauge={
            "axis": {"range": [0, 100], "tickcolor": "#334155", "tickfont": {"color": "#475569", "size": 10}},
            "bar": {"color": "#6366f1", "thickness": 0.28},
            "bgcolor": "rgba(0,0,0,0)",
            "borderwidth": 0,
            "steps": [
                {"range": [0, 40],  "color": "rgba(239,68,68,.12)"},
                {"range": [40, 70], "color": "rgba(245,158,11,.1)"},
                {"range": [70, 100],"color": "rgba(16,185,129,.1)"},
            ],
            "threshold": {
                "line": {"color": "#818cf8", "width": 2},
                "thickness": 0.75,
                "value": value
            }
        }
    ))
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        margin=dict(t=20, b=10, l=20, r=20),
        height=180,
        font={"family": "Sora"},
    )
    return fig


# ── Helper: Prob bar chart ────────────────────────────────────────────────────
def prob_bar_chart(probs: dict) -> go.Figure:
    colors_map = {"Low": "#34d399", "Medium": "#fbbf24", "High": "#f87171"}
    labels = list(probs.keys())
    values = [v * 100 for v in probs.values()]
    bar_colors = [colors_map.get(k, "#818cf8") for k in labels]

    fig = go.Figure(go.Bar(
        x=labels, y=values,
        marker_color=bar_colors,
        marker_line_width=0,
        text=[f"{v:.1f}%" for v in values],
        textposition="outside",
        textfont={"color": "#94a3b8", "size": 12, "family": "JetBrains Mono"},
    ))
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        margin=dict(t=30, b=10, l=10, r=10),
        height=200,
        xaxis=dict(showgrid=False, tickfont={"color": "#94a3b8", "size": 12}, linecolor="rgba(0,0,0,0)"),
        yaxis=dict(showgrid=True, gridcolor="rgba(255,255,255,.05)", tickfont={"color": "#475569", "size": 10}, range=[0, max(values) * 1.25]),
        showlegend=False,
    )
    return fig


# ── SESSION STATE ─────────────────────────────────────────────────────────────
if "result" not in st.session_state:
    st.session_state.result = None
if "error" not in st.session_state:
    st.session_state.error = None
if "last_input" not in st.session_state:
    st.session_state.last_input = None


# ══════════════════════════════════════════════════════════════════════════════
# HERO
# ══════════════════════════════════════════════════════════════════════════════
st.markdown("""
<div class="hero">
    <div class="hero-tag">🛡️ AI-Powered Underwriting</div>
    <h1>Insurance <span>Premium</span> Predictor</h1>
    <p>Enter applicant details below to instantly predict the insurance premium category using our XGBoost model.</p>
    <div class="hero-badge">● Model Online</div>
</div>
""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# LAYOUT — left (form) | right (results)
# ══════════════════════════════════════════════════════════════════════════════
left, right = st.columns([1.05, 0.95], gap="large")

# ─────────────────────────────────────────────────────────
# LEFT — Input Form
# ─────────────────────────────────────────────────────────
with left:
    with st.form("predict_form", clear_on_submit=False):

        # ── Section 1: Personal Information ──────────────────
        st.markdown("""
        <div class="section-card">
            <div class="section-label">Section 01</div>
            <div class="section-title">👤 Personal Information</div>
        """, unsafe_allow_html=True)

        col1, col2 = st.columns(2)
        with col1:
            age = st.number_input("Age (years)", min_value=1, max_value=119, value=30, step=1)
        with col2:
            city = st.selectbox("City", options=VALID_CITIES, index=VALID_CITIES.index("Mumbai"))

        occupation = st.selectbox("Occupation", options=VALID_OCCUPATIONS, index=VALID_OCCUPATIONS.index("Software Engineer"))

        smoker = st.toggle("Smoker", value=False)

        st.markdown("</div>", unsafe_allow_html=True)

        # ── Section 2: Physical Details ───────────────────────
        st.markdown("""
        <div class="section-card">
            <div class="section-label">Section 02</div>
            <div class="section-title">⚖️ Physical Details</div>
        """, unsafe_allow_html=True)

        col3, col4 = st.columns(2)
        with col3:
            weight = st.number_input("Weight (kg)", min_value=1.0, max_value=300.0, value=70.0, step=0.5, format="%.1f")
        with col4:
            height = st.number_input("Height (cm)", min_value=100.0, max_value=249.0, value=170.0, step=0.5, format="%.1f")

        # Live BMI preview
        bmi_val, bmi_cat, bmi_color = compute_bmi(weight, height)
        st.markdown(f"""
        <div style="margin-top:.3rem; color:#64748b; font-size:.8rem;">
            Calculated BMI: 
            <span style="color:{bmi_color}; font-weight:700; font-family:'JetBrains Mono',monospace;">{bmi_val}</span>
            <span class="bmi-badge" style="background:rgba(255,255,255,.05); color:{bmi_color}; border:1px solid {bmi_color}44;">
                {bmi_cat}
            </span>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("</div>", unsafe_allow_html=True)

        # ── Section 3: Financial Information ──────────────────
        st.markdown("""
        <div class="section-card">
            <div class="section-label">Section 03</div>
            <div class="section-title">💼 Financial Information</div>
        """, unsafe_allow_html=True)

        income_lpa = st.number_input(
            "Annual Income (LPA — Lakhs Per Annum)",
            min_value=0.1, max_value=500.0, value=8.0, step=0.5, format="%.1f"
        )
        st.markdown(f"""
        <div style="color:#64748b; font-size:.78rem; margin-top:.2rem;">
            ≈ ₹&nbsp;{income_lpa:.1f}L / year &nbsp;·&nbsp; ₹&nbsp;{income_lpa/12:.2f}L / month
        </div>
        """, unsafe_allow_html=True)

        st.markdown("</div>", unsafe_allow_html=True)

        # ── Submit ────────────────────────────────────────────
        submitted = st.form_submit_button("🔍 Predict Premium Category", use_container_width=True)

    # Handle submission
    if submitted:
        payload = {
            "age": int(age),
            "weight": float(weight),
            "height": float(height),
            "income_lpa": float(income_lpa),
            "smoker": bool(smoker),
            "city": city,
            "occupation": occupation,
        }
        with st.spinner("Running prediction model…"):
            result, error = call_api(payload)
        st.session_state.result = result
        st.session_state.error = error
        st.session_state.last_input = payload


# ─────────────────────────────────────────────────────────
# RIGHT — Results Panel
# ─────────────────────────────────────────────────────────
with right:

    # ── No result yet ─────────────────────────────────────
    if st.session_state.result is None and st.session_state.error is None:
        st.markdown("""
        <div class="placeholder-box">
            <div class="ph-icon">🎯</div>
            <p>Fill in the applicant details on the left<br>and click <strong style="color:#6366f1;">Predict Premium Category</strong><br>to see the risk assessment here.</p>
        </div>
        """, unsafe_allow_html=True)

    # ── Error ─────────────────────────────────────────────
    elif st.session_state.error:
        st.markdown(f"""
        <div class="error-box">
            <strong>⚠️ Prediction Failed</strong><br><br>
            {st.session_state.error}
        </div>
        """, unsafe_allow_html=True)

    # ── Results ───────────────────────────────────────────
    else:
        res = st.session_state.result
        inp = st.session_state.last_input
        predicted = res.get("predicted_premium", "–")
        confidence = res.get("confidence", 0.0)
        probs = res.get("class_probabilities", {})
        colors = PREMIUM_COLORS.get(predicted, {"bg": "#1e293b", "border": "#334155", "text": "#e2e8f0", "icon": "📊"})

        # ── Prediction banner ─────────────────────────────
        st.markdown(f"""
        <div class="result-hero" style="background:{colors['bg']}22; border:1px solid {colors['border']}55;">
            <div class="result-icon">{colors['icon']}</div>
            <div class="result-label" style="color:{colors['text']};">Predicted Premium Category</div>
            <div class="result-value" style="color:{colors['border']};">{predicted} Premium</div>
            <div class="result-sub" style="color:{colors['text']};">Model confidence: <strong>{confidence}%</strong></div>
        </div>
        """, unsafe_allow_html=True)

        # ── Confidence gauge + top metric ─────────────────
        mc1, mc2 = st.columns(2)
        with mc1:
            st.markdown('<div class="section-card" style="padding:1.2rem;">', unsafe_allow_html=True)
            st.markdown('<div class="section-label">Confidence Score</div>', unsafe_allow_html=True)
            st.plotly_chart(confidence_gauge(confidence), use_container_width=True, config={"displayModeBar": False})
            st.markdown('</div>', unsafe_allow_html=True)
        with mc2:
            bmi_v, bmi_c, bmi_col = compute_bmi(inp["weight"], inp["height"])
            st.markdown(f"""
            <div class="section-card" style="padding:1.2rem;">
                <div class="section-label">Quick Stats</div>
                <div style="display:flex; flex-direction:column; gap:.8rem; margin-top:.5rem;">
                    <div>
                        <div style="font-size:.7rem; color:#64748b; font-weight:600; letter-spacing:.08em; text-transform:uppercase;">BMI</div>
                        <div style="font-size:1.4rem; font-weight:700; color:{bmi_col}; font-family:'JetBrains Mono',monospace;">{bmi_v} <span style="font-size:.8rem; font-weight:500;">{bmi_c}</span></div>
                    </div>
                    <div>
                        <div style="font-size:.7rem; color:#64748b; font-weight:600; letter-spacing:.08em; text-transform:uppercase;">Smoker Status</div>
                        <div style="font-size:1.1rem; font-weight:700; color:{'#f87171' if inp['smoker'] else '#34d399'};">{'🚬 Yes' if inp['smoker'] else '✅ Non-smoker'}</div>
                    </div>
                    <div>
                        <div style="font-size:.7rem; color:#64748b; font-weight:600; letter-spacing:.08em; text-transform:uppercase;">Income</div>
                        <div style="font-size:1.1rem; font-weight:700; color:#e2e8f0; font-family:'JetBrains Mono',monospace;">₹ {inp['income_lpa']:.1f} LPA</div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)

        # ── Class probabilities chart ─────────────────────
        st.markdown("""
        <div class="section-card">
            <div class="section-label">Risk Distribution</div>
            <div class="section-title" style="margin-bottom:.5rem;">📊 Class Probabilities</div>
        """, unsafe_allow_html=True)

        # Custom bars
        prob_colors = {"Low": "#34d399", "Medium": "#fbbf24", "High": "#f87171"}
        for cls, prob in probs.items():
            pct = round(prob * 100, 1)
            col = prob_colors.get(cls, "#818cf8")
            st.markdown(f"""
            <div class="prob-row">
                <div class="prob-name">{cls}</div>
                <div class="prob-bar-bg">
                    <div class="prob-bar-fill" style="width:{pct}%; background:{col};"></div>
                </div>
                <div class="prob-pct" style="color:{col};">{pct}%</div>
            </div>
            """, unsafe_allow_html=True)

        # Plotly bar
        st.plotly_chart(prob_bar_chart(probs), use_container_width=True, config={"displayModeBar": False})
        st.markdown("</div>", unsafe_allow_html=True)

        # ── Input summary ─────────────────────────────────
        st.markdown("""
        <div class="section-card">
            <div class="section-label">Submitted Data</div>
            <div class="section-title" style="margin-bottom:.8rem;">🗂️ Input Summary</div>
            <div class="input-summary">
        """, unsafe_allow_html=True)

        rows = [
            ("Age", f"{inp['age']} yrs"),
            ("City", inp['city']),
            ("Occupation", inp['occupation']),
            ("Weight", f"{inp['weight']} kg"),
            ("Height", f"{inp['height']} cm"),
            ("Income", f"₹ {inp['income_lpa']} LPA"),
            ("Smoker", "Yes" if inp['smoker'] else "No"),
        ]
        table_html = "<table>" + "".join(
            f"<tr><td>{k}</td><td>{v}</td></tr>" for k, v in rows
        ) + "</table>"
        st.markdown(table_html + "</div></div>", unsafe_allow_html=True)


# ── Footer ────────────────────────────────────────────────────────────────────
st.markdown("""
<div style="text-align:center; margin-top:3rem; padding-top:1.5rem; border-top:1px solid rgba(255,255,255,.05);">
    <span style="font-size:.75rem; color:#334155;">
        InsureIQ · XGBoost Prediction Engine · Built by 
        <span style="color:#6366f1;">Kaushik</span>
    </span>
</div>
""", unsafe_allow_html=True)