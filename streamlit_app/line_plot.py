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
    st.write(fig)
    fig.update_xaxes(type="log")
    fig.update_yaxes(type="log")
    st.write(fig)
