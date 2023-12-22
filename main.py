import os

import pandas as pd
from SPARQLWrapper import JSON, SPARQLWrapper

EUROVOC_JENA = "eurovoc"
PREFIXES = """
    PREFIX dcat:    <http://www.w3.org/ns/dcat#>
    PREFIX dct:     <http://purl.org/dc/terms/>
    PREFIX eurovoc: <http://eurovoc.europa.eu/>
    PREFIX foaf:    <http://xmlns.com/foaf/0.1/>
    PREFIX odp:     <http://data.europa.eu/euodp/ontologies/ec-odp#>
    PREFIX rb:      <https://w3id.org/riverbench/schema/metadata#>
    PREFIX rbdoc:   <https://w3id.org/riverbench/schema/documentation#>
    PREFIX rdfs:    <http://www.w3.org/2000/01/rdf-schema#>
    PREFIX skos:    <http://www.w3.org/2004/02/skos/core#>
    PREFIX spdx:    <http://spdx.org/rdf/terms#>
    PREFIX stax:    <https://w3id.org/stax/ontology#>
    PREFIX xsd:     <http://www.w3.org/2001/XMLSchema#>
"""


def get_data(dataset_name, statistics_type):
    url = f"http://localhost:3030/{dataset_name}/query"
    sparql = SPARQLWrapper(url)
    sparql.setReturnFormat(JSON)
    query = f"""
        {PREFIXES}
        SELECT *
        WHERE {'{'}
          <https://w3id.org/riverbench/datasets/{dataset_name}/{statistics_type}> rb:hasStatistics ?stats .
          ?stats a ?metadata ;
          OPTIONAL {'{'}?stats rbdoc:hasDocWeight ?hasDocWeight {'}'}
          OPTIONAL {'{'}?stats rb:maximum ?maximum {'}'}
          OPTIONAL {'{'}?stats rb:mean ?mean {'}'}
          OPTIONAL {'{'}?stats rb:minimum ?minimum {'}'}
          OPTIONAL {'{'}?stats rb:standardDeviation ?standardDeviation {'}'}
          OPTIONAL {'{'}?stats rb:sum ?sum {'}'}
          OPTIONAL {'{'}?stats rb:uniqueCount ?uniqueCount {'}'}
        {'}'}
    """
    sparql.setQuery(query)
    results = sparql.query().convert()
    data = {
        "dataset": [],
        "metadata": [],
        "hasDocWeight": [],
        "maximum": [],
        "mean": [],
        "minimum": [],
        "standardDeviation": [],
        "sum": [],
        "uniqueCount": [],
    }
    for result in results["results"]["bindings"]:
        for key in data:
            if key in result:
                data[key].append(result[key]["value"])
            else:
                data[key].append(None)
    data["dataset"] = [dataset_name] * len(data["metadata"])
    return pd.DataFrame(data)


def get_eurovoc_themes(dataset_name, predicate="skos:narrower+"):
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
    themes = []
    for result in results["results"]["bindings"]:
        themes.append(result["theme"]["value"].split("/")[-1])
    url_eurovoc = f"http://localhost:3030/{EUROVOC_JENA}/query"
    sparql_eurovoc = SPARQLWrapper(url_eurovoc)
    sparql_eurovoc.setReturnFormat(JSON)
    for theme in themes:
        query_eurovoc = f"""
            {PREFIXES}
            SELECT DISTINCT ?theme ?label
            WHERE {'{'}
                eurovoc:{theme} {predicate} ?theme .
                ?theme skos:prefLabel ?label .
                FILTER(LANG(?label) = "en")
            {'}'}
        """
        sparql_eurovoc.setQuery(query_eurovoc)
        results = sparql_eurovoc.query().convert()
        themes_predicate = []
        for result in results["results"]["bindings"]:
            themes_predicate.append(result["theme"]["value"].split("/")[-1])
        print(theme, themes_predicate)


def main():
    statistics = "dev#statistics-full"
    # statistics = "dev#statistics-100k"
    datasets = [
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
    dir_to_save = f"datasets/{statistics}"
    if not os.path.exists(dir_to_save):
        os.makedirs(dir_to_save)
    dataframe = get_data(datasets[0], statistics)
    for dataset in datasets[1:]:
        dataframe = pd.concat([dataframe, get_data(dataset, statistics)])
    dataframe.to_csv(f"{dir_to_save}/all_datasets.csv", index=False)
    for dataset in datasets:
        print(dataset)
        get_eurovoc_themes(dataset, "skos:related+")
        print()


if __name__ == "__main__":
    main()
