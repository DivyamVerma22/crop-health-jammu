# =========================
# IMPORTS
# =========================
import streamlit as st
import ee
import numpy as np
import joblib
import folium
from streamlit_folium import st_folium
from datetime import datetime

# =========================
# PAGE CONFIG
# =========================
st.set_page_config(
    page_title="Spatio-Temporal Crop Health Assessment — Jammu Region",
    layout="wide",
    page_icon="🌾",
    initial_sidebar_state="expanded",
)

# =========================
# SCIENTIFIC-PROJECT STYLING
# Clean, restrained, neutral. Reads like a research dashboard,
# not a consumer product.
# =========================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Serif:wght@500;600;700&family=IBM+Plex+Sans:wght@300;400;500;600&family=IBM+Plex+Mono:wght@400;500&display=swap');

html, body, [class*="css"] {
    font-family: 'IBM Plex Sans', -apple-system, system-ui, sans-serif;
    color: #1f2937;
}
.stApp {
    background: #fafaf7;
}

/* ---- Document header ---- */
.doc-header {
    border-bottom: 2px solid #1f2937;
    padding: 18px 0 14px 0;
    margin-bottom: 28px;
}
.doc-eyebrow {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.72rem;
    letter-spacing: 1.4px;
    text-transform: uppercase;
    color: #6b7280;
    margin-bottom: 6px;
}
.doc-title {
    font-family: 'IBM Plex Serif', serif;
    font-size: 1.7rem;
    font-weight: 600;
    color: #111827;
    margin: 0 0 4px 0;
    line-height: 1.25;
    letter-spacing: -0.2px;
}
.doc-subtitle {
    font-size: 0.92rem;
    color: #4b5563;
    margin: 0;
    max-width: 720px;
    line-height: 1.55;
}
.doc-meta {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.72rem;
    color: #6b7280;
    margin-top: 10px;
    letter-spacing: 0.3px;
}

/* ---- Section headers (numbered like a paper) ---- */
.sec-h {
    font-family: 'IBM Plex Serif', serif;
    font-size: 1.05rem;
    font-weight: 600;
    color: #111827;
    margin: 28px 0 10px 0;
    padding-bottom: 6px;
    border-bottom: 1px solid #d1d5db;
    letter-spacing: -0.1px;
}
.sec-num {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.78rem;
    font-weight: 500;
    color: #6b7280;
    margin-right: 8px;
}

/* ---- Result block ---- */
.result-block {
    background: #ffffff;
    border: 1px solid #d1d5db;
    border-radius: 4px;
    padding: 20px 24px;
    margin-bottom: 16px;
}
.result-row {
    display: grid;
    grid-template-columns: 200px 1fr;
    gap: 18px;
    padding: 6px 0;
    border-bottom: 1px dotted #e5e7eb;
}
.result-row:last-child { border-bottom: none; }
.result-key {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.78rem;
    color: #6b7280;
    letter-spacing: 0.2px;
}
.result-val {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.92rem;
    color: #111827;
    font-weight: 500;
}
.result-val.num {
    font-variant-numeric: tabular-nums;
}

/* ---- CHS panel ---- */
.chs-panel {
    background: #ffffff;
    border: 1px solid #d1d5db;
    border-left: 4px solid #374151;
    border-radius: 4px;
    padding: 22px 26px;
    margin-bottom: 18px;
    display: grid;
    grid-template-columns: 1fr 2fr;
    gap: 26px;
    align-items: center;
}
.chs-value {
    font-family: 'IBM Plex Serif', serif;
    font-size: 2.6rem;
    font-weight: 600;
    color: #111827;
    line-height: 1;
    font-variant-numeric: tabular-nums;
}
.chs-label {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.7rem;
    letter-spacing: 1.4px;
    text-transform: uppercase;
    color: #6b7280;
    margin-bottom: 6px;
}
.chs-cat {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.78rem;
    letter-spacing: 1px;
    text-transform: uppercase;
    margin-top: 6px;
    padding: 3px 10px;
    display: inline-block;
    border-radius: 2px;
    border: 1px solid currentColor;
}
.cat-low { color: #b45309; }
.cat-mod { color: #6b7280; }
.cat-high { color: #166534; }

.chs-bar-wrap {
    width: 100%;
    background: #f3f4f6;
    border: 1px solid #e5e7eb;
    height: 10px;
    border-radius: 2px;
    position: relative;
    margin: 14px 0 6px 0;
}
.chs-bar-fill {
    height: 100%;
    background: #374151;
}
.chs-bar-marker {
    position: absolute;
    top: -3px; bottom: -3px;
    width: 2px;
    background: #1f2937;
}
.chs-bar-ticks {
    display: flex;
    justify-content: space-between;
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.68rem;
    color: #6b7280;
    margin-top: 2px;
}

/* ---- Feature table ---- */
.feat-table {
    width: 100%;
    border-collapse: collapse;
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.86rem;
    background: #ffffff;
    border: 1px solid #d1d5db;
    border-radius: 4px;
    overflow: hidden;
}
.feat-table th {
    background: #f3f4f6;
    color: #374151;
    font-weight: 500;
    text-align: left;
    padding: 9px 14px;
    font-size: 0.74rem;
    letter-spacing: 0.6px;
    text-transform: uppercase;
    border-bottom: 1px solid #d1d5db;
}
.feat-table td {
    padding: 9px 14px;
    border-bottom: 1px solid #f3f4f6;
    color: #1f2937;
    font-variant-numeric: tabular-nums;
}
.feat-table tr:last-child td { border-bottom: none; }
.feat-table .flag-low { color: #b45309; font-weight: 500; }
.feat-table .flag-high { color: #1e40af; font-weight: 500; }
.feat-table .flag-norm { color: #374151; }

/* ---- Recommendation card ---- */
.rec-card {
    background: #ffffff;
    border: 1px solid #d1d5db;
    border-left: 3px solid #6b7280;
    border-radius: 3px;
    padding: 14px 18px;
    margin-bottom: 10px;
}
.rec-card.do { border-left-color: #166534; }
.rec-card.dont { border-left-color: #b45309; }
.rec-trigger {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.68rem;
    letter-spacing: 0.8px;
    text-transform: uppercase;
    color: #6b7280;
    margin-bottom: 4px;
}
.rec-text {
    font-size: 0.92rem;
    color: #1f2937;
    line-height: 1.55;
    margin-bottom: 6px;
}
.rec-ref {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.72rem;
    color: #6b7280;
}
.rec-ref-tag {
    display: inline-block;
    background: #f3f4f6;
    border: 1px solid #d1d5db;
    border-radius: 2px;
    padding: 1px 6px;
    margin-right: 4px;
    font-size: 0.7rem;
}

/* ---- Sidebar ---- */
[data-testid="stSidebar"] {
    background: #f5f5f0 !important;
    border-right: 1px solid #d1d5db;
}
[data-testid="stSidebar"] * {
    color: #1f2937 !important;
}

/* ---- Buttons ---- */
.stButton > button {
    font-family: 'IBM Plex Sans', sans-serif;
    font-weight: 500;
    border-radius: 3px;
    border: 1px solid #374151;
    color: #ffffff;
    letter-spacing: 0.2px;
    transition: background 0.15s ease;
}
.stButton > button:hover {
    background: #111827;
    color: #ffffff;
}

/* ---- Methodology note ---- */
.method-note {
    background: #f9fafb;
    border: 1px solid #e5e7eb;
    border-left: 3px solid #6b7280;
    padding: 14px 18px;
    font-size: 0.86rem;
    color: #374151;
    line-height: 1.6;
    margin-bottom: 16px;
}

/* ---- Footnote ---- */
.footnote {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.72rem;
    color: #6b7280;
    line-height: 1.6;
    padding-top: 18px;
    border-top: 1px solid #e5e7eb;
    margin-top: 32px;
}

/* Hide default Streamlit chrome that looks consumer-y */
[data-testid="stMetricDelta"] { display: none; }
.stAlert { border-radius: 3px !important; }
</style>
""", unsafe_allow_html=True)


# =========================
# LOAD MODEL
# =========================
@st.cache_resource
def load_model():
    return joblib.load("models/Best_model.pkl")

model = load_model()


# =========================
# INIT GEE (SAFE)
# =========================
@st.cache_resource
def init_gee():
    try:
        ee.Initialize(project='gee-jammu-dissertation')
    except Exception:
        try:
            ee.Authenticate()
            ee.Initialize(project='gee-jammu-dissertation')
        except Exception:
            pass

init_gee()


# =========================
# SESSION STATE
# =========================
for key, default in [("run_clicked", False), ("result", None)]:
    if key not in st.session_state:
        st.session_state[key] = default


# =========================
# SIDEBAR
# =========================
with st.sidebar:
    st.markdown("""
    <div style='padding: 16px 0 10px 0;'>
        <div style='font-family:IBM Plex Mono,monospace; font-size:0.68rem;
                    letter-spacing:1.4px; text-transform:uppercase; color:#6b7280;'>
            Research Tool · v1.0
        </div>
        <div style='font-family:IBM Plex Serif,serif; font-size:1.05rem;
                    font-weight:600; color:#111827; margin-top:2px;'>
            CHS Assessment
        </div>
    </div>
    <hr style='border:none; border-top:1px solid #d1d5db; margin: 4px 0 18px 0;'>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div style='font-family:IBM Plex Mono,monospace; font-size:0.68rem;
                letter-spacing:1.2px; text-transform:uppercase;
                color:#6b7280; margin-bottom:8px;'>
        Input Parameters
    </div>
    """, unsafe_allow_html=True)

    lat = st.number_input("Latitude (WGS84)",  value=32.7266, format="%.6f")
    lon = st.number_input("Longitude (WGS84)", value=74.8570, format="%.6f")

    st.markdown("<div style='margin-top:18px;'></div>", unsafe_allow_html=True)
    run_btn = st.button("Run Prediction", use_container_width=True)
    reset_btn = st.button("Reset", use_container_width=True)

    if run_btn:
        st.session_state.run_clicked = True
    if reset_btn:
        st.session_state.run_clicked = False
        st.session_state.result = None

    st.markdown("""
    <hr style='border:none; border-top:1px solid #d1d5db; margin: 22px 0 12px 0;'>
    <div style='font-family:IBM Plex Mono,monospace; font-size:0.68rem;
                letter-spacing:1.2px; text-transform:uppercase;
                color:#6b7280; margin-bottom:8px;'>
        Data Sources
    </div>
    <div style='font-size:0.82rem; color:#374151; line-height:1.7;'>
        Sentinel-2 SR &nbsp;·&nbsp; <span style='color:#6b7280;'>spectral bands</span><br>
        MODIS MOD11A2 &nbsp;·&nbsp; <span style='color:#6b7280;'>LST</span><br>
        CHIRPS Daily &nbsp;·&nbsp; <span style='color:#6b7280;'>precipitation</span>
    </div>
    <hr style='border:none; border-top:1px solid #d1d5db; margin: 18px 0 10px 0;'>
    <div style='font-family:IBM Plex Mono,monospace; font-size:0.66rem; color:#6b7280; line-height:1.6;'>
        AOI: Jammu region<br>
        32.50–33.50 °N, 74.50–75.88 °E
    </div>
    """, unsafe_allow_html=True)


# =========================
# DOCUMENT HEADER
# =========================
st.markdown("""
<div class="doc-header">
    <div class="doc-eyebrow">Master's Dissertation · Remote Sensing &amp; Machine Learning</div>
    <h1 class="doc-title">Spatio-Temporal Crop Health Assessment for the Jammu Region</h1>
    <p class="doc-subtitle">
        Coordinate-level Crop Health Score (CHS) inference using Sentinel-2 surface reflectance,
        MODIS land-surface temperature, and CHIRPS precipitation, scored by a temporally-validated
        Random Forest regressor (R² ≈ 0.61 on the 2024+ hold-out).
    </p>
    <div class="doc-meta">
        Model: Random Forest (n_estimators=400) &nbsp;·&nbsp;
        Window: 6 months × 7 features &nbsp;·&nbsp;
        Target: CHS<sub>t</sub> ∈ [0, 1]
    </div>
</div>
""", unsafe_allow_html=True)


# =========================
# CLASSIFICATION
# =========================
def classify_chs(chs):
    if chs < 0.30:
        return "Low"
    elif chs < 0.60:
        return "Moderate"
    else:
        return "High"


# =========================
# REGIONAL FEATURE THRESHOLDS
# Derived from the empirical distribution of features across the
# 150 training points (data/sample/final.csv).  We use Q25 and Q75
# of the in-region values as "low" and "high" cut-offs so that a
# flag fires only when a feature is genuinely abnormal for Jammu.
# =========================
THRESH = {
    # name      low_cut  high_cut   units
    "NDVI":          (0.333, 0.722),
    "EVI":           (0.257, 0.505),
    "NDMI":          (0.066, 0.240),
    "NDWI":          (-0.628, -0.326),  # higher (less negative) NDWI = wetter/water
    "LST":           (21.3,  29.5),
    "Rainfall":      (101.5, 332.9),
    "Rainfall_lag1": (93.3,  330.8),
}

def feature_status(name, value):
    """Return ('low' | 'norm' | 'high', description)."""
    lo, hi = THRESH[name]
    if value < lo:
        return "low", f"below regional Q25 ({lo:.2f})"
    if value > hi:
        return "high", f"above regional Q75 ({hi:.2f})"
    return "norm", f"within Q25–Q75 ({lo:.2f}–{hi:.2f})"


# =========================
# REFERENCED RECOMMENDATIONS
# Each recommendation is a dict with:
#   trigger    : human-readable condition that activated it
#   text       : the recommendation itself
#   ref_tag    : short citation tag, matched to references.md
#
# Rules are evaluated against (category, feature values).  Only
# triggered rules appear, so two different sites will see different
# recommendation sets driven by what their satellite features
# actually show.
# =========================

def build_recommendations(category, values):
    """Build Do / Don't lists driven by category + feature values."""
    NDVI = values.get("NDVI", 0.0)
    EVI  = values.get("EVI",  0.0)
    NDMI = values.get("NDMI", 0.0)
    NDWI = values.get("NDWI", -0.5)
    LST  = values.get("LST",  25.0)
    RAIN = values.get("Rainfall", 0.0)
    RAIN_LAG = values.get("Rainfall_lag1", 0.0)

    ndvi_s = feature_status("NDVI", NDVI)[0]
    ndmi_s = feature_status("NDMI", NDMI)[0]
    lst_s  = feature_status("LST",  LST)[0]
    rain_s = feature_status("Rainfall", RAIN)[0]

    dos = []
    donts = []

    # ---- Category-level baseline guidance (always fires) ----
    if category == "High":
        dos.append({
            "trigger": "CHS ≥ 0.60",
            "text": "Maintain the current crop-management regime; canopy vigour and "
                    "biomass indicators are within the upper quartile observed across "
                    "the regional training set.",
            "ref_tag": "Huete2002",
        })
    elif category == "Moderate":
        dos.append({
            "trigger": "0.30 ≤ CHS < 0.60",
            "text": "Schedule a follow-up assessment within 10–14 days; this CHS range "
                    "corresponds to the transition zone where untreated stress most "
                    "frequently degrades to a low-health state.",
            "ref_tag": "Gao1996",
        })
    else:  # Low
        dos.append({
            "trigger": "CHS < 0.30",
            "text": "Initiate field verification immediately and prepare a targeted "
                    "intervention; CHS values in this range coincide with documented "
                    "yield-loss thresholds in semi-arid cereal systems.",
            "ref_tag": "Anderson2007",
        })

    # ---- NDVI-driven rules ----
    if ndvi_s == "low":
        dos.append({
            "trigger": f"NDVI = {NDVI:.3f} (low for Jammu)",
            "text": "Conduct ground-truth biomass and canopy-cover sampling; depressed "
                    "NDVI is a robust indicator of reduced photosynthetically-active "
                    "biomass and should be corroborated before agronomic decisions.",
            "ref_tag": "Tucker1979",
        })
        donts.append({
            "trigger": f"NDVI = {NDVI:.3f}",
            "text": "Avoid attributing the depressed NDVI signal solely to canopy "
                    "stress without checking for confounders such as bare-soil "
                    "exposure, recent tillage, or sensor-related saturation effects.",
            "ref_tag": "Huete1988",
        })
    elif ndvi_s == "high":
        donts.append({
            "trigger": f"NDVI = {NDVI:.3f} (above regional Q75)",
            "text": "Do not over-apply nitrogen; high-NDVI canopies are at elevated "
                    "risk of lodging and nitrogen-induced disease susceptibility in "
                    "dense cropping systems.",
            "ref_tag": "Hatfield2010",
        })

    # ---- NDMI-driven rules (canopy moisture) ----
    if ndmi_s == "low":
        dos.append({
            "trigger": f"NDMI = {NDMI:.3f} (low canopy moisture)",
            "text": "Apply deficit-irrigation protocols and verify soil-moisture "
                    "status at 0–30 cm depth; low NDMI consistently correlates with "
                    "reduced canopy water content in remote-sensing studies.",
            "ref_tag": "Gao1996",
        })
        donts.append({
            "trigger": f"NDMI = {NDMI:.3f}",
            "text": "Avoid mid-day overhead sprinkler irrigation when canopy "
                    "moisture is already stressed; evaporative losses are "
                    "maximised during peak LST hours.",
            "ref_tag": "Allen1998",
        })

    # ---- LST-driven rules (thermal stress) ----
    if lst_s == "high":
        dos.append({
            "trigger": f"LST = {LST:.1f} °C (above regional Q75)",
            "text": "Consider applying potassium-based foliar sprays or temporary "
                    "shading; sustained high LST is associated with reduced stomatal "
                    "conductance and photosynthetic efficiency in C3 crops.",
            "ref_tag": "Anderson2007",
        })
        donts.append({
            "trigger": f"LST = {LST:.1f} °C",
            "text": "Do not apply contact pesticides under elevated canopy "
                    "temperatures; phytotoxicity risk and active-ingredient "
                    "volatilisation both increase sharply above 30 °C.",
            "ref_tag": "Matthews2000",
        })
    elif lst_s == "low":
        donts.append({
            "trigger": f"LST = {LST:.1f} °C (below regional Q25)",
            "text": "Avoid scheduling thermo-sensitive operations such as germination "
                    "tests; sub-Q25 LST values often coincide with cloud-affected "
                    "or partially-snow-covered pixels in this AOI.",
            "ref_tag": "Wan2014",
        })

    # ---- Rainfall-driven rules ----
    if rain_s == "low" and RAIN_LAG < THRESH["Rainfall_lag1"][0]:
        dos.append({
            "trigger": f"Rainfall = {RAIN:.0f} mm, lag = {RAIN_LAG:.0f} mm (compound dry)",
            "text": "Treat this as a compound-drought episode; both the contemporaneous "
                    "month and the antecedent period fall below regional Q25, which "
                    "consistently precedes yield loss in CHIRPS-based drought studies.",
            "ref_tag": "Funk2015",
        })
    elif rain_s == "low":
        dos.append({
            "trigger": f"Rainfall = {RAIN:.0f} mm (below regional Q25)",
            "text": "Verify irrigation infrastructure availability and prioritise water "
                    "delivery; CHIRPS-derived monthly totals are well-calibrated for "
                    "the western Himalayan foothills.",
            "ref_tag": "Funk2015",
        })

    if rain_s == "high":
        donts.append({
            "trigger": f"Rainfall = {RAIN:.0f} mm (above regional Q75)",
            "text": "Do not undertake heavy machinery operations on saturated soils; "
                    "structural compaction caused by trafficking under excess "
                    "moisture has measurable multi-season productivity impacts.",
            "ref_tag": "Hamza2005",
        })

    # ---- NDVI vs NDMI dissociation (early stress signal) ----
    if ndvi_s != "low" and ndmi_s == "low":
        dos.append({
            "trigger": "NDVI normal, NDMI low (early-stress signature)",
            "text": "Treat this combination as an early-warning indicator. Canopy "
                    "structure is still intact but tissue-level water content has "
                    "declined — a documented precursor to visible stress symptoms.",
            "ref_tag": "Gao1996",
        })

    return dos, donts


# =========================
# PREDICTION FUNCTION
# (Inference logic unchanged per user request — same as supplied version.)
# =========================
def predict_chs(lat, lon):
    point = ee.Geometry.Point([lon, lat])

    today = datetime.today()
    year  = today.year
    month = today.month

    start_date = f"{year}-01-01"
    end_date   = f"{year}-03-31"

    def select(img):
        return img.select(['B2', 'B3', 'B4', 'B8', 'B11'])

    s2 = (
        ee.ImageCollection("COPERNICUS/S2_SR")
        .filterBounds(point)
        .filterDate(start_date, end_date)
        .filter(ee.Filter.lt('CLOUDY_PIXEL_PERCENTAGE', 10))
        .map(select)
        .median()
    )

    ndvi = s2.normalizedDifference(['B8', 'B4']).rename('NDVI')
    evi  = s2.expression(
        '2.5*((NIR-RED)/(NIR+6*RED-7.5*BLUE+1))',
        {'NIR': s2.select('B8'), 'RED': s2.select('B4'), 'BLUE': s2.select('B2')}
    ).rename('EVI')
    ndmi = s2.normalizedDifference(['B8',  'B11']).rename('NDMI')
    ndwi = s2.normalizedDifference(['B3',  'B8' ]).rename('NDWI')

    lst = (
        ee.ImageCollection("MODIS/061/MOD11A2")
        .filterBounds(point)
        .filterDate(start_date, end_date)
        .select('LST_Day_1km')
        .mean()
        .multiply(0.02)
        .subtract(273.15)
        .rename('LST')
    )

    rain = (
        ee.ImageCollection("UCSB-CHG/CHIRPS/DAILY")
        .filterBounds(point)
        .filterDate(start_date, end_date)
        .sum()
        .rename('Rainfall')
    )

    rain_lag = (
        ee.ImageCollection("UCSB-CHG/CHIRPS/DAILY")
        .filterBounds(point)
        .filterDate(f"{year-1}-10-01", f"{year-1}-12-31")
        .sum()
        .rename('Rainfall_lag1')
    )

    feature_img = ee.Image.cat([ndvi, evi, ndmi, ndwi, lst, rain, rain_lag])

    values = feature_img.reduceRegion(
        reducer   = ee.Reducer.mean(),
        geometry  = point,
        scale     = 30,
        maxPixels = 1e9
    ).getInfo()

    if None in values.values():
        return None

    features = ['NDVI', 'EVI', 'NDMI', 'NDWI', 'LST', 'Rainfall', 'Rainfall_lag1']
    x       = np.array([values[f] for f in features], dtype='float32')
    X_model = np.repeat(x.reshape(1, -1), 6, axis=1)
    chs     = model.predict(X_model)[0]

    return chs, month, year, values


# =========================
# MAIN EXECUTION
# =========================
if st.session_state.run_clicked:
    with st.spinner("Retrieving satellite features and running inference…"):
        result = predict_chs(lat, lon)
        st.session_state.result = result

    if result is None:
        st.error("Insufficient satellite data for the selected location and date range. "
                 "Check cloud cover or adjust coordinates.")
    else:
        st.success("Prediction complete.")


# =========================
# RESULTS DISPLAY
# =========================
if st.session_state.result is not None:
    chs, month, year, values = st.session_state.result
    category = classify_chs(chs)
    chs_pct = float(min(max(chs * 100, 0), 100))
    month_name = datetime(year, month, 1).strftime("%B")

    cat_cls = {"Low": "cat-low", "Moderate": "cat-mod", "High": "cat-high"}[category]

    # =========================
    # § 1. PREDICTION RESULT
    # =========================
    st.markdown('<div class="sec-h"><span class="sec-num">§ 1</span>Prediction</div>',
                unsafe_allow_html=True)

    st.markdown(f"""
    <div class="chs-panel">
        <div>
            <div class="chs-label">Crop Health Score</div>
            <div class="chs-value">{chs:.3f}</div>
            <div class="chs-cat {cat_cls}">{category}</div>
        </div>
        <div>
            <div class="chs-label" style='margin-bottom:8px;'>Position on regional CHS scale</div>
            <div class="chs-bar-wrap">
                <div class="chs-bar-fill" style="width:{chs_pct:.1f}%;"></div>
                <div class="chs-bar-marker" style="left:30%;"></div>
                <div class="chs-bar-marker" style="left:60%;"></div>
            </div>
            <div class="chs-bar-ticks">
                <span>0.00</span><span>0.30 · Low|Mod</span>
                <span>0.60 · Mod|High</span><span>1.00</span>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(f"""
    <div class="result-block">
        <div class="result-row">
            <div class="result-key">Location</div>
            <div class="result-val num">{lat:.6f} °N, {lon:.6f} °E</div>
        </div>
        <div class="result-row">
            <div class="result-key">Reference period</div>
            <div class="result-val">{month_name} {year}</div>
        </div>
        <div class="result-row">
            <div class="result-key">CHS</div>
            <div class="result-val num">{chs:.4f}</div>
        </div>
        <div class="result-row">
            <div class="result-key">Classification</div>
            <div class="result-val">{category}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # =========================
    # § 2. EXTRACTED FEATURES
    # =========================
    st.markdown('<div class="sec-h"><span class="sec-num">§ 2</span>Extracted Features</div>',
                unsafe_allow_html=True)

    st.markdown("""
    <div class="method-note">
        Feature values shown below are spatial means at the queried point.
        "Status" flags compare each value against the empirical
        Q25–Q75 range observed across the 150 training points (Jammu region),
        not against generic textbook thresholds.
    </div>
    """, unsafe_allow_html=True)

    feature_rows = []
    for name, val, unit, desc in [
        ("NDVI", values["NDVI"], "—", "Normalised Difference Vegetation Index"),
        ("EVI", values["EVI"], "—", "Enhanced Vegetation Index"),
        ("NDMI", values["NDMI"], "—", "Normalised Difference Moisture Index"),
        ("NDWI", values["NDWI"], "—", "Normalised Difference Water Index"),
        ("LST", values["LST"], "°C", "Land Surface Temperature (MODIS day-time)"),
        ("Rainfall", values["Rainfall"], "mm", "CHIRPS cumulative precipitation (current window)"),
        ("Rainfall_lag1", values["Rainfall_lag1"], "mm", "CHIRPS lagged precipitation (Oct–Dec prior year)"),
    ]:
        status, status_desc = feature_status(name, val)
        flag_cls = {"low": "flag-low", "high": "flag-high", "norm": "flag-norm"}[status]
        flag_lbl = {"low": "LOW", "high": "HIGH", "norm": "NORMAL"}[status]
        feature_rows.append(
            f"<tr>"
            f"<td><strong>{name}</strong></td>"
            f"<td>{val:.3f} {unit}</td>"
            f"<td class='{flag_cls}'>{flag_lbl}</td>"
            f"<td style='color:#6b7280; font-family:IBM Plex Sans, sans-serif;'>{status_desc}</td>"
            f"<td style='color:#6b7280; font-family:IBM Plex Sans, sans-serif;'>{desc}</td>"
            f"</tr>"
        )

    st.markdown(f"""
    <table class="feat-table">
        <thead><tr>
            <th>Feature</th>
            <th>Value</th>
            <th>Status</th>
            <th>Reference range</th>
            <th>Description</th>
        </tr></thead>
        <tbody>{''.join(feature_rows)}</tbody>
    </table>
    """, unsafe_allow_html=True)

    # =========================
    # § 3. SPATIAL CONTEXT
    # =========================
    st.markdown('<div class="sec-h"><span class="sec-num">§ 3</span>Spatial Context</div>',
                unsafe_allow_html=True)

    fmap = folium.Map(
        location=[lat, lon],
        zoom_start=11,
        control_scale=True,
        tiles="CartoDB positron",
    )
    color_map = {"Low": "#b45309", "Moderate": "#6b7280", "High": "#166534"}
    folium.CircleMarker(
        location=[lat, lon],
        radius=10,
        color=color_map[category],
        fill=True,
        fill_color=color_map[category],
        fill_opacity=0.7,
        weight=2,
        popup=folium.Popup(
            f"<b>CHS:</b> {chs:.3f}<br><b>Class:</b> {category}<br>"
            f"<b>NDVI:</b> {values['NDVI']:.3f}<br><b>LST:</b> {values['LST']:.1f} °C",
            max_width=220
        ),
        tooltip=f"CHS {chs:.3f} · {category}",
    ).add_to(fmap)
    folium.Circle(
        location=[lat, lon], radius=1500,
        color=color_map[category], fill=False, weight=1.5, dash_array="4,4",
    ).add_to(fmap)
    folium.Rectangle(
        bounds=[[32.50, 74.50], [33.50, 75.88]],
        color="#1f2937", weight=1.5, fill=False, dash_array="6,6",
        tooltip="Training AOI",
    ).add_to(fmap)
    st_folium(fmap, width=None, height=380)

    # =========================
    # § 4. AGRONOMIC RECOMMENDATIONS
    # =========================
    st.markdown('<div class="sec-h"><span class="sec-num">§ 4</span>Agronomic Recommendations</div>',
                unsafe_allow_html=True)

    st.markdown(f"""
    <div class="method-note">
        Recommendations below are evaluated dynamically against the
        <strong>predicted CHS class</strong> and the <strong>extracted feature
        values</strong> at this location. Only rules whose trigger condition
        is met for this point are shown; two different fields will see
        different recommendation sets. Each item is linked to a referenced
        source (see <code>references.md</code> in the repository).
    </div>
    """, unsafe_allow_html=True)

    dos, donts = build_recommendations(category, values)

    col_a, col_b = st.columns([1, 1], gap="medium")

    with col_a:
        st.markdown("**Recommended actions**")
        if not dos:
            st.markdown("_No rules fired at this point._")
        for item in dos:
            st.markdown(f"""
            <div class="rec-card do">
                <div class="rec-trigger">Trigger · {item['trigger']}</div>
                <div class="rec-text">{item['text']}</div>
                <div class="rec-ref"><span class="rec-ref-tag">{item['ref_tag']}</span></div>
            </div>
            """, unsafe_allow_html=True)

    with col_b:
        st.markdown("**Actions to avoid**")
        if not donts:
            st.markdown("_No contraindications fired at this point._")
        for item in donts:
            st.markdown(f"""
            <div class="rec-card dont">
                <div class="rec-trigger">Trigger · {item['trigger']}</div>
                <div class="rec-text">{item['text']}</div>
                <div class="rec-ref"><span class="rec-ref-tag">{item['ref_tag']}</span></div>
            </div>
            """, unsafe_allow_html=True)

    # =========================
    # FOOTNOTE
    # =========================
    st.markdown("""
    <div class="footnote">
        <strong>Disclaimer.</strong> Predictions are derived from remote-sensing inputs and
        a Random Forest regressor trained on 150 fixed sampling points across the Jammu region.
        Recommendations are heuristic, derived from peer-reviewed sources, and intended to
        support — not replace — ground-truth field assessment by a qualified agronomist.
        Citation tags shown next to each recommendation resolve to entries in
        <code>references.md</code>.
    </div>
    """, unsafe_allow_html=True)


# =========================
# EMPTY STATE
# =========================
else:
    st.markdown("""
    <div style="background:#ffffff; border:1px solid #d1d5db; border-radius:4px;
                padding:36px 40px; text-align:left;">
        <div style="font-family:'IBM Plex Mono',monospace; font-size:0.72rem;
                    letter-spacing:1.4px; text-transform:uppercase; color:#6b7280;
                    margin-bottom:10px;">
            STATE · No active prediction
        </div>
        <div style="font-family:'IBM Plex Serif',serif; font-size:1.05rem;
                    color:#111827; margin-bottom:8px;">
            Enter coordinates and run inference
        </div>
        <div style="font-size:0.88rem; color:#4b5563; line-height:1.65; max-width:640px;">
            Specify a latitude and longitude in the sidebar (default values are pre-filled
            for the Jammu region) and click <strong>Run Prediction</strong>. The system will
            retrieve Sentinel-2, MODIS, and CHIRPS observations through Earth Engine,
            compute the seven model features, and return the predicted Crop Health Score
            along with feature-driven agronomic recommendations.
        </div>
    </div>
    """, unsafe_allow_html=True)