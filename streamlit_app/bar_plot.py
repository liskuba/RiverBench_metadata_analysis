import numpy as np
import pandas as pd
import plotly.graph_objects as go
import streamlit as st


def generate_bar_plot(df, datasets, metadata, metric):
    df = df[(df.stream_size == 'full') & (df.stream_type == 'stream')]

    data = []

    for i in range(len(metadata)):
        data.append(go.Bar(name=metadata[i],

                           x=df[(df.dataset.isin(datasets)) & (df.metadata == metadata[i])].dataset.to_numpy(),
                           y=df[(df.dataset.isin(datasets)) & (df.metadata == metadata[i])][metric].to_numpy()))

    fig = go.Figure(data=data)

    fig.update_layout(
        barmode='group',
        title="Value of Selected Metric for Selected Datasets and Metadata Info given Full Dataset",
        xaxis_title="Datasets",
        yaxis_title="Metric Value",
        legend_title="Metadata",
    )

    st.write(fig)
