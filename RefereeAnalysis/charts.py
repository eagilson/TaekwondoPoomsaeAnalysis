# charts.py
import numpy as np
import pandas as pd
import plotly.graph_objects as go
from typing import Dict, Any

def histogram_bin_regularization(data: np.ndarray, bin_width: int = 0.1):
    """
    Creates bin edges for a Histogram that are centered at 0 and have a standard width.

    Args:
        data (numpy.ndarray): Data to plot in a histogram.
        bin_width (int): OPTIONAL. Width of the bin in the data units. Default is 0.1.
        
    Returns:
        bins
    """

    half_bin_width = bin_width / 2

    # Find the range of data to determine how many bins you need
    data_min, data_max = data.min(), data.max()

    # Compute the leftmost bin edge (floor to multiple of bin_width, below data_min)
    left_edge = np.floor(data_min / bin_width) * bin_width + half_bin_width

    # Compute the rightmost bin edge (ceil to multiple of bin_width, above data_max)
    right_edge = np.ceil(data_max / bin_width) * bin_width + half_bin_width

    # Create bin edges: from left_edge to right_edge with step = bin_width
    bins = np.arange(left_edge, right_edge, bin_width)

    return bins

def _safe_histogram(data: np.ndarray, bin_width: int = 0.1, max_bins: int = 100):
    """Compute histogram with capped bin count."""
    data = data[~np.isnan(data)]
    if len(data) == 0:
        return np.array([]), np.array([])

    if len(data) <= 1:
        return np.array([1]), np.array([data[0] - 0.5, data[0] + 0.5])

    bins = histogram_bin_regularization(data, bin_width)

    try:
        hist, edges = np.histogram(data, bins=bins)
        if len(hist) > max_bins:
            hist, edges = np.histogram(data, bins=max_bins)
    except:
        hist, edges = np.histogram(data, bins=min(max_bins, 30))

    return hist, edges


def make_bar_chart(data_series, title: str, color: str, bin_width: int = 0.1) -> Dict[str, Any]:
    """Single series histogram (used for all bar charts)."""
    if data_series.empty:
        return {'data': [], 'layout': {}}

    data = pd.to_numeric(data_series, errors='coerce').dropna().values
    if len(data) == 0:
        return {'data': [], 'layout': {}}

    hist, edges = _safe_histogram(data,bin_width)
    centers = (edges[:-1] + edges[1:]) / 2

    return {
        'data': [go.Bar(
            x=centers,
            y=hist,
            marker_color=color,
            #width=0.1,
            hovertemplate='Gap: %{x:.3f}<br>Count: %{y}<extra></extra>'
        )],
        'layout': go.Layout(
            title=title,
            xaxis=dict(title='Score Gap'),
            yaxis=dict(title='Count'),
            bargap=0.05,
            showlegend=False
        )
    }


def make_box_chart(data_series, title: str, color: str) -> Dict[str, Any]:
    """Box plot."""
    if data_series.empty:
        return {'data': [], 'layout': {}}

    data = pd.to_numeric(data_series, errors='coerce').dropna().values
    if len(data) == 0:
        return {'data': [], 'layout': {}}

    return {
        'data': [go.Box(
            y=data,
            name='',
            marker_color=color,
            boxpoints='outliers',
            jitter=0.3,
            pointpos=0,
            notched=True
        )],
        'layout': go.Layout(
            title=title,
            yaxis=dict(title='Score Difference'),
            xaxis=dict(showticklabels=False),
            showlegend=False
        )
    }