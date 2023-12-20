import os

import pandas as pd
from SPARQLWrapper import JSON, SPARQLWrapper


def get_data(dataset_name, statistics_type):
    url = f"http://localhost:3030/{dataset_name}/query"
    sparql = SPARQLWrapper(url)
    sparql.setReturnFormat(JSON)
    query = f"""
        PREFIX dcat:    <http://www.w3.org/ns/dcat#>
        PREFIX dcterms: <http://purl.org/dc/terms/>
        PREFIX eurovoc: <http://eurovoc.europa.eu/>
        PREFIX foaf:    <http://xmlns.com/foaf/0.1/>
        PREFIX rb:      <https://w3id.org/riverbench/schema/metadata#>
        PREFIX rbdoc:   <https://w3id.org/riverbench/schema/documentation#>
        PREFIX rdfs:    <http://www.w3.org/2000/01/rdf-schema#>
        PREFIX spdx:    <http://spdx.org/rdf/terms#>
        PREFIX stax:    <https://w3id.org/stax/ontology#>
        PREFIX xsd:     <http://www.w3.org/2001/XMLSchema#>
        
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


if __name__ == "__main__":
    main()
