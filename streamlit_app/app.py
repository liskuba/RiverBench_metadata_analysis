# import radar_plot
#
# path_to_radar_csv = f"streamlit_app/data/dev#statistics-full_all_datasets.csv"
#
# radar_plot.generate_radar_plot(path_to_radar_csv)
import os

import numpy as np
import pandas as pd
import streamlit as st
from bar_plot import generate_bar_plot
from box_plot import generate_box_plot
from eurovoc_themes import (DATASETS, generate_eurovoc_themes_visualization,
                            load_avg_shortest_paths, load_dataset_themes,
                            load_graph)
from line_plot import generate_line_plot
from radar_plot import generate_radar_plot
from streamlit_option_menu import option_menu

path_to_graph_file = "streamlit_app/data/graph_with_eurovoc_themes.pickle"
path_to_themes = "streamlit_app/data/themes.json"
path_to_avg_shortest_path = "streamlit_app/data/avg_shortest_path.csv"


@st.cache_data
def load_metadata():
    def read_dataset_sizes():
        df_sizes = pd.read_csv(
            os.path.join("streamlit_app", "data", "all_datasets_sizes.csv")
        )
        df_stats_10k = pd.read_csv(
            os.path.join("streamlit_app", "data", "dev#statistics-10k_all_datasets.csv")
        )
        df_stats_100k = pd.read_csv(
            os.path.join(
                "streamlit_app", "data", "dev#statistics-100k_all_datasets.csv"
            )
        )
        df_stats_full = pd.read_csv(
            os.path.join(
                "streamlit_app", "data", "dev#statistics-full_all_datasets.csv"
            )
        )

        return df_sizes, df_stats_10k, df_stats_100k, df_stats_full

    df_sizes, df_stats_10k, df_stats_100k, df_stats_full = read_dataset_sizes()

    df_stats_10k["stream_size"] = "10k"
    df_stats_100k["stream_size"] = "100k"
    df_stats_full["stream_size"] = "full"

    df_stats = pd.concat([df_stats_10k, df_stats_100k, df_stats_full])
    df_all = pd.merge(df_sizes, df_stats, on=["dataset", "stream_size"], how="inner")
    df_all["metadata"] = df_all.apply(
        lambda row: row.metadata.split("#")[1].removesuffix("Statistics"), axis=1
    )

    return df_all


@st.cache_data
def load_eurovoc():
    graph = load_graph(path_to_graph_file)
    themes_dict = load_dataset_themes(path_to_themes)
    avg_shortest_paths_df = load_avg_shortest_paths(
        path_to_avg_shortest_path
    ).set_index(pd.Series(DATASETS))
    return graph, themes_dict, avg_shortest_paths_df


df = load_metadata()
G, themes, avg_shortest_paths = load_eurovoc()

links = {
    'assist-iot-weather': "[assist-iot-weather](https://riverbench.github.io/datasets/assist-iot-weather/dev/)",
    'assist-iot-weather-graphs': "[assist-iot-weather-graphs](https://riverbench.github.io/datasets/assist-iot-weather-graphs/dev/)",
    'citypulse-traffic': "[citypulse-traffic](https://riverbench.github.io/datasets/citypulse-traffic/dev/)",
    'citypulse-traffic-graphs': "[citypulse-traffic-graphs](https://riverbench.github.io/datasets/citypulse-traffic-graph/dev/)",
    'dbpedia-live': "[dbpedia-live](https://riverbench.github.io/datasets/dbpedia-live/dev/)",
    'digital-agenda-indicators': "[digital-agenda-indicators](https://riverbench.github.io/datasets/digital-agenda-indicators/dev/)",
    'linked-spending': "[linked-spending](https://riverbench.github.io/datasets/linked-spending/dev/)",
    'lod-katrina': "[lod-katrina](https://riverbench.github.io/datasets/lod-katrina/dev/)",
    'muziekweb': "[muziekweb](https://riverbench.github.io/datasets/muziekweb/dev/)",
    'nanopubs': "[nanopubs](https://riverbench.github.io/datasets/nanopubs/dev/)",
    'politiquices': "[politiquices](https://riverbench.github.io/datasets/politiquices/dev/)",
    'yago-annotated-facts': "[yago-annotated-facts](https://riverbench.github.io/datasets/yago-annotated-facts/dev/)"
}
# def on_change(key):
#     selection = st.session_state[key]
#     st.write(f"Selection changed to {selection}")


selected_tab = option_menu(
    None,
    ["RadarPlot", "BarPlot", "LinePlot", "EuroVoc"],  # "BoxPlot",
    icons=["radar", "bar-chart", "graph-up", "balloon"],  # , "box"
    key="menu",
    orientation="horizontal",
)  # on_change=on_change

datasets = st.multiselect(
    "Datasets",
    df["dataset"].unique().tolist(),
    [df["dataset"].unique().tolist()[i] for i in [0, 2, 4, 5]],
)

links_to_display = ''
for dataset in datasets:
    links_to_display += links[dataset] + ' '

st.write(links_to_display)

# if 'metadata_single' not in st.session_state:
#     st.session_state['metadata_single'] = df["metadata"].unique().tolist()[1]
# else:
#     metadata_single = st.session_state['metadata_single']

if selected_tab == "RadarPlot" or selected_tab == "BarPlot":
    stateful_multi = df["metadata"].unique().tolist()[:5] if "metadata_multi" not in st.session_state else \
    st.session_state["metadata_multi"]

    metadata_multi = st.multiselect(
        "Metadata",
        df["metadata"].unique().tolist(),
        stateful_multi,
    )
    st.session_state["metadata_multi"] = metadata_multi


elif selected_tab == 'LinePlot' or selected_tab == 'BoxPlot':
    stateful_index = (
        0
        if "metadata_single" not in st.session_state
        else st.session_state["metadata_single"]
    )
    metadata_single = st.selectbox(
        "Metadata",
        df["metadata"].unique().tolist(),
        index=stateful_index,
    )
    st.session_state["metadata_single"] = (
        df["metadata"].unique().tolist().index(metadata_single)
    )

if selected_tab != 'EuroVoc':
    metric = st.selectbox(
        "Metric",
        (
            "maximum",
            "mean",
            "minimum",
            "standardDeviation",
            "sum",
            "uniqueCount",
        ),  # df["metadata"].unique().tolist(),
        index=1,
    )

if selected_tab == "RadarPlot":
    generate_radar_plot(df, datasets, metadata_multi, metric)
elif selected_tab == "BarPlot":
    generate_bar_plot(df, datasets, metadata_multi, metric)
elif selected_tab == "LinePlot":
    generate_line_plot(df, datasets, metadata_single, metric)
# elif selected_tab == "BoxPlot":
#     generate_box_plot(df, datasets, metadata_single, metric)
elif selected_tab == "EuroVoc":
    generate_eurovoc_themes_visualization(G, themes, avg_shortest_paths, datasets)
