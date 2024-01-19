import numpy as np
import pandas as pd
import plotly.graph_objects as go
import streamlit as st


def generate_line_plot(df, datasets, metadata, metric):
    fig = go.Figure()
    for i in range(len(datasets)):
        x = df[(df.dataset == datasets[i]) & (df.metadata == metadata)].hasStreamElementCount.to_numpy()
        y = df[(df.dataset == datasets[i]) & (df.metadata == metadata)][metric].to_numpy()
        fig.add_trace(
            go.Scatter(x=x, y=y, name=datasets[i])
        )

    fig.update_layout(
        barmode='group',
        title="Value of Selected Metric for Selected Datasets given Dataset Size",
        xaxis_title="Dataset Size",
        yaxis_title="Statistic Value",
        legend_title="Dataset",
    )

    axes_type = st.radio(
        "Axes",
        ["logarithmic", "linear"],
        key="axes",
        horizontal=True,
        index=0
    )

    if axes_type == 'logarithmic':
        fig.update_xaxes(type="log")
        fig.update_yaxes(type="log")

    st.write(fig)
