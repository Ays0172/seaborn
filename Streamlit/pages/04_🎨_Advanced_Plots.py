"""
Page 4 — Advanced Plots
========================
CatPlot, Pair Plot, FacetGrid, Styling — multi-panel grids & theme mastery.
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

st.set_page_config(page_title="Advanced Plots", page_icon="🎨", layout="wide")
inject_custom_css()
hero("🎨 Advanced Plots", "CatPlot · Pair Plot · FacetGrid · Styling — multi-panel grids & theme mastery")

# ── Dataset selector ──
dataset_name = st.sidebar.selectbox("Dataset", ["tips", "iris", "penguins", "titanic"], key="adv_ds")

@st.cache_data
def load_dataset(name):
    return sns.load_dataset(name)

df = load_dataset(dataset_name)
num_cols = df.select_dtypes(include=[np.number]).columns.tolist()
cat_cols = df.select_dtypes(include=["category", "object"]).columns.tolist()

palette_options = ["deep", "muted", "pastel", "bright", "dark", "colorblind",
                   "Set2", "Set3", "husl", "viridis", "magma", "rocket"]

tabs = st.tabs(["🗂️ CatPlot", "🔗 Pair Plot", "🔲 FacetGrid", "🎨 Styling"])

# ═══════════════════════════════════════════════════════
# TAB 1 — CatPlot
# ═══════════════════════════════════════════════════════
with tabs[0]:
    step_header(1, "CatPlot — Flexible Categorical Grids")
    show_explanation(
        "<code>sns.catplot()</code> is a figure-level function that gives access to all categorical plot types "
        "(<code>kind</code>) plus automatic faceting with <code>col</code> and <code>row</code> parameters."
    )

    c1, c2, c3, c4 = st.columns(4)
    x_cat = c1.selectbox("X (category)", cat_cols, key="catplot_x") if cat_cols else None
    y_cat = c2.selectbox("Y (numeric)", num_cols, key="catplot_y")
    kind_cat = c3.selectbox("Kind", ["box", "violin", "bar", "strip", "swarm", "point"], key="catplot_kind")
    pal_cat = c4.selectbox("Palette", palette_options, key="catplot_pal")

    col_facet = st.selectbox("Column facet", [None] + cat_cols, key="catplot_col")
    hue_cat = st.selectbox("Hue", [None] + cat_cols, key="catplot_hue")

    if x_cat:
        g = sns.catplot(data=df, x=x_cat, y=y_cat, kind=kind_cat, hue=hue_cat,
                        col=col_facet, palette=pal_cat, height=5, aspect=1.2)
        g.fig.suptitle(f"CatPlot — {kind_cat} of {y_cat} by {x_cat}", fontweight="bold", fontsize=13, y=1.02)
        plt.tight_layout()
        st.pyplot(g.fig)
        plt.close(g.fig)

        show_code(f"sns.catplot(data=df, x='{x_cat}', y='{y_cat}', kind='{kind_cat}', hue={repr(hue_cat)}, col={repr(col_facet)})")
    else:
        st.warning("No categorical columns found in this dataset.")

    with st.expander("📸 Notebook Outputs — CatPlot"):
        image_gallery(load_gallery_images("CatPlot"), cols=4)

# ═══════════════════════════════════════════════════════
# TAB 2 — Pair Plot
# ═══════════════════════════════════════════════════════
with tabs[1]:
    step_header(2, "Pair Plot — Pairwise Relationships")
    show_explanation(
        "<code>sns.pairplot()</code> creates a grid of scatter plots for every pair of numeric variables, "
        "with histograms or KDE on the diagonal. Great for EDA."
    )

    c1, c2, c3 = st.columns(3)
    hue_pair = c1.selectbox("Hue", [None] + cat_cols, key="pair_hue")
    pal_pair = c2.selectbox("Palette", palette_options, key="pair_pal")
    diag_kind = c3.selectbox("Diagonal kind", ["auto", "hist", "kde"], key="pair_diag")

    # Limit columns for pair plot performance
    selected_cols = st.multiselect("Select columns (max 5 for performance)",
                                   num_cols, default=num_cols[:min(4, len(num_cols))], key="pair_cols")

    if len(selected_cols) >= 2:
        subset = df[selected_cols + ([hue_pair] if hue_pair else [])].dropna()
        if len(subset) > 500:
            subset = subset.sample(500, random_state=42)
            st.caption(f"⚡ Sampled 500 rows for performance (from {len(df)})")

        g = sns.pairplot(subset, hue=hue_pair, palette=pal_pair, diag_kind=diag_kind,
                         plot_kws={"alpha": 0.6, "edgecolor": "white", "linewidth": 0.3})
        g.fig.suptitle("Pair Plot — Pairwise Relationships", fontweight="bold", fontsize=13, y=1.01)
        st.pyplot(g.fig)
        plt.close(g.fig)

        show_code(f"sns.pairplot(df[{selected_cols}], hue={repr(hue_pair)}, diag_kind='{diag_kind}')")
    else:
        st.warning("Select at least 2 numeric columns.")

    with st.expander("📸 Notebook Outputs — Pair Plot"):
        image_gallery(load_gallery_images("Pair Plot"), cols=3)

# ═══════════════════════════════════════════════════════
# TAB 3 — FacetGrid
# ═══════════════════════════════════════════════════════
with tabs[2]:
    step_header(3, "FacetGrid — Multi-panel Subplot Grids")
    show_explanation(
        "<code>sns.FacetGrid()</code> creates a grid of subplots based on categorical variables, "
        "then maps a plotting function onto each panel."
    )

    c1, c2, c3 = st.columns(3)
    col_fg = c1.selectbox("Column facet", cat_cols, key="fg_col") if cat_cols else None
    row_fg = c2.selectbox("Row facet", [None] + cat_cols, key="fg_row")
    hue_fg = c3.selectbox("Hue", [None] + cat_cols, key="fg_hue")

    plot_var = st.selectbox("Plot variable (numeric)", num_cols, key="fg_var")
    plot_type_fg = st.selectbox("Plot type", ["histplot", "kdeplot", "boxplot"], key="fg_type")

    if col_fg:
        g = sns.FacetGrid(df, col=col_fg, row=row_fg, hue=hue_fg,
                          height=4, aspect=1.2, palette="deep")
        plot_fn = getattr(sns, plot_type_fg)
        if plot_type_fg in ("histplot", "kdeplot"):
            g.map_dataframe(plot_fn, x=plot_var)
        else:
            g.map_dataframe(plot_fn, y=plot_var)
        g.add_legend()
        g.fig.suptitle(f"FacetGrid — {plot_type_fg} of {plot_var}", fontweight="bold", fontsize=13, y=1.02)
        plt.tight_layout()
        st.pyplot(g.fig)
        plt.close(g.fig)

        show_code(f"g = sns.FacetGrid(df, col='{col_fg}', row={repr(row_fg)}, hue={repr(hue_fg)})\ng.map_dataframe(sns.{plot_type_fg}, x='{plot_var}')\ng.add_legend()")
    else:
        st.warning("No categorical columns found for faceting.")

    with st.expander("📸 Notebook Outputs — FacetGrid"):
        image_gallery(load_gallery_images("FacetGrid"), cols=4)

# ═══════════════════════════════════════════════════════
# TAB 4 — Styling
# ═══════════════════════════════════════════════════════
with tabs[3]:
    step_header(4, "Styling — Themes, Palettes & Polish")
    show_explanation(
        "Seaborn provides built-in themes (<code>sns.set_style()</code>) and color palettes (<code>sns.set_palette()</code>) "
        "to quickly transform your plots' appearance."
    )

    c1, c2 = st.columns(2)
    style_choice = c1.selectbox("Theme", ["darkgrid", "whitegrid", "dark", "white", "ticks"], key="style_theme")
    palette_choice = c2.selectbox("Palette", palette_options, key="style_pal")

    context_choice = st.selectbox("Context (scale)", ["notebook", "paper", "talk", "poster"], key="style_ctx")
    font_scale = st.slider("Font scale", 0.5, 2.5, 1.2, 0.1, key="style_fs")

    col_style = st.selectbox("Column", num_cols, key="style_col")

    sns.set_theme(style=style_choice, palette=palette_choice, context=context_choice, font_scale=font_scale)

    fig, axes = plt.subplots(1, 3, figsize=(15, 4))

    sns.histplot(data=df, x=col_style, ax=axes[0], kde=True)
    axes[0].set_title("Histogram + KDE", fontweight="bold")

    if cat_cols:
        cat_for_style = cat_cols[0]
        sns.boxplot(data=df, x=cat_for_style, y=col_style, ax=axes[1])
        axes[1].set_title("Boxplot", fontweight="bold")
        plt.setp(axes[1].xaxis.get_majorticklabels(), rotation=45)
    else:
        sns.kdeplot(data=df, x=col_style, ax=axes[1], fill=True)
        axes[1].set_title("KDE Plot", fontweight="bold")

    sns.scatterplot(data=df, x=num_cols[0], y=col_style, ax=axes[2], alpha=0.6)
    axes[2].set_title("Scatter", fontweight="bold")

    plt.tight_layout()
    st.pyplot(fig)
    plt.close(fig)

    # Reset to defaults
    sns.set_theme()

    show_code(f"sns.set_theme(style='{style_choice}', palette='{palette_choice}', context='{context_choice}', font_scale={font_scale})")

    # Show palette swatches
    st.markdown("#### 🌈 Current Palette Preview")
    pal_fig, pal_ax = plt.subplots(figsize=(8, 1))
    colors = sns.color_palette(palette_choice, 10)
    for i, c in enumerate(colors):
        pal_ax.add_patch(plt.Rectangle((i, 0), 1, 1, color=c))
    pal_ax.set_xlim(0, 10)
    pal_ax.set_ylim(0, 1)
    pal_ax.axis("off")
    pal_ax.set_title(f"Palette: {palette_choice}", fontsize=11, fontweight="bold")
    plt.tight_layout()
    st.pyplot(pal_fig)
    plt.close(pal_fig)

    with st.expander("📸 Notebook Outputs — Styling"):
        image_gallery(load_gallery_images("Styling the plots"), cols=4)
