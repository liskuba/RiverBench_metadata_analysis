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

    # Change the bar mode
    fig.update_layout(barmode='group')

    st.write(fig)
