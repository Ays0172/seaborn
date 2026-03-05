"""
Page 3 — Relational Plots
==========================
Scatterplot, Lineplot, Heatmap — explore relationships & correlations.
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

st.set_page_config(page_title="Relational Plots", page_icon="🔗", layout="wide")
inject_custom_css()
hero("🔗 Relational Plots", "Scatterplot · Lineplot · Heatmap — explore relationships & correlations")

# ── Dataset selector ──
dataset_name = st.sidebar.selectbox("Dataset", ["tips", "iris", "penguins", "mpg", "diamonds"], key="rel_ds")

@st.cache_data
def load_dataset(name):
    return sns.load_dataset(name)

df = load_dataset(dataset_name)
num_cols = df.select_dtypes(include=[np.number]).columns.tolist()
cat_cols = df.select_dtypes(include=["category", "object"]).columns.tolist()

palette_options = ["deep", "muted", "pastel", "bright", "dark", "colorblind",
                   "Set2", "husl", "coolwarm", "viridis", "magma", "rocket", "flare"]
cmap_options = ["viridis", "magma", "rocket", "coolwarm", "YlGnBu", "RdYlBu", "Blues", "Greens", "Spectral"]

tabs = st.tabs(["⚬ Scatterplot", "📈 Lineplot", "🌡️ Heatmap"])

# ═══════════════════════════════════════════════════════
# TAB 1 — Scatterplot
# ═══════════════════════════════════════════════════════
with tabs[0]:
    step_header(1, "Scatterplot — Two-variable Relationships")
    show_explanation(
        "Scatter plots reveal the relationship between two numeric variables. "
        "Use <code>sns.scatterplot()</code> with <code>hue</code>, <code>size</code>, and <code>style</code> "
        "to encode additional dimensions."
    )

    c1, c2, c3, c4 = st.columns(4)
    x_scat = c1.selectbox("X", num_cols, index=0, key="scat_x")
    y_idx = min(1, len(num_cols) - 1)
    y_scat = c2.selectbox("Y", num_cols, index=y_idx, key="scat_y")
    hue_scat = c3.selectbox("Hue", [None] + cat_cols, key="scat_hue")
    pal_scat = c4.selectbox("Palette", palette_options, key="scat_pal")

    c5, c6 = st.columns(2)
    size_scat = c5.selectbox("Size by", [None] + num_cols, key="scat_size")
    style_scat = c6.selectbox("Style by", [None] + cat_cols, key="scat_style")

    fig, ax = plt.subplots(figsize=(10, 6))
    sns.scatterplot(data=df, x=x_scat, y=y_scat, hue=hue_scat, size=size_scat,
                    style=style_scat, palette=pal_scat, ax=ax, alpha=0.7, edgecolor="white", linewidth=0.4)
    ax.set_title(f"Scatterplot — {x_scat} vs {y_scat}", fontweight="bold", fontsize=13)
    plt.tight_layout()
    st.pyplot(fig)
    plt.close(fig)

    show_code(f"sns.scatterplot(data=df, x='{x_scat}', y='{y_scat}', hue={repr(hue_scat)}, size={repr(size_scat)}, style={repr(style_scat)})")

    with st.expander("📸 Notebook Outputs — Scatterplot"):
        image_gallery(load_gallery_images("Scatterplots"), cols=4)

# ═══════════════════════════════════════════════════════
# TAB 2 — Lineplot
# ═══════════════════════════════════════════════════════
with tabs[1]:
    step_header(2, "Lineplot — Trends & Time Series")
    show_explanation(
        "Line plots are ideal for showing trends over a continuous axis. "
        "Use <code>sns.lineplot()</code> which automatically adds confidence intervals when data has replicates."
    )

    c1, c2, c3, c4 = st.columns(4)
    x_line = c1.selectbox("X", num_cols + cat_cols, key="line_x")
    y_line = c2.selectbox("Y", num_cols, key="line_y")
    hue_line = c3.selectbox("Hue", [None] + cat_cols, key="line_hue")
    pal_line = c4.selectbox("Palette", palette_options, key="line_pal")
    ci_line = st.selectbox("Confidence interval", [95, 68, "sd", None], key="line_ci")

    fig, ax = plt.subplots(figsize=(10, 5))
    sns.lineplot(data=df, x=x_line, y=y_line, hue=hue_line,
                 palette=pal_line, ax=ax, linewidth=2.5)
    ax.set_title(f"Lineplot — {y_line} vs {x_line}", fontweight="bold", fontsize=13)
    plt.xticks(rotation=45)
    plt.tight_layout()
    st.pyplot(fig)
    plt.close(fig)

    show_code(f"sns.lineplot(data=df, x='{x_line}', y='{y_line}', hue={repr(hue_line)}, palette='{pal_line}')")

    with st.expander("📸 Notebook Outputs — Lineplot"):
        image_gallery(load_gallery_images("Lineplot"), cols=3)

# ═══════════════════════════════════════════════════════
# TAB 3 — Heatmap
# ═══════════════════════════════════════════════════════
with tabs[2]:
    step_header(3, "Heatmap — Correlation Matrix")
    show_explanation(
        "Heatmaps display a color-coded matrix — perfect for visualizing correlations. "
        "Use <code>sns.heatmap()</code> with <code>annot=True</code> to show values in cells."
    )

    if len(num_cols) >= 2:
        c1, c2 = st.columns(2)
        cmap_heat = c1.selectbox("Colormap", cmap_options, key="heat_cmap")
        annot_heat = c2.checkbox("Show annotations", value=True, key="heat_annot")
        square_heat = st.checkbox("Square cells", value=True, key="heat_sq")

        corr = df[num_cols].corr().round(3)

        fig, ax = plt.subplots(figsize=(10, 8))
        sns.heatmap(corr, annot=annot_heat, cmap=cmap_heat, square=square_heat,
                    linewidths=0.5, linecolor="white", ax=ax,
                    fmt=".2f" if annot_heat else "", vmin=-1, vmax=1,
                    cbar_kws={"shrink": 0.8, "label": "Correlation"})
        ax.set_title("Correlation Heatmap", fontweight="bold", fontsize=13, pad=15)
        plt.tight_layout()
        st.pyplot(fig)
        plt.close(fig)

        show_code(f"sns.heatmap(df[{num_cols}].corr(), annot={annot_heat}, cmap='{cmap_heat}', square={square_heat})")
    else:
        st.warning("Need at least 2 numeric columns for a heatmap. Try a different dataset.")

    with st.expander("📸 Notebook Outputs — Heatmap"):
        image_gallery(load_gallery_images("Heatmap"), cols=3)
