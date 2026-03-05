"""
Page 1 — Distribution Plots
============================
Histogram, KDE Plot, Boxplot, Violin Plot — interactive Seaborn demos.
"""

import streamlit as st
import seaborn as sns
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import sys, os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from utils.styles import inject_custom_css, hero, step_header
from utils.helpers import show_code, show_explanation, load_gallery_images, image_gallery

st.set_page_config(page_title="Distribution Plots", page_icon="📊", layout="wide")
inject_custom_css()
hero("📊 Distribution Plots", "Histogram · KDE · Boxplot · Violin — understand how your data is spread")

# ── Dataset selector ──
dataset_name = st.sidebar.selectbox("Dataset", ["tips", "iris", "penguins", "diamonds"], key="dist_ds")

@st.cache_data
def load_dataset(name):
    return sns.load_dataset(name)

df = load_dataset(dataset_name)
num_cols = df.select_dtypes(include=[np.number]).columns.tolist()
cat_cols = df.select_dtypes(include=["category", "object"]).columns.tolist()

palette_options = ["deep", "muted", "pastel", "bright", "dark", "colorblind",
                   "Set2", "Set3", "husl", "coolwarm", "viridis", "magma", "rocket"]

tabs = st.tabs(["📶 Histogram", "🌊 KDE Plot", "📦 Boxplot", "🎻 Violin Plot"])

# ═══════════════════════════════════════════════════════
# TAB 1 — Histogram
# ═══════════════════════════════════════════════════════
with tabs[0]:
    step_header(1, "Histogram — Frequency Distributions")
    show_explanation(
        "A histogram divides data into bins and counts observations per bin. "
        "Use <code>sns.histplot()</code> with <code>kde=True</code> to overlay a smooth density curve."
    )

    c1, c2, c3, c4 = st.columns(4)
    col_hist = c1.selectbox("Column", num_cols, key="hist_col")
    bins_hist = c2.slider("Bins", 5, 60, 20, key="hist_bins")
    hue_hist = c3.selectbox("Hue", [None] + cat_cols, key="hist_hue")
    pal_hist = c4.selectbox("Palette", palette_options, key="hist_pal")
    kde_on = st.checkbox("Overlay KDE curve", value=True, key="hist_kde")

    fig, ax = plt.subplots(figsize=(10, 5))
    sns.histplot(data=df, x=col_hist, bins=bins_hist, hue=hue_hist,
                 palette=pal_hist, kde=kde_on, ax=ax, edgecolor="white", linewidth=0.5)
    ax.set_title(f"Histogram — {col_hist}", fontweight="bold", fontsize=13)
    plt.tight_layout()
    st.pyplot(fig)
    plt.close(fig)

    show_code(f"sns.histplot(data=df, x='{col_hist}', bins={bins_hist}, hue={repr(hue_hist)}, kde={kde_on}, palette='{pal_hist}')")

    with st.expander("📸 Notebook Outputs — Histogram"):
        image_gallery(load_gallery_images("Histogram"), cols=4)

# ═══════════════════════════════════════════════════════
# TAB 2 — KDE Plot
# ═══════════════════════════════════════════════════════
with tabs[1]:
    step_header(2, "KDE Plot — Smooth Density Curves")
    show_explanation(
        "Kernel Density Estimation (KDE) produces a smooth probability density curve. "
        "Use <code>sns.kdeplot()</code> with <code>fill=True</code> for shaded areas."
    )

    c1, c2, c3 = st.columns(3)
    col_kde = c1.selectbox("Column", num_cols, key="kde_col")
    hue_kde = c2.selectbox("Hue", [None] + cat_cols, key="kde_hue")
    pal_kde = c3.selectbox("Palette", palette_options, key="kde_pal")
    fill_kde = st.checkbox("Fill under curve", value=True, key="kde_fill")
    bw_kde = st.slider("Bandwidth adjust", 0.2, 3.0, 1.0, 0.1, key="kde_bw")

    fig, ax = plt.subplots(figsize=(10, 5))
    sns.kdeplot(data=df, x=col_kde, hue=hue_kde, palette=pal_kde,
                fill=fill_kde, bw_adjust=bw_kde, ax=ax, linewidth=2)
    ax.set_title(f"KDE Plot — {col_kde}", fontweight="bold", fontsize=13)
    plt.tight_layout()
    st.pyplot(fig)
    plt.close(fig)

    show_code(f"sns.kdeplot(data=df, x='{col_kde}', hue={repr(hue_kde)}, fill={fill_kde}, bw_adjust={bw_kde})")

    with st.expander("📸 Notebook Outputs — KDE Plot"):
        image_gallery(load_gallery_images("KDE Plot"), cols=4)

# ═══════════════════════════════════════════════════════
# TAB 3 — Boxplot
# ═══════════════════════════════════════════════════════
with tabs[2]:
    step_header(3, "Boxplot — Distributions & Outliers")
    show_explanation(
        "Box plots display median, quartiles, and outliers. "
        "Use <code>sns.boxplot()</code> with <code>orient</code> to switch horizontal/vertical."
    )

    c1, c2, c3, c4 = st.columns(4)
    col_box_y = c1.selectbox("Y (numeric)", num_cols, key="box_y")
    col_box_x = c2.selectbox("X (category)", [None] + cat_cols, key="box_x")
    hue_box = c3.selectbox("Hue", [None] + cat_cols, key="box_hue")
    pal_box = c4.selectbox("Palette", palette_options, key="box_pal")

    fig, ax = plt.subplots(figsize=(10, 5))
    sns.boxplot(data=df, x=col_box_x, y=col_box_y, hue=hue_box,
                palette=pal_box, ax=ax, linewidth=1.2)
    ax.set_title(f"Boxplot — {col_box_y}", fontweight="bold", fontsize=13)
    plt.tight_layout()
    st.pyplot(fig)
    plt.close(fig)

    show_code(f"sns.boxplot(data=df, x={repr(col_box_x)}, y='{col_box_y}', hue={repr(hue_box)}, palette='{pal_box}')")

    with st.expander("📸 Notebook Outputs — Boxplot"):
        image_gallery(load_gallery_images("Boxplot"), cols=4)

# ═══════════════════════════════════════════════════════
# TAB 4 — Violin Plot
# ═══════════════════════════════════════════════════════
with tabs[3]:
    step_header(4, "Violin Plot — Distribution Shape + Statistics")
    show_explanation(
        "Violin plots combine box plots with KDE, showing the distribution shape. "
        "Use <code>sns.violinplot()</code> with <code>split=True</code> for comparative halves."
    )

    c1, c2, c3, c4 = st.columns(4)
    col_vio_y = c1.selectbox("Y (numeric)", num_cols, key="vio_y")
    col_vio_x = c2.selectbox("X (category)", [None] + cat_cols, key="vio_x")
    hue_vio = c3.selectbox("Hue", [None] + cat_cols, key="vio_hue")
    pal_vio = c4.selectbox("Palette", palette_options, key="vio_pal")
    inner_vio = st.selectbox("Inner", ["box", "quart", "point", "stick", None], key="vio_inner")

    fig, ax = plt.subplots(figsize=(10, 5))
    sns.violinplot(data=df, x=col_vio_x, y=col_vio_y, hue=hue_vio,
                   palette=pal_vio, inner=inner_vio, ax=ax, linewidth=1.2)
    ax.set_title(f"Violin Plot — {col_vio_y}", fontweight="bold", fontsize=13)
    plt.tight_layout()
    st.pyplot(fig)
    plt.close(fig)

    show_code(f"sns.violinplot(data=df, x={repr(col_vio_x)}, y='{col_vio_y}', hue={repr(hue_vio)}, inner={repr(inner_vio)})")

    with st.expander("📸 Notebook Outputs — Violin Plot"):
        image_gallery(load_gallery_images("Violin Plot"), cols=4)
