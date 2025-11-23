import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from scipy import stats
from sklearn.decomposition import PCA

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
SKY = "#9BD3DD"

# ============================================================
# SESSION STATE INITIALIZATION
# ============================================================
if 'uploaded_data' not in st.session_state:
    st.session_state.uploaded_data = None
if 'column_annotations' not in st.session_state:
    st.session_state.column_annotations = {}
if 'current_module' not in st.session_state:
    st.session_state.current_module = 'upload'

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
# HELPER FUNCTIONS - DATA PROCESSING
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
            annotations[col] = {'condition': 'Control', 'renamed': f'C{idx + 1}'}
        else:
            annotations[col] = {'condition': 'Treatment', 'renamed': f'T{idx - midpoint + 1}'}
    
    return annotations

def clean_intensity_data(df, numerical_cols):
    """Treat 0, 1, and NaN as missing values"""
    df_clean = df[numerical_cols].copy()
    df_clean = df_clean.replace([0, 1], np.nan)
    return df_clean

# ============================================================
# PLOTTING FUNCTIONS
# ============================================================
@st.cache_data
def plot_unique_proteins(df, numerical_cols):
    """Plot 1: Unique proteins detected"""
    df_clean = clean_intensity_data(df, numerical_cols)
    
    counts = []
    for col in numerical_cols:
        count = df_clean[col].notna().sum()
        counts.append(count)
    
    fig = go.Figure(data=[
        go.Bar(x=numerical_cols, y=counts, marker_color=PRIMARY_RED)
    ])
    
    fig.update_layout(
        title="Unique Proteins Detected per Sample",
        xaxis_title="Sample",
        yaxis_title="Number of Proteins",
        height=400,
        template="plotly_white"
    )
    
    return fig

@st.cache_data
def plot_intensity_distribution(df, numerical_cols, annotations):
    """Plot 2: Intensity distribution violin plot"""
    df_clean = clean_intensity_data(df, numerical_cols)
    
    data_list = []
    for col in numerical_cols:
        condition = annotations[col]['condition']
        renamed = annotations[col]['renamed']
        values = df_clean[col].dropna()
        log_values = np.log10(values[values > 0])
        
        for val in log_values:
            data_list.append({
                'Sample': renamed,
                'Condition': condition,
                'Log10 Intensity': val
            })
    
    plot_df = pd.DataFrame(data_list)
    
    fig = px.violin(
        plot_df,
        x='Sample',
        y='Log10 Intensity',
        color='Condition',
        color_discrete_map={'Control': SKY, 'Treatment': DARK_RED},
        box=True,
        points=False
    )
    
    fig.update_layout(
        title="Intensity Distribution (Log10)",
        height=500,
        template="plotly_white"
    )
    
    return fig

@st.cache_data
def plot_cv_analysis(df, numerical_cols, annotations):
    """Plot 3: Coefficient of Variation"""
    df_clean = clean_intensity_data(df, numerical_cols)
    
    control_cols = [col for col in numerical_cols if annotations[col]['condition'] == 'Control']
    treatment_cols = [col for col in numerical_cols if annotations[col]['condition'] == 'Treatment']
    
    cv_data = []
    
    for idx, row in df_clean.iterrows():
        # Control CV
        control_vals = row[control_cols].dropna()
        if len(control_vals) > 1:
            cv_control = (control_vals.std() / control_vals.mean()) * 100
            cv_data.append({'Condition': 'Control', 'CV (%)': cv_control})
        
        # Treatment CV
        treatment_vals = row[treatment_cols].dropna()
        if len(treatment_vals) > 1:
            cv_treatment = (treatment_vals.std() / treatment_vals.mean()) * 100
            cv_data.append({'Condition': 'Treatment', 'CV (%)': cv_treatment})
    
    cv_df = pd.DataFrame(cv_data)
    
    fig = px.violin(
        cv_df,
        x='Condition',
        y='CV (%)',
        color='Condition',
        color_discrete_map={'Control': SKY, 'Treatment': DARK_RED},
        box=True,
        points=False
    )
    
    fig.update_layout(
        title="Coefficient of Variation by Condition",
        height=500,
        template="plotly_white"
    )
    
    return fig

@st.cache_data
def plot_pca(df, numerical_cols, annotations):
    """Plot 4: PCA clustering"""
    df_clean = clean_intensity_data(df, numerical_cols)
    
    # Remove rows with too many missing values
    df_pca = df_clean.dropna(thresh=len(numerical_cols) * 0.5)
    df_pca = df_pca.fillna(df_pca.mean())
    
    # Transpose for PCA (samples as rows)
    data_transposed = df_pca.T
    
    # Perform PCA
    pca = PCA(n_components=2)
    components = pca.fit_transform(data_transposed)
    
    # Create plot data
    plot_data = []
    for idx, col in enumerate(numerical_cols):
        plot_data.append({
            'PC1': components[idx, 0],
            'PC2': components[idx, 1],
            'Sample': annotations[col]['renamed'],
            'Condition': annotations[col]['condition']
        })
    
    plot_df = pd.DataFrame(plot_data)
    
    fig = px.scatter(
        plot_df,
        x='PC1',
        y='PC2',
        color='Condition',
        text='Sample',
        color_discrete_map={'Control': SKY, 'Treatment': DARK_RED},
        size_max=15
    )
    
    fig.update_traces(marker=dict(size=12), textposition='top center')
    
    fig.update_layout(
        title=f"PCA: Sample Clustering (PC1: {pca.explained_variance_ratio_[0]:.1%}, PC2: {pca.explained_variance_ratio_[1]:.1%})",
        height=500,
        template="plotly_white"
    )
    
    return fig

# ============================================================
# HEADER
# ============================================================
st.markdown(f"""
<div style="background: {PRIMARY_RED}; padding: 20px; margin: -1rem -1rem 2rem -1rem; color: white;">
    <h1 style="margin: 0; font-size: 28px;">🧬 DIA Proteomics Analysis Pipeline</h1>
    <p style="margin: 5px 0 0 0; font-size: 14px;">Multi-Module Data Analysis Platform</p>
</div>
""", unsafe_allow_html=True)

# ============================================================
# MODULE SELECTION
# ============================================================
tab1, tab2 = st.tabs(["📁 Module 1: Data Import", "📊 Module 2: Quality Control"])

# ============================================================
# MODULE 1: DATA IMPORT
# ============================================================
with tab1:
    st.markdown("""
    <div class="module-header">
        <h2 style="margin:0; font-size:24px;">📥 Data Import & Validation</h2>
        <p style="margin:5px 0 0 0; opacity:0.9;">Import mass spectrometry data with automatic format detection</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.subheader("📁 Step 1: Upload Data File")
    
    uploaded_file = st.file_uploader(
        "Drop CSV or TSV file here",
        type=["csv", "tsv", "txt"],
        help="Supports CSV/TSV files from Spectronaut, DIA-NN, MaxQuant, FragPipe"
    )
    
    if uploaded_file is not None:
        try:
            sep = "\t" if uploaded_file.name.endswith((".tsv", ".txt")) else ","
            df = pd.read_csv(uploaded_file, sep=sep)
            
            st.session_state.uploaded_data = df
            
            st.success(f"✓ **File loaded:** {uploaded_file.name} • {len(df):,} rows • {len(df.columns)} columns")
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Total Rows", f"{len(df):,}")
            with col2:
                st.metric("Total Columns", len(df.columns))
            with col3:
                st.metric("File Size", f"{df.memory_usage(deep=True).sum() / 1024**2:.1f} MB")
            
            st.divider()
            
            # Column Detection
            st.subheader("🔍 Step 2: Column Detection")
            metadata_cols, numerical_cols = detect_column_types(df)
            
            col1, col2 = st.columns(2)
            with col1:
                st.metric("📋 Metadata Columns", len(metadata_cols))
            with col2:
                st.metric("📊 Numerical Columns", len(numerical_cols))
            
            st.divider()
            
            # Column Annotation
            st.subheader("🗂️ Step 3: Annotate Numerical Columns")
            st.info("ℹ **Auto-annotation:** First half → Control • Second half → Treatment")
            
            if not st.session_state.column_annotations and len(numerical_cols) > 0:
                st.session_state.column_annotations = auto_annotate_columns(numerical_cols)
            
            col1, col2, col3 = st.columns([3, 2, 2])
            with col1:
                st.markdown("**Original Column**")
            with col2:
                st.markdown("**Rename To**")
            with col3:
                st.markdown("**Condition**")
            
            st.markdown("---")
            
            annotations = st.session_state.column_annotations.copy()
            
            for col in numerical_cols:
                if col not in annotations:
                    annotations[col] = {'condition': 'Control', 'renamed': col}
                
                row_col1, row_col2, row_col3 = st.columns([3, 2, 2])
                
                with row_col1:
                    st.text(col)
                
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
            
            # Summary
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
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Numerical Columns", len(numerical_cols))
            with col2:
                st.metric("Control Samples", n_control)
            with col3:
                st.metric("Treatment Samples", n_treatment)
            
        except Exception as e:
            st.error(f"✕ **Error:** {str(e)}")

# ============================================================
# MODULE 2: QUALITY CONTROL
# ============================================================
with tab2:
    st.markdown("""
    <div class="module-header">
        <h2 style="margin:0; font-size:24px;">📊 Quality Control Visualization</h2>
        <p style="margin:5px 0 0 0; opacity:0.9;">Comprehensive data quality assessment with 4 key plots</p>
    </div>
    """, unsafe_allow_html=True)
    
    if st.session_state.uploaded_data is not None and st.session_state.column_annotations:
        df = st.session_state.uploaded_data
        metadata_cols, numerical_cols = detect_column_types(df)
        annotations = st.session_state.column_annotations
        
        st.info("ℹ **Data processing:** Values 0, 1, and NaN are treated as missing")
        
        st.divider()
        
        # Plot 1
        st.subheader("1️⃣ Unique Proteins Detected")
        fig1 = plot_unique_proteins(df, numerical_cols)
        st.plotly_chart(fig1, use_container_width=True)
        
        st.divider()
        
        # Plot 2
        st.subheader("2️⃣ Intensity Distribution")
        fig2 = plot_intensity_distribution(df, numerical_cols, annotations)
        st.plotly_chart(fig2, use_container_width=True)
        
        st.divider()
        
        # Plot 3
        st.subheader("3️⃣ Coefficient of Variation (CV)")
        fig3 = plot_cv_analysis(df, numerical_cols, annotations)
        st.plotly_chart(fig3, use_container_width=True)
        
        cv_threshold = st.slider("CV threshold for high variability (%)", 10, 200, 100)
        st.caption(f"Proteins with CV > {cv_threshold}% indicate high variability")
        
        st.divider()
        
        # Plot 4
        st.subheader("4️⃣ PCA: Sample Clustering")
        fig4 = plot_pca(df, numerical_cols, annotations)
        st.plotly_chart(fig4, use_container_width=True)
        
    else:
        st.warning("⚠️ **No data uploaded.** Please upload data in Module 1 first.")

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
