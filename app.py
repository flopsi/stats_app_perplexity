import streamlit as st

# ============================================================
# THERMO FISHER BRAND COLORS
# ============================================================
PRIMARY_RED = "#E71316"
DARK_RED = "#A6192E"
PRIMARY_GRAY = "#54585A"
LIGHT_GRAY = "#E2E3E4"
NAVY = "#262262"
ORANGE = "#EA7600"
YELLOW = "#F1B434"
GREEN = "#B5BD00"

# ============================================================
# EXACT CSS FROM HTML MOCKUP
# ============================================================
st.markdown(f"""
<style>
    * {{
        font-family: Arial, -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
    }}
    body {{
        background-color: #f8f9fa;
    }}
    .module-header {{
        background: linear-gradient(90deg, {PRIMARY_RED} 0%, {DARK_RED} 100%);
        padding: 30px;
        border-radius: 8px;
        margin-bottom: 40px;
        color: white;
        display: flex;
        align-items: center;
        gap: 20px;
    }}
    .module-icon {{
        width: 60px;
        height: 60px;
        background-color: rgba(255,255,255,0.2);
        border-radius: 8px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 32px;
    }}
    .module-info h2 {{
        margin: 0;
        font-size: 24px;
        color: white;
    }}
    .module-info p {{
        margin: 5px 0 0 0;
        opacity: 0.9;
        font-size: 15px;
    }}
    .stButton > button {{
        padding: 12px 24px;
        border-radius: 6px;
        font-size: 14px;
        font-weight: 500;
    }}
    .stButton > button[kind="primary"] {{
        background-color: {PRIMARY_RED};
        color: white;
    }}
    .stButton > button[kind="primary"]:hover {{
        background-color: {DARK_RED};
    }}
</style>
""", unsafe_allow_html=True)

# ============================================================
# HEADER BANNER
# ============================================================
st.markdown(f"""
<div style="background-color: {PRIMARY_RED}; padding: 20px 40px; margin: -1rem -1rem 2rem -1rem; color: white;">
    <h1 style="margin: 0; font-size: 28px; font-weight: 600;">DIA Proteomics Analysis Pipeline</h1>
    <p style="margin: 5px 0 0 0; font-size: 14px; opacity: 0.95;">Module demonstrations and UI components</p>
</div>
""", unsafe_allow_html=True)

# ============================================================
# NAVIGATION TABS (st.tabs)
# ============================================================
nav_tabs = st.tabs([
    "Module 1: Data Import",
    "Module 2: Quality Control",
    "Module 3: Preprocessing",
    "Module 4: Analysis"
])

with nav_tabs[0]:
    # ============================================================
    # MODULE HEADER (gradient with icon)
    # ============================================================
    st.markdown("""
    <div class="module-header">
        <div class="module-icon">📥</div>
        <div class="module-info">
            <h2>Module 1: Data Import & Validation</h2>
            <p>Import mass spectrometry output matrices with automatic format detection and validation</p>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # ============================================================
    # WORKFLOW STEPS GRID (static 4-column)
    # ============================================================
    st.markdown("### Workflow Steps")
    cols = st.columns(4)
    with cols[0]:
        st.markdown(f"""
        <div style="background-color: white; border: 1px solid {LIGHT_GRAY}; border-radius: 8px; padding: 25px;">
            <div style="width: 40px; height: 40px; background-color: {PRIMARY_RED}; color: white; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-weight: 600; font-size: 18px; margin-bottom: 15px;">1</div>
            <div style="font-size: 48px; margin-bottom: 15px; opacity: 0.7;">📁</div>
            <h3 style="font-size: 18px; color: {PRIMARY_GRAY}; margin-bottom: 12px;">File upload</h3>
            <p style="font-size: 14px; color: {PRIMARY_GRAY};">Drag and drop or browse to upload CSV files from Spectronaut, DIA-NN, MaxQuant, or FragPipe</p>
        </div>
        """, unsafe_allow_html=True)
    with cols[1]:
        st.markdown(f"""
        <div style="background-color: white; border: 1px solid {LIGHT_GRAY}; border-radius: 8px; padding: 25px;">
            <div style="width: 40px; height: 40px; background-color: {PRIMARY_RED}; color: white; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-weight: 600; font-size: 18px; margin-bottom: 15px;">2</div>
            <div style="font-size: 48px; margin-bottom: 15px; opacity: 0.7;">🔍</div>
            <h3 style="font-size: 18px; color: {PRIMARY_GRAY}; margin-bottom: 12px;">Format detection</h3>
            <p style="font-size: 14px; color: {PRIMARY_GRAY};">Automatic identification of file format using header patterns and column structure analysis</p>
        </div>
        """, unsafe_allow_html=True)
    with cols[2]:
        st.markdown(f"""
        <div style="background-color: white; border: 1px solid {LIGHT_GRAY}; border-radius: 8px; padding: 25px;">
            <div style="width: 40px; height: 40px; background-color: {PRIMARY_RED}; color: white; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-weight: 600; font-size: 18px; margin-bottom: 15px;">3</div>
            <div style="font-size: 48px; margin-bottom: 15px; opacity: 0.7;">✓</div>
            <h3 style="font-size: 18px; color: {PRIMARY_GRAY}; margin-bottom: 12px;">Data validation</h3>
            <p style="font-size: 14px; color: {PRIMARY_GRAY};">Verify data integrity, check for missing values, and validate against expected schema</p>
        </div>
        """, unsafe_allow_html=True)
    with cols[3]:
        st.markdown(f"""
        <div style="background-color: white; border: 1px solid {LIGHT_GRAY}; border-radius: 8px; padding: 25px;">
            <div style="width: 40px; height: 40px; background-color: {PRIMARY_RED}; color: white; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-weight: 600; font-size: 18px; margin-bottom: 15px;">4</div>
            <div style="font-size: 48px; margin-bottom: 15px; opacity: 0.7;">📋</div>
            <h3 style="font-size: 18px; color: {PRIMARY_GRAY}; margin-bottom: 12px;">Preview & confirm</h3>
            <p style="font-size: 14px; color: {PRIMARY_GRAY};">Review data summary statistics and column mappings before proceeding to analysis</p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # KEY FEATURES
    with st.container(border=True):
        st.markdown("### Key features")
        st.divider()
        col1, col2 = st.columns(2)
        with col1:
            st.markdown(f"""
            <div style="display: flex; gap: 15px; margin-bottom: 20px;">
                <div style="width: 40px; height: 40px; background-color: rgba(231, 19, 22, 0.1); border-radius: 6px; display: flex; align-items: center; justify-content: center; font-size: 20px;">🔄</div>
                <div><h4 style="font-size: 15px; font-weight: 600;">Multi-format support</h4><p style="font-size: 13px; opacity: 0.8;">Handles DIA-NN, Spectronaut, MaxQuant, and FragPipe output formats automatically</p></div>
            </div>
            """, unsafe_allow_html=True)
            st.markdown(f"""
            <div style="display: flex; gap: 15px; margin-bottom: 20px;">
                <div style="width: 40px; height: 40px; background-color: rgba(231, 19, 22, 0.1); border-radius: 6px; display: flex; align-items: center; justify-content: center; font-size: 20px;">🛡️</div>
                <div><h4 style="font-size: 15px; font-weight: 600;">File validation</h4><p style="font-size: 13px; opacity: 0.8;">Validates uploaded files against expected schema and data types</p></div>
            </div>
            """, unsafe_allow_html=True)
            st.markdown(f"""
            <div style="display: flex; gap: 15px; margin-bottom: 20px;">
                <div style="width: 40px; height: 40px; background-color: rgba(231, 19, 22, 0.1); border-radius: 6px; display: flex; align-items: center; justify-content: center; font-size: 20px;">📊</div>
                <div><h4 style="font-size: 15px; font-weight: 600;">Preliminary statistics</h4><p style="font-size: 13px; opacity: 0.8;">Generates summary stats including total entries and column types</p></div>
            </div>
            """, unsafe_allow_html=True)
        with col2:
            st.markdown(f"""
            <div style="display: flex; gap: 15px; margin-bottom: 20px;">
                <div style="width: 40px; height: 40px; background-color: rgba(231, 19, 22, 0.1); border-radius: 6px; display: flex; align-items: center; justify-content: center; font-size: 20px;">🎯</div>
                <div><h4 style="font-size: 15px; font-weight: 600;">Automatic column detection</h4><p style="font-size: 13px; opacity: 0.8;">Uses regex patterns to identify and map columns to standardized names</p></div>
            </div>
            """, unsafe_allow_html=True)
            st.markdown(f"""
            <div style="display: flex; gap: 15px; margin-bottom: 20px;">
                <div style="width: 40px; height: 40px; background-color: rgba(231, 19, 22, 0.1); border-radius: 6px; display: flex; align-items: center; justify-content: center; font-size: 20px;">✏️</div>
                <div><h4 style="font-size: 15px; font-weight: 600;">Sample name cleanup</h4><p style="font-size: 13px; opacity: 0.8;">Automatically extracts and standardizes sample names from headers</p></div>
            </div>
            """, unsafe_allow_html=True)
            st.markdown(f"""
            <div style="display: flex; gap: 15px; margin-bottom: 20px;">
                <div style="width: 40px; height: 40px; background-color: rgba(231, 19, 22, 0.1); border-radius: 6px; display: flex; align-items: center; justify-content: center; font-size: 20px;">👁️</div>
                <div><h4 style="font-size: 15px; font-weight: 600;">Data preview</h4><p style="font-size: 13px; opacity: 0.8;">Interactive preview with filtering and sorting capabilities</p></div>
            </div>
            """, unsafe_allow_html=True)

    # UPLOAD DEMO SECTION 
    with st.container(border=True):
        st.markdown("### Upload demonstration")
        uploaded_file = st.file_uploader(
            "Drop CSV file here or click to browse",
            type=["csv"],
            help="Supports .csv files from Spectronaut, DIA-NN, MaxQuant, FragPipe"
        )
        col1, col2, col3 = st.columns(3)
        with col1:
            st.button("📥 Upload File", type="primary")
        with col2:
            st.button("📂 Browse Files")
        with col3:
            st.button("🔄 Reset")

    # UI COMPONENT EXAMPLES
    with st.container(border=True):
        st.markdown("### UI component examples")
        st.divider()

        st.markdown("#### Buttons")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.button("Primary Action", type="primary", key="demo_btn_1")
        with col2:
            st.button("Secondary Action", key="demo_btn_2")
        with col3:
            st.button("Outline Button", key="demo_btn_3")

        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("#### Status indicators")
        st.success("✓ **Success:** Data imported successfully: 1,234 proteins quantified")
        st.warning("⚠ **Warning:** 15% missing values detected in the dataset")
        st.info("ℹ **Info:** Upload will begin processing automatically after validation")
        st.error("✕ **Error:** File format not recognized. Please upload a valid CSV file")

# Tabs 2-4: Placeholder
with nav_tabs[1]:
    st.info("Module 2: Quality Control - Coming soon")
with nav_tabs[2]:
    st.info("Module 3: Preprocessing - Coming soon")
with nav_tabs[3]:
    st.info("Module 4: Analysis - Coming soon")

# FOOTER
st.divider()
st.markdown(f"""
<div style="text-align: center; padding: 30px; color: {PRIMARY_GRAY}; font-size: 12px;">
    <strong style="display: block; margin-bottom: 10px;">Proprietary & Confidential | For Internal Use Only</strong>
    <p>© 2024 Thermo Fisher Scientific Inc. All rights reserved.</p>
</div>
""", unsafe_allow_html=True)
