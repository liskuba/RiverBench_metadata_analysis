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

RADAR_STATISTICS = ["dev#statistics-full", "dev#statistics-100k"]

RADAR_DATAFRAMES_DIRECTORY = "../streamlit_app/data"

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

URL_EUROVOC = f"http://localhost:3030/{EUROVOC_JENA}/query"

EUROVOC_GRAPH_FILEPATH = "../streamlit_app/data/graph_with_eurovoc_themes.pickle"
