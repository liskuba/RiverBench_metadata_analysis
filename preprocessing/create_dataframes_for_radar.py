import os

import pandas as pd
from constants import PREFIXES, RADAR_STATISTICS
from SPARQLWrapper import JSON, SPARQLWrapper


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


def save_dataframes_for_all_datasets(datasets, directory):
    if not os.path.exists(directory):
        os.makedirs(directory)
    for statistic in RADAR_STATISTICS:
        dataframe = get_data(datasets[0], statistic)
        for dataset in datasets[1:]:
            dataframe = pd.concat([dataframe, get_data(dataset, statistic)])
        dataframe.to_csv(f"{directory}/{statistic}_all_datasets.csv", index=False)
