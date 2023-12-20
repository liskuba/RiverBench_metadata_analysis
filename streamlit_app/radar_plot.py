import numpy as np
import pandas as pd
import plotly.graph_objects as go
import streamlit as st


def generate_radar_plot(path_to_csv):
    df = pd.read_csv(path_to_csv)

    # TODO: automate including all datasets (e.g. from dataframe)
    datasets = st.multiselect(
        "Datasets",
        [
            "assist-iot-weather",
            "assist-iot-weather-graphs",
            "citypulse-traffic-graphs",
            "citypulse-traffic",
            "dbpedia-live",
            "digital-agenda-indicators",
            "linked-spending",
            "lod-katrina",
            "muziekweb",
            "nanopubs",
            "politiquices",
            "yago-annotated-facts",
        ],
        ["assist-iot-weather", "politiquices"],
    )

    categories = st.multiselect(
        "Metadata",
        [
            "SimpleLiteralCountStatistics",
            "IriCountStatistics",
            "ObjectCountStatistics",
            "GraphCountStatistics",
            "SubjectCountStatistics",
            "DatatypeLiteralCountStatistics",
            "BlankNodeCountStatistics",
            "LanguageLiteralCountStatistics",
            "QuotedTripleCountStatistics",
            "StatementCountStatistics",
            "LiteralCountStatistics",
            "PredicateCountStatistics",
        ],
        [
            "LanguageLiteralCountStatistics",
            "GraphCountStatistics",
            "BlankNodeCountStatistics",
            "LiteralCountStatistics",
            "SimpleLiteralCountStatistics",
        ],
    )

    categories = [
        "https://w3id.org/riverbench/schema/metadata#" + category
        for category in categories
    ]

    statistic = st.selectbox(
        "Statistic",
        ("maximum", "mean", "minimum", "standardDeviation", "sum", "uniqueCount"),
        index=1,
    )

    datasets_radar_stats = __get_stats_for_each_dataset(
        df, datasets, categories, statistic
    )

    ranges = np.max(np.array(datasets_radar_stats), axis=0) * 1.2
    ranges = list(map(lambda x: int(x + 1), ranges))

    categories = [
        f"{categories[i].split('#')[-1]} ({ranges[i]})" for i in range(len(categories))
    ]

    fig = go.Figure()

    for i in range(len(datasets)):
        dataset_radar_stats = datasets_radar_stats[i]
        dataset_radar_stats = [
            dataset_radar_stats[j] / ranges[j] for j in range(len(dataset_radar_stats))
        ]
        fig.add_trace(
            go.Scatterpolar(
                r=dataset_radar_stats, theta=categories, fill="toself", name=datasets[i]
            )
        )

    fig.update_layout(
        polar=dict(radialaxis=dict(visible=True, range=[0, 1])), showlegend=False
    )

    st.write(fig)


def __get_stats_for_each_dataset(dataframe, datasets, categories, statistic):
    datasets_radar_stats = []
    for i in range(len(datasets)):
        datasets_radar_stats.append([])
        for j in range(len(categories)):
            val = dataframe.loc[
                (
                    (dataframe["dataset"] == datasets[i])
                    & (dataframe["metadata"] == categories[j])
                ),
                statistic,
            ].iloc[0]
            datasets_radar_stats[i].append(val)
    return datasets_radar_stats
