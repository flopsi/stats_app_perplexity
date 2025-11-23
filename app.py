import streamlit as st
import pandas as pd
import numpy as np

# ============================================================
# PAGE CONFIG
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
GREEN = "#B5BD00"
ORANGE = "#EA7600"

# ============================================================
# SESSION STATE INITIALIZATION
# ============================================================
if 'uploaded_data' not in st.session_state:
    st.session_state.uploaded_data = None
if 'column_annotations' not in st.session_state:
    st.session_state.column_annotations = {}
if 'show_annotation' not in st.session_state:
    st.session_state.show_annotation = False

# ============================================================
# CACHED CSS
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
            border-radius: 6px; font-weight: 500; border: none;
        }}
        .stButton > button[kind="primary"]:hover {{background-color: {DARK_RED};}}
    </style>
    """

st.markdown(load_css(), unsafe_allow_html=True)

# ============================================================
# HELPER FUNCTIONS
# ============================================================
def detect_column_types(df):
    """Detect metadata vs numerical columns"""
    metadata_cols = []
    numerical_cols = []
    
    for col in df.columns:
        numeric_values = pd.to_numeric(df[col], errors='coerce')
        if numeric_values.isna().all():
            metadata_cols.append(col)
        else:
            numerical_cols.append(col)
    
    return metadata_cols, numerical_cols

def auto_annotate_columns(numerical_cols):
    """Auto-assign Control/Treatment based on position"""
    annotations = {}
    midpoint = len(numerical_cols) // 2
    
    for idx, col in enumerate(numerical_cols):
        if idx < midpoint:
            annotations[col] = {
                'condition': 'Control',
                'renamed': f'C{idx + 1}'
            }
        else:
            annotations[col] = {
                'condition': 'Treatment',
                'renamed': f'T{idx - midpoint + 1}'
            }
    
    return annotations

# ============================================================
# HEADER
# ============================================================
st.markdown(f"""
<div style="background: {PRIMARY_RED}; padding: 20px; margin: -1rem -1rem 2rem -1rem; color: white;">
    <h1 style="margin: 0; font-size: 28px;">🧬 DIA Proteomics Analysis Pipeline</h1>
    <p style="margin: 5px 0 0 0; font-size: 14px;">Module 1: Data Import & Annotation</p>
</div>
""", unsafe_allow_html=True)

# ============================================================
# MODULE HEADER
# ============================================================
st.markdown("""
<div class="module-header">
    <h2 style="margin:0; font-size:24px;">📥 Data Import & Validation</h2>
    <p style="margin:5px 0 0 0; opacity:0.9;">Import mass spectrometry data with automatic format detection</p>
</div>
""", unsafe_allow_html=True)

# ============================================================
# FILE UPLOAD SECTION
# ============================================================
st.subheader("📁 Step 1: Upload Data File")

uploaded_file = st.file_uploader(
    "Drop CSV or TSV file here",
    type=["csv", "tsv", "txt"],
    help="Supports CSV/TSV files from Spectronaut, DIA-NN, MaxQuant, FragPipe"
)

if uploaded_file is not None:
    try:
        # Detect separator
        sep = "\t" if uploaded_file.name.endswith((".tsv", ".txt")) else ","
        df = pd.read_csv(uploaded_file, sep=sep)
        
        st.session_state.uploaded_data = df
        st.session_state.show_annotation = True
        
        # Success message
        st.success(f"✓ **File loaded:** {uploaded_file.name} • {len(df):,} rows • {len(df.columns)} columns")
        
        # Summary metrics
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Rows", f"{len(df):,}")
        with col2:
            st.metric("Total Columns", len(df.columns))
        with col3:
            st.metric("File Size", f"{df.memory_usage(deep=True).sum() / 1024**2:.1f} MB")
        
        st.divider()
        
        # ============================================================
        # COLUMN DETECTION
        # ============================================================
        st.subheader("🔍 Step 2: Column Detection")
        
        metadata_cols, numerical_cols = detect_column_types(df)
        
        col1, col2 = st.columns(2)
        with col1:
            st.metric("📋 Metadata Columns", len(metadata_cols))
            with st.expander("View metadata columns"):
                for col in metadata_cols:
                    st.text(f"• {col}")
        
        with col2:
            st.metric("📊 Numerical Columns", len(numerical_cols))
            with st.expander("View numerical columns"):
                for col in numerical_cols:
                    st.text(f"• {col}")
        
        st.divider()
        
        # ============================================================
        # COLUMN ANNOTATION
        # ============================================================
        st.subheader("🗂️ Step 3: Annotate Numerical Columns")
        
        st.info("ℹ **Auto-annotation:** First half → Control (C1, C2...) • Second half → Treatment (T1, T2...)")
        
        # Auto-annotate if not already done
        if not st.session_state.column_annotations and len(numerical_cols) > 0:
            st.session_state.column_annotations = auto_annotate_columns(numerical_cols)
        
        # Annotation table header
        col1, col2, col3 = st.columns([3, 2, 2])
        with col1:
            st.markdown("**Original Column**")
        with col2:
            st.markdown("**Rename To**")
        with col3:
            st.markdown("**Condition**")
        
        st.markdown("---")
        
        # Annotation rows
        annotations = st.session_state.column_annotations.copy()
        
        for col in numerical_cols:
            if col not in annotations:
                annotations[col] = {'condition': 'Control', 'renamed': col}
            
            row_col1, row_col2, row_col3 = st.columns([3, 2, 2])
            
            with row_col1:
                sample_vals = df[col].dropna().head(2).tolist()
                sample_str = ", ".join([f"{v:.2e}" if isinstance(v, (int, float)) else str(v)[:15] for v in sample_vals])
                st.text(col)
                st.caption(f"Sample: {sample_str}")
            
            with row_col2:
                new_name = st.text_input(
                    "Rename",
                    value=annotations[col]['renamed'],
                    key=f"rename_{col}",
                    label_visibility="collapsed"
                )
                annotations[col]['renamed'] = new_name
            
            with row_col3:
                condition = st.selectbox(
                    "Condition",
                    options=["Control", "Treatment"],
                    index=0 if annotations[col]['condition'] == 'Control' else 1,
                    key=f"cond_{col}",
                    label_visibility="collapsed"
                )
                annotations[col]['condition'] = condition
        
        st.session_state.column_annotations = annotations
        
        st.divider()
        
        # ============================================================
        # ANNOTATION SUMMARY
        # ============================================================
        st.subheader("📋 Annotation Summary")
        
        summary_data = []
        for col in numerical_cols:
            ann = annotations.get(col, {'renamed': col, 'condition': 'Unknown'})
            summary_data.append({
                'Original': col,
                'Renamed': ann['renamed'],
                'Condition': ann['condition']
            })
        
        summary_df = pd.DataFrame(summary_data)
        st.dataframe(summary_df, use_container_width=True, hide_index=True)
        
        n_control = sum(1 for ann in annotations.values() if ann['condition'] == 'Control')
        n_treatment = sum(1 for ann in annotations.values() if ann['condition'] == 'Treatment')
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Numerical Columns", len(numerical_cols))
        with col2:
            st.metric("Control Samples", n_control)
        with col3:
            st.metric("Treatment Samples", n_treatment)
        with col4:
            st.metric("Metadata Columns", len(metadata_cols))
        
        st.divider()
        
        # ============================================================
        # DATA PREVIEW
        # ============================================================
        st.subheader("👁️ Step 4: Data Preview")
        
        preview_rows = st.slider("Number of rows to preview", 5, 50, 10)
        st.dataframe(df.head(preview_rows), use_container_width=True)
        
        st.divider()
        
        # ============================================================
        # NEXT STEPS
        # ============================================================
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("🔄 Reset and Upload New File", use_container_width=True):
                st.session_state.uploaded_data = None
                st.session_state.column_annotations = {}
                st.session_state.show_annotation = False
                st.rerun()
        
        with col2:
            st.button("Next: Quality Control ➡️", type="primary", use_container_width=True, disabled=True)
            st.caption("Quality control module coming soon")
        
    except Exception as e:
        st.error(f"✕ **Error loading file:** {str(e)}")
        st.info("💡 **Tip:** Ensure your file is a valid CSV or TSV format")

else:
    # ============================================================
    # WORKFLOW STEPS (when no file uploaded)
    # ============================================================
    st.subheader("Workflow Overview")
    
    c1, c2, c3, c4 = st.columns(4)
    
    with c1:
        st.markdown("**1️⃣ File upload**")
        st.caption("📁 Upload CSV/TSV from mass spec software")
    with c2:
        st.markdown("**2️⃣ Column detection**")
        st.caption("🔍 Auto-detect metadata vs numerical")
    with c3:
        st.markdown("**3️⃣ Annotation**")
        st.caption("🗂️ Assign conditions and rename")
    with c4:
        st.markdown("**4️⃣ Preview**")
        st.caption("👁️ Review before proceeding")
    
    st.divider()
    
    # KEY FEATURES
    st.subheader("Key Features")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("🔄 **Multi-format support**")
        st.caption("DIA-NN, Spectronaut, MaxQuant, FragPipe")
        
        st.markdown("🛡️ **Automatic validation**")
        st.caption("Schema and data type checking")
        
        st.markdown("📊 **Smart detection**")
        st.caption("Auto-identify column types")
    
    with col2:
        st.markdown("🎯 **Auto-annotation**")
        st.caption("Intelligent condition assignment")
        
        st.markdown("✏️ **Flexible renaming**")
        st.caption("Customize sample names")
        
        st.markdown("👁️ **Interactive preview**")
        st.caption("Review data before analysis")

# ============================================================
# FOOTER
# ============================================================
st.divider()
st.markdown(f"""
<div style="text-align:center; padding:20px; color:{PRIMARY_GRAY}; font-size:12px;">
    <strong>Proprietary & Confidential | For Internal Use Only</strong><br>
    © 2024 Thermo Fisher Scientific Inc. All rights reserved.
</div>
""", unsafe_allow_html=True)
