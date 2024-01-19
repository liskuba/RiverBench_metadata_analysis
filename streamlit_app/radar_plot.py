import numpy as np
import pandas as pd
import plotly.graph_objects as go
import streamlit as st


def generate_radar_plot(df, datasets, metadata, metric):
    df = df[(df.stream_size == 'full') & (df.stream_type == 'stream')]

    datasets_radar_stats = __get_stats_for_each_dataset(
        df, datasets, metadata, metric
    )

    ranges = np.max(np.array(datasets_radar_stats), axis=0) * 1.2
    ranges = list(map(lambda x: int(x + 1), ranges))

    metadata = [
        f"{metadata[i]} ({ranges[i]})" for i in range(len(metadata))
    ]

    fig = go.Figure()

    for i in range(len(datasets)):
        dataset_radar_stats = datasets_radar_stats[i]
        dataset_radar_stats = [
            dataset_radar_stats[j] / ranges[j] for j in range(len(dataset_radar_stats))
        ]
        fig.add_trace(
            go.Scatterpolar(
                r=dataset_radar_stats, theta=metadata, fill="toself", name=datasets[i]
            )
        )

    fig.update_layout(
        polar=dict(radialaxis=dict(visible=True, range=[0, 1])), showlegend=True
    )

    st.write(fig)


def __get_stats_for_each_dataset(df, datasets, metadata, statistic):
    datasets_radar_stats = []
    for i in range(len(datasets)):
        datasets_radar_stats.append([])
        for j in range(len(metadata)):
            val = df.loc[
                (
                        (df["dataset"] == datasets[i])
                        & (df["metadata"] == metadata[j])
                ),
                statistic,
            ].iloc[0]
            datasets_radar_stats[i].append(np.nan_to_num(val))
    return datasets_radar_stats
