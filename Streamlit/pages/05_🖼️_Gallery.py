"""
Page 5 — Gallery
==================
Browse all 120+ notebook output images organized by plot type.
"""

import streamlit as st
import sys, os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from utils.styles import inject_custom_css, hero, step_header
from utils.helpers import load_gallery_images, image_gallery, PLOT_TYPES, create_metric_cards

st.set_page_config(page_title="Gallery", page_icon="🖼️", layout="wide")
inject_custom_css()
hero("🖼️ Visualization Gallery", "Browse all 120+ stunning chart outputs from the Seaborn notebooks")

# ── Overall stats ──
total_images = sum(len(load_gallery_images(pt)) for pt in PLOT_TYPES)
create_metric_cards([
    (str(len(PLOT_TYPES)), "Plot Types"),
    (str(total_images), "Total Images"),
    ("16", "Notebooks"),
    ("🔥", "Quality"),
])

st.divider()

# ── Filter ──
filter_options = ["📋 All Plot Types"] + [f"{meta['emoji']} {name}" for name, meta in PLOT_TYPES.items()]
selected = st.selectbox("Filter by plot type", filter_options, key="gallery_filter")

cols_count = st.sidebar.slider("Grid columns", 2, 5, 3, key="gallery_cols")

if selected == "📋 All Plot Types":
    # Show all plot types in sections
    for name, meta in PLOT_TYPES.items():
        images = load_gallery_images(name)
        if images:
            step_header(0, f"{meta['emoji']} {name} — {len(images)} charts")
            image_gallery(images, cols=cols_count)
            st.divider()
else:
    # Extract plot type name from selection
    plot_name = selected.split(" ", 1)[1] if " " in selected else selected
    images = load_gallery_images(plot_name)
    if images:
        st.markdown(f"### {selected} — {len(images)} charts")
        image_gallery(images, cols=cols_count)
    else:
        st.info(f"No output images found for **{plot_name}**.")

# ── Footer ──
st.divider()
st.markdown(
    "<center style='color:#64748b; font-size:0.85rem;'>"
    "All images generated from Jupyter notebooks · Seaborn Visuals"
    "</center>",
    unsafe_allow_html=True,
)
