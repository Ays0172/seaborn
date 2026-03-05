"""
Seaborn Visuals — Interactive Visualization Gallery
====================================================
Main entry point for the Streamlit multi-page application.
"""

import streamlit as st
import sys, os

# ── Make utils importable from any page ──
sys.path.insert(0, os.path.dirname(__file__))

from utils.styles import inject_custom_css, hero
from utils.helpers import create_metric_cards, PLOT_TYPES

# ── Page config ──
st.set_page_config(
    page_title="Seaborn Visuals",
    page_icon="🎨",
    layout="wide",
    initial_sidebar_state="expanded",
)

inject_custom_css()

# ── Sidebar branding ──
with st.sidebar:
    st.markdown("## 🎨 Seaborn Visuals")
    st.caption("Data Never Looked So Good")
    st.divider()
    st.markdown(
        "**Pages**\n"
        "- 📊 Distribution Plots\n"
        "- 📈 Categorical Plots\n"
        "- 🔗 Relational Plots\n"
        "- 🎨 Advanced Plots\n"
        "- 🖼️ Gallery\n"
    )
    st.divider()
    st.caption("Use the sidebar pages ↑ to navigate.")

# ── Hero section ──
hero(
    "🎨 Seaborn Visuals",
    "Elegant, expressive, and ready to impress — a collection of stunning statistical visualizations powered by Seaborn & Python.",
)

# ── Overview metrics ──
create_metric_cards([
    ("15", "Plot Types"),
    ("16", "Notebooks"),
    ("120+", "Charts"),
    ("5+", "Datasets"),
])

# ── Plot type cards ──
st.markdown("### 🗺️ Visualization Roadmap")

col1, col2 = st.columns(2)

categories = [
    {
        "title": "📊 Distribution Plots",
        "desc": "Histogram, KDE Plot, Boxplot, Violin Plot — understand how your data is spread.",
        "badge": "4 Plot Types · Interactive Controls",
    },
    {
        "title": "📈 Categorical Plots",
        "desc": "Bar Plot, Count Plot, Strip Plot, Swarm Plot — compare categories visually.",
        "badge": "4 Plot Types · Multiple Palettes",
    },
    {
        "title": "🔗 Relational Plots",
        "desc": "Scatterplot, Lineplot, Heatmap — explore relationships & correlations.",
        "badge": "3 Plot Types · Live Charts",
    },
    {
        "title": "🎨 Advanced Plots",
        "desc": "CatPlot, Pair Plot, FacetGrid, Styling — multi-panel grids & theme mastery.",
        "badge": "4 Plot Types · Styling Demo",
    },
    {
        "title": "🖼️ Full Gallery",
        "desc": "Browse all 120+ output images from the notebooks, organized by plot type.",
        "badge": "120+ Images · Grid View",
    },
]

for i, cat in enumerate(categories):
    target = col1 if i % 2 == 0 else col2
    with target:
        st.markdown(f"""
        <div class="module-card">
            <h3>{cat["title"]}</h3>
            <p>{cat["desc"]}</p>
            <span class="badge">{cat["badge"]}</span>
        </div>
        """, unsafe_allow_html=True)

# ── All plot types mini grid ──
st.markdown("### 📋 All 15 Plot Types")

grid_cols = st.columns(5)
for idx, (name, meta) in enumerate(PLOT_TYPES.items()):
    with grid_cols[idx % 5]:
        st.markdown(f"""
        <div class="module-card" style="padding:1rem; margin-bottom:0.7rem; text-align:center;">
            <div style="font-size:1.6rem;">{meta["emoji"]}</div>
            <div style="color:#fb923c; font-weight:600; font-size:0.85rem; margin-top:0.3rem;">{name}</div>
            <div style="color:#64748b; font-size:0.7rem; margin-top:0.2rem;">{meta["count"]} charts</div>
        </div>
        """, unsafe_allow_html=True)

# ── Footer ──
st.divider()
st.markdown(
    "<center style='color:#64748b; font-size:0.85rem;'>"
    "Built with ❤️ using Streamlit · Seaborn Visuals"
    "</center>",
    unsafe_allow_html=True,
)
