"""
Page 2 — Categorical Plots
===========================
Bar Plot, Count Plot, Strip Plot, Swarm Plot — interactive Seaborn demos.
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

st.set_page_config(page_title="Categorical Plots", page_icon="📈", layout="wide")
inject_custom_css()
hero("📈 Categorical Plots", "Bar · Count · Strip · Swarm — compare categories with style")

# ── Dataset selector ──
dataset_name = st.sidebar.selectbox("Dataset", ["tips", "titanic", "penguins", "diamonds"], key="cat_ds")

@st.cache_data
def load_dataset(name):
    return sns.load_dataset(name)

df = load_dataset(dataset_name)
num_cols = df.select_dtypes(include=[np.number]).columns.tolist()
cat_cols = df.select_dtypes(include=["category", "object"]).columns.tolist()

palette_options = ["deep", "muted", "pastel", "bright", "dark", "colorblind",
                   "Set2", "Set3", "husl", "coolwarm", "viridis", "magma"]

tabs = st.tabs(["📊 Bar Plot", "🔢 Count Plot", "📍 Strip Plot", "🐝 Swarm Plot"])

# ═══════════════════════════════════════════════════════
# TAB 1 — Bar Plot
# ═══════════════════════════════════════════════════════
with tabs[0]:
    step_header(1, "Bar Plot — Compare Quantities")
    show_explanation(
        "Bar plots show an estimate of central tendency (mean by default) for a numeric variable "
        "grouped by a categorical variable. Use <code>sns.barplot()</code> with <code>estimator</code> to change the aggregation."
    )

    c1, c2, c3, c4 = st.columns(4)
    x_bar = c1.selectbox("X (category)", cat_cols, key="bar_x") if cat_cols else None
    y_bar = c2.selectbox("Y (numeric)", num_cols, key="bar_y")
    hue_bar = c3.selectbox("Hue", [None] + cat_cols, key="bar_hue")
    pal_bar = c4.selectbox("Palette", palette_options, key="bar_pal")
    est_bar = st.selectbox("Estimator", ["mean", "median", "sum", "max", "min"], key="bar_est")

    est_map = {"mean": np.mean, "median": np.median, "sum": np.sum, "max": np.max, "min": np.min}

    if x_bar:
        fig, ax = plt.subplots(figsize=(10, 5))
        sns.barplot(data=df, x=x_bar, y=y_bar, hue=hue_bar,
                    palette=pal_bar, estimator=est_map[est_bar], ax=ax, edgecolor="white", linewidth=0.5)
        ax.set_title(f"Bar Plot — {y_bar} by {x_bar}", fontweight="bold", fontsize=13)
        plt.xticks(rotation=45)
        plt.tight_layout()
        st.pyplot(fig)
        plt.close(fig)

        show_code(f"sns.barplot(data=df, x='{x_bar}', y='{y_bar}', hue={repr(hue_bar)}, estimator=np.{est_bar}, palette='{pal_bar}')")
    else:
        st.warning("No categorical columns found in this dataset.")

    with st.expander("📸 Notebook Outputs — Bar Plot"):
        image_gallery(load_gallery_images("Bar Plot"), cols=4)

# ═══════════════════════════════════════════════════════
# TAB 2 — Count Plot
# ═══════════════════════════════════════════════════════
with tabs[1]:
    step_header(2, "Count Plot — Category Frequencies")
    show_explanation(
        "Count plots show the number of observations in each category. "
        "It's essentially a histogram for categorical data. Use <code>sns.countplot()</code>."
    )

    c1, c2, c3 = st.columns(3)
    x_cnt = c1.selectbox("X (category)", cat_cols, key="cnt_x") if cat_cols else None
    hue_cnt = c2.selectbox("Hue", [None] + cat_cols, key="cnt_hue")
    pal_cnt = c3.selectbox("Palette", palette_options, key="cnt_pal")

    if x_cnt:
        fig, ax = plt.subplots(figsize=(10, 5))
        sns.countplot(data=df, x=x_cnt, hue=hue_cnt,
                      palette=pal_cnt, ax=ax, edgecolor="white", linewidth=0.5)
        ax.set_title(f"Count Plot — {x_cnt}", fontweight="bold", fontsize=13)
        plt.xticks(rotation=45)
        plt.tight_layout()
        st.pyplot(fig)
        plt.close(fig)

        show_code(f"sns.countplot(data=df, x='{x_cnt}', hue={repr(hue_cnt)}, palette='{pal_cnt}')")
    else:
        st.warning("No categorical columns found in this dataset.")

    with st.expander("📸 Notebook Outputs — Count Plot"):
        image_gallery(load_gallery_images("CountPlot"), cols=3)

# ═══════════════════════════════════════════════════════
# TAB 3 — Strip Plot
# ═══════════════════════════════════════════════════════
with tabs[2]:
    step_header(3, "Strip Plot — Individual Data Points")
    show_explanation(
        "Strip plots display individual observations as dots for each category. "
        "Use <code>sns.stripplot()</code> with <code>jitter</code> to reduce overlap."
    )

    c1, c2, c3, c4 = st.columns(4)
    y_strip = c1.selectbox("Y (numeric)", num_cols, key="strip_y")
    x_strip = c2.selectbox("X (category)", [None] + cat_cols, key="strip_x")
    hue_strip = c3.selectbox("Hue", [None] + cat_cols, key="strip_hue")
    pal_strip = c4.selectbox("Palette", palette_options, key="strip_pal")
    jitter_strip = st.slider("Jitter", 0.0, 0.5, 0.2, 0.05, key="strip_jitter")

    fig, ax = plt.subplots(figsize=(10, 5))
    sns.stripplot(data=df, x=x_strip, y=y_strip, hue=hue_strip,
                  palette=pal_strip, jitter=jitter_strip, ax=ax, alpha=0.7, size=5)
    ax.set_title(f"Strip Plot — {y_strip}", fontweight="bold", fontsize=13)
    plt.tight_layout()
    st.pyplot(fig)
    plt.close(fig)

    show_code(f"sns.stripplot(data=df, x={repr(x_strip)}, y='{y_strip}', hue={repr(hue_strip)}, jitter={jitter_strip})")

    with st.expander("📸 Notebook Outputs — Strip Plot"):
        image_gallery(load_gallery_images("Strip plot"), cols=3)

# ═══════════════════════════════════════════════════════
# TAB 4 — Swarm Plot
# ═══════════════════════════════════════════════════════
with tabs[3]:
    step_header(4, "Swarm Plot — Non-overlapping Scatter")
    show_explanation(
        "Swarm plots position dots to avoid overlap, giving a complete picture of the distribution. "
        "Use <code>sns.swarmplot()</code>. Works best with smaller datasets (< 500 points)."
    )

    c1, c2, c3, c4 = st.columns(4)
    y_swarm = c1.selectbox("Y (numeric)", num_cols, key="swarm_y")
    x_swarm = c2.selectbox("X (category)", [None] + cat_cols, key="swarm_x")
    hue_swarm = c3.selectbox("Hue", [None] + cat_cols, key="swarm_hue")
    pal_swarm = c4.selectbox("Palette", palette_options, key="swarm_pal")
    size_swarm = st.slider("Point size", 2, 10, 5, key="swarm_size")

    # Limit data for swarm plot performance
    df_swarm = df.sample(min(200, len(df)), random_state=42) if len(df) > 200 else df

    fig, ax = plt.subplots(figsize=(10, 5))
    sns.swarmplot(data=df_swarm, x=x_swarm, y=y_swarm, hue=hue_swarm,
                  palette=pal_swarm, size=size_swarm, ax=ax)
    ax.set_title(f"Swarm Plot — {y_swarm} (n={len(df_swarm)})", fontweight="bold", fontsize=13)
    plt.tight_layout()
    st.pyplot(fig)
    plt.close(fig)

    show_code(f"sns.swarmplot(data=df, x={repr(x_swarm)}, y='{y_swarm}', hue={repr(hue_swarm)}, size={size_swarm})")

    with st.expander("📸 Notebook Outputs — Swarm Plot"):
        image_gallery(load_gallery_images("Swarm Plot"), cols=3)
