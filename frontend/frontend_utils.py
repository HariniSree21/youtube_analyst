# frontend/frontend_utils.py

import streamlit as st
import pandas as pd

def display_comparison_table(comparison_data):
    """Render side-by-side comparison table of two channels."""
    df = pd.DataFrame(comparison_data)
    df.set_index("channel_name", inplace=True)
    st.dataframe(df.T)

def plot_bar_comparison(comparison_data, metric="subscribers"):
    """Plot a bar chart comparing selected metric between channels."""
    labels = [d["channel_name"] for d in comparison_data]
    values = [int(d.get(metric, 0)) for d in comparison_data]
    chart_data = pd.DataFrame({metric.title(): values}, index=labels)
    st.bar_chart(chart_data)
