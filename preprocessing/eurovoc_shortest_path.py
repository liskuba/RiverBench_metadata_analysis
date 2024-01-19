import json
import pickle

import networkx as nx
import pandas as pd
from constants import PREFIXES, URL_EUROVOC
from SPARQLWrapper import JSON, SPARQLWrapper

from streamlit_app.eurovoc_themes import (find_shortest_path,
                                          load_dataset_themes, load_graph)


def load_eurovoc_to_graph():
    G = nx.Graph()
    edge_labels = dict()
    sparql_eurovoc = SPARQLWrapper(URL_EUROVOC)
    sparql_eurovoc.setReturnFormat(JSON)
    predicates = ["skos:related", "skos:broader", "skos:narrower"]
    for predicate in predicates:
        query_eurovoc = f"""
            {PREFIXES}
            SELECT DISTINCT ?theme1 ?theme2
            WHERE {'{'}
                ?theme1 {predicate} ?theme2
                FILTER(STRSTARTS(STR(?theme1), STR(eurovoc:)))
            {'}'}
        """
        sparql_eurovoc.setQuery(query_eurovoc)
        results = sparql_eurovoc.query().convert()
        for result in results["results"]["bindings"]:
            node1 = result["theme1"]["value"].split("/")[-1]
            node2 = result["theme2"]["value"].split("/")[-1]
            G.add_edge(node1, node2)
            edge_labels[(node1, node2)] = predicate

    pos = nx.kamada_kawai_layout(G)
    for theme, position in pos.items():
        G.nodes[theme]["pos"] = position
        G.nodes[theme]["label"] = get_theme_label(theme)

    return G, edge_labels


def get_theme_label(theme, lang="en"):
    sparql_eurovoc = SPARQLWrapper(URL_EUROVOC)
    sparql_eurovoc.setReturnFormat(JSON)
    query_eurovoc = f"""
        {PREFIXES}
        SELECT DISTINCT ?theme ?label
        WHERE {'{'}
            eurovoc:{theme} skos:prefLabel ?label .
            FILTER(LANG(?label) = "{lang}")
        {'}'}
    """
    sparql_eurovoc.setQuery(query_eurovoc)
    results = sparql_eurovoc.query().convert()
    theme_labelled = results["results"]["bindings"][0]["label"]["value"]
    return theme_labelled


def save_themes_for_datasets(all_datasets, path_to_save):
    themes = dict()
    for dataset_name in all_datasets:
        url_dataset = f"http://localhost:3030/{dataset_name}/query"
        sparql_dataset = SPARQLWrapper(url_dataset)
        sparql_dataset.setReturnFormat(JSON)
        query_dataset = f"""
            {PREFIXES}
            SELECT DISTINCT ?theme
            WHERE {'{'}
                <https://w3id.org/riverbench/datasets/{dataset_name}/dev> dcat:theme ?theme .
            {'}'}
        """
        sparql_dataset.setQuery(query_dataset)
        results = sparql_dataset.query().convert()
        themes[dataset_name] = []
        for result in results["results"]["bindings"]:
            themes[dataset_name].append(result["theme"]["value"].split("/")[-1])
    print(themes)
    with open(path_to_save, "w") as f:
        json.dump(themes, f)


# Firstly save_graph and save_themes_for_datasets must be run
def calculate_all_avg_shortest_path(
    datasets, output_path, path_to_graph, path_to_themes=None
):
    graph = load_graph(path_to_graph)
    themes = load_dataset_themes(path_to_themes)
    scores = [[0] * len(datasets) for _ in range(len(datasets))]
    for i in range(len(datasets)):
        scores[i][i] = 0
        for j in range(i + 1, len(datasets)):
            score = calculate_avg_shortest_path(datasets[i], datasets[j], graph, themes)
            scores[i][j] = score
            scores[j][i] = score
    scores_df = pd.DataFrame(scores)
    scores_df.columns = datasets
    scores_df.to_csv(output_path, index=False)


def calculate_avg_shortest_path(dataset1, dataset2, graph, themes):
    themes1 = themes[dataset1]
    themes2 = themes[dataset2]
    distances = []
    for theme1 in themes1:
        for theme2 in themes2:
            if theme1 == theme2:
                distances.append(0)
            else:
                path, _ = find_shortest_path(graph, theme1, theme2)
                distances.append(len(path) - 1)
    return sum(distances) / len(distances)


def save_graph(graph, filepath):
    pickle.dump(graph, open(filepath, "wb"))
