import pickle

import networkx as nx
from SPARQLWrapper import JSON, SPARQLWrapper

from constants import (PREFIXES, URL_EUROVOC)


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


# TODO: przenieśc do folderu streamlit_app? A tu zostawic tylko sam preprocessing/przygotowanie rzeczy
def find_shortest_path(
        graph,
        start_theme,
        end_theme,
        return_labels=True,
        labels_lang="en",
        return_predicates=False,
        edge_labels=None,
):
    if return_predicates and edge_labels is None:
        raise Exception(
            "When return_predicates is True, you have to provide edge_labels"
        )
    try:
        path = nx.shortest_path(graph, source=start_theme, target=end_theme)
    except nx.NetworkXNoPath:
        return None, None
    if not return_labels and not return_predicates:
        return path, None
    elif return_labels and not return_predicates:
        return [get_theme_label(theme, lang=labels_lang) for theme in path], None
    elif not return_labels and return_predicates:
        return path, [edge_labels[(path[i], path[i + 1])] for i in range(len(path) - 1)]
    elif return_labels and return_predicates:
        return (
            [get_theme_label(theme, lang=labels_lang) for theme in path],
            [edge_labels[(path[i], path[i + 1])] for i in range(len(path) - 1)],
        )


def save_graph(graph, filepath):
    pickle.dump(graph, open(filepath, "wb"))


def load_graph(filepath):
    return pickle.load(open(filepath, "rb"))
