import streamlit as st

# ============================================================
# PAGE CONFIG - MUST BE FIRST
# ============================================================
st.set_page_config(
    page_title="DIA Proteomics Pipeline",
    page_icon="🧬",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ============================================================
# COLORS
# ============================================================
PRIMARY_RED = "#E71316"
DARK_RED = "#A6192E"
PRIMARY_GRAY = "#54585A"
LIGHT_GRAY = "#E2E3E4"

# ============================================================
# CACHED CSS - LOADS ONCE
# ============================================================
@st.cache_resource
def load_css():
    return f"""
    <style>
        * {{font-family: Arial, sans-serif;}}
        .module-header {{
            background: linear-gradient(90deg, {PRIMARY_RED} 0%, {DARK_RED} 100%);
            padding: 30px; border-radius: 8px; margin-bottom: 40px; color: white;
        }}
        .stButton > button[kind="primary"] {{
            background-color: {PRIMARY_RED}; color: white; padding: 12px 24px;
            border-radius: 6px; font-weight: 500;
        }}
        .stButton > button[kind="primary"]:hover {{background-color: {DARK_RED};}}
    </style>
    """

st.markdown(load_css(), unsafe_allow_html=True)

# ============================================================
# HEADER (simplified)
# ============================================================
st.markdown(f"""
<div style="background: {PRIMARY_RED}; padding: 20px; margin: -1rem -1rem 2rem -1rem; color: white;">
    <h1 style="margin: 0; font-size: 28px;">DIA Proteomics Analysis Pipeline</h1>
    <p style="margin: 5px 0 0 0; font-size: 14px;">Module demonstrations and UI components</p>
</div>
""", unsafe_allow_html=True)

# ============================================================
# TABS (Streamlit native - fast)
# ============================================================
tab1, tab2, tab3, tab4 = st.tabs([
    "Module 1: Data Import",
    "Module 2: Quality Control",
    "Module 3: Preprocessing",
    "Module 4: Analysis"
])

with tab1:
    # MODULE HEADER
    st.markdown("""
    <div class="module-header">
        <h2 style="margin:0; font-size:24px;">📥 Module 1: Data Import & Validation</h2>
        <p style="margin:5px 0 0 0; opacity:0.9;">Import mass spectrometry output matrices</p>
    </div>
    """, unsafe_allow_html=True)
    
    # WORKFLOW STEPS - Use native Streamlit columns (faster)
    st.subheader("Workflow Steps")
    c1, c2, c3, c4 = st.columns(4)
    
    with c1:
        st.markdown("**1️⃣ File upload**")
        st.caption("📁 Drag and drop CSV files")
    with c2:
        st.markdown("**2️⃣ Format detection**")
        st.caption("🔍 Automatic identification")
    with c3:
        st.markdown("**3️⃣ Data validation**")
        st.caption("✓ Verify integrity")
    with c4:
        st.markdown("**4️⃣ Preview**")
        st.caption("📋 Review statistics")
    
    st.divider()
    
    # KEY FEATURES (simplified)
    st.subheader("Key features")
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("🔄 **Multi-format support**")
        st.caption("DIA-NN, Spectronaut, MaxQuant, FragPipe")
        
        st.markdown("🛡️ **File validation**")
        st.caption("Schema and data type validation")
        
        st.markdown("📊 **Preliminary statistics**")
        st.caption("Summary stats and column types")
    
    with col2:
        st.markdown("🎯 **Automatic column detection**")
        st.caption("Regex pattern identification")
        
        st.markdown("✏️ **Sample name cleanup**")
        st.caption("Extract and standardize names")
        
        st.markdown("👁️ **Data preview**")
        st.caption("Interactive filtering and sorting")
    
    st.divider()
    
    # UPLOAD DEMO
    st.subheader("Upload demonstration")
    uploaded_file = st.file_uploader("Drop CSV file here", type=["csv"])
    
    c1, c2, c3 = st.columns(3)
    with c1:
        st.button("📥 Upload File", type="primary")
    with c2:
        st.button("📂 Browse Files")
    with c3:
        st.button("🔄 Reset")
    
    st.divider()
    
    # STATUS EXAMPLES
    st.subheader("Status indicators")
    st.success("✓ **Success:** Data imported: 1,234 proteins")
    st.warning("⚠ **Warning:** 15% missing values detected")
    st.info("ℹ **Info:** Processing starts after validation")
    st.error("✕ **Error:** File format not recognized")

with tab2:
    st.info("Module 2: Quality Control - Coming soon")

with tab3:
    st.info("Module 3: Preprocessing - Coming soon")

with tab4:
    st.info("Module 4: Analysis - Coming soon")

# FOOTER
st.divider()
st.markdown(f"""
<div style="text-align:center; padding:20px; color:{PRIMARY_GRAY}; font-size:12px;">
    <strong>Proprietary & Confidential | For Internal Use Only</strong><br>
    © 2024 Thermo Fisher Scientific Inc.
</div>
""", unsafe_allow_html=True)
