import json
import pickle
import sys

import networkx as nx
import pandas as pd
import plotly.graph_objects as go
import streamlit as st

# TODO: somehow import this from preprocessing.constants
DATASETS = [
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
]

DEFAULT_COLOR = "#607d8b"
COLORS = [
    "#f44336",
    "#ff5722",
    "#673ab7",
    "#2196f3",
    "#3f51b5",
    "#4caf50",
    "#795548",
    "#9c27b0",
    "#ffc107",
    "#009688",
    "#03a9f4",
    "#cddc39",
    "#e81e63",
    "#ffeb3b",
    "#ff9800",
    "#8bc34a",
    "#00bcd4",
]


def load_graph(filepath):
    return pickle.load(open(filepath, "rb"))


def load_dataset_themes(filepath):
    with open(filepath, "r") as f:
        themes = json.load(f)
    return themes


def load_avg_shortest_paths(filepath):
    return pd.read_csv(filepath)


def edges_to_lists(graph):
    edge_x = []
    edge_y = []
    for edge in graph.edges():
        x0, y0 = graph.nodes[edge[0]]["pos"]
        x1, y1 = graph.nodes[edge[1]]["pos"]
        edge_x.append(x0)
        edge_x.append(x1)
        edge_x.append(None)
        edge_y.append(y0)
        edge_y.append(y1)
        edge_y.append(None)

    return edge_x, edge_y


def nodes_to_lists(graph, datasets, themes):
    node_x = []
    node_y = []
    node_text = []
    colors = [DEFAULT_COLOR] * len(graph.nodes)
    sizes = [4] * len(graph.nodes)
    for i, node in enumerate(graph.nodes()):
        x, y = graph.nodes[node]["pos"]
        node_text.append(graph.nodes[node]["label"])
        node_x.append(x)
        node_y.append(y)
        for j, dataset in enumerate(datasets):
            if node in themes[dataset]:
                colors[i] = COLORS[j % len(COLORS)]
                sizes[i] = 12
                node_text[-1] += f", {dataset} theme"
    return node_x, node_y, node_text, colors, sizes


def find_shortest_path(graph, start_theme, end_theme, return_labels=True):
    try:
        path = nx.shortest_path(graph, source=start_theme, target=end_theme)
    except nx.NetworkXNoPath:
        return None, None
    if not return_labels:
        return path, None
    else:
        return path, [graph.nodes[theme]["label"] for theme in path]


def generate_eurovoc_themes_visualization(G, themes, avg_shortest_paths, datasets=None):
    # TODO: wywalic do app, zeby sie nie wczytywalo za kazdym razem (loading)
    if datasets is None:
        datasets = ["assist-iot-weather", "dbpedia-live", "muziekweb"]  # TODO: wywalic

    themes_to_select = []
    for df_name, themes_one_df in themes.items():
        if df_name in datasets:
            themes_to_select += themes_one_df
    themes_to_select = list(set(themes_to_select))

    themes_to_select_labelled = [G.nodes[theme]["label"] for theme in themes_to_select]

    selected_themes = st.multiselect(
        "Shortest path between two themes",
        themes_to_select_labelled,
        themes_to_select_labelled[:2],
        max_selections=2,
    )

    edge_x, edge_y = edges_to_lists(G)

    edge_trace = go.Scatter(
        x=edge_x,
        y=edge_y,
        line=dict(width=0.1, color="#C7C0BF"),
        hoverinfo="none",
        mode="lines",
    )

    node_x, node_y, node_text, colors, sizes = nodes_to_lists(G, datasets, themes)

    path_x, path_y = [], []

    if len(selected_themes) == 2:
        path, path_labelled = find_shortest_path(
            G,
            themes_to_select[themes_to_select_labelled.index(selected_themes[0])],
            themes_to_select[themes_to_select_labelled.index(selected_themes[1])],
        )
        if path is None:
            st.write(f"There is no connection between selected themes :(")
        else:
            st.write(f"Shortest path: {path_labelled} ({len(path_labelled) - 1} edges)")
            for i in range(len(path) - 1):
                x0, y0 = G.nodes[path[i]]["pos"]
                x1, y1 = G.nodes[path[i + 1]]["pos"]
                sizes[list(G.nodes()).index(path[i])] = 10
                path_x.append(x0)
                path_x.append(x1)
                path_x.append(None)
                path_y.append(y0)
                path_y.append(y1)
                path_y.append(None)
            sizes[list(G.nodes()).index(path[len(path) - 1])] = 10

    shortest_path_trace = go.Scatter(
        x=path_x,
        y=path_y,
        line=dict(width=1.5, color="#ff0099"),
        hoverinfo="none",
        mode="lines",
    )

    node_trace = go.Scatter(
        x=node_x,
        y=node_y,
        mode="markers",
        hoverinfo="text",
        marker=dict(color=colors, size=sizes, line_width=0.5),
    )

    # node_trace.marker.color = ["#15DDEE"] * len(G.nodes)
    node_trace.text = node_text

    fig = go.Figure(
        data=[edge_trace, node_trace, shortest_path_trace],
        layout=go.Layout(
            title="Eurovoc themes",
            titlefont_size=14,
            showlegend=False,
            hovermode="closest",
            margin=dict(b=20, l=5, r=5, t=40),
            xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
            yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
        ),
    )

    st.write(fig)
    st.markdown("**Average shortest path**")
    st.write(avg_shortest_paths.filter(items=datasets, axis=0)[datasets])
