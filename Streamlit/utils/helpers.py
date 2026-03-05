"""Shared helper utilities for the Seaborn Visuals Streamlit app."""

import streamlit as st
import os
import glob


def show_code(code: str, language: str = "python") -> None:
    """Display a code block with syntax highlighting."""
    st.code(code, language=language)


def show_explanation(text: str) -> None:
    """Render an explanation inside a styled info card."""
    st.markdown(
        f'<div class="info-card">{text}</div>',
        unsafe_allow_html=True,
    )


def create_metric_cards(metrics: list[tuple[str, str]]) -> None:
    """
    Render a row of mini metric cards.

    metrics: list of (value, label) tuples.
    """
    cards_html = "".join(
        f'<div class="metric-mini"><div class="value">{val}</div><div class="label">{lbl}</div></div>'
        for val, lbl in metrics
    )
    st.markdown(f'<div class="metric-row">{cards_html}</div>', unsafe_allow_html=True)


def get_project_root() -> str:
    """Return the absolute path to the seaborn project root (parent of Streamlit/)."""
    return os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))


def load_gallery_images(plot_type_dir: str) -> list[str]:
    """
    Scan a plot-type directory for output PNGs and return sorted paths.

    Parameters
    ----------
    plot_type_dir : str
        Name of the plot-type folder, e.g. "Bar Plot".

    Returns
    -------
    list[str]
        Sorted list of absolute paths to PNG files.
    """
    root = get_project_root()
    pattern = os.path.join(root, plot_type_dir, "output*.png")
    images = sorted(glob.glob(pattern))
    return images


def image_gallery(images: list[str], cols: int = 3, captions: list[str] | None = None) -> None:
    """
    Display images in a responsive grid.

    Parameters
    ----------
    images : list[str]
        List of image file paths.
    cols : int
        Number of columns in the grid.
    captions : list[str] | None
        Optional captions for each image.
    """
    if not images:
        st.info("No output images found for this plot type.")
        return

    for i in range(0, len(images), cols):
        row = st.columns(cols)
        for j, col in enumerate(row):
            idx = i + j
            if idx < len(images):
                cap = captions[idx] if captions and idx < len(captions) else os.path.basename(images[idx])
                col.image(images[idx], caption=cap, use_container_width=True)


# ── Plot-type metadata ──
PLOT_TYPES = {
    "Bar Plot":        {"emoji": "📊", "desc": "Compare quantities across categories", "count": 12},
    "Boxplot":         {"emoji": "📦", "desc": "Visualize distributions & outliers", "count": 10},
    "CatPlot":         {"emoji": "🗂️", "desc": "Flexible categorical grid plots", "count": 8},
    "CountPlot":       {"emoji": "🔢", "desc": "Count occurrences per category", "count": 6},
    "FacetGrid":       {"emoji": "🔲", "desc": "Multi-panel subplot grids", "count": 10},
    "Heatmap":         {"emoji": "🌡️", "desc": "Color-coded matrix visualizations", "count": 6},
    "Histogram":       {"emoji": "📶", "desc": "Frequency distributions of data", "count": 8},
    "KDE Plot":        {"emoji": "🌊", "desc": "Smooth probability density curves", "count": 8},
    "Lineplot":        {"emoji": "📈", "desc": "Trends & time-series visualization", "count": 5},
    "Pair Plot":       {"emoji": "🔗", "desc": "Pairwise relationships in a dataset", "count": 6},
    "Scatterplots":    {"emoji": "⚬", "desc": "Relationships between two variables", "count": 8},
    "Strip plot":      {"emoji": "📍", "desc": "Individual data points by category", "count": 6},
    "Styling the plots": {"emoji": "🎨", "desc": "Themes, palettes & visual polish", "count": 8},
    "Swarm Plot":      {"emoji": "🐝", "desc": "Non-overlapping categorical scatter", "count": 6},
    "Violin Plot":     {"emoji": "🎻", "desc": "Distribution shape + box statistics", "count": 6},
}
