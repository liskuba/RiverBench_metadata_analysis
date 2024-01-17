from eurovoc_shortest_path import load_eurovoc_to_graph, save_graph
from constants import EUROVOC_GRAPH_FILEPATH, RADAR_DATAFRAMES_DIRECTORY, DATASETS
from create_dataframes_for_radar import save_dataframes_for_all_datasets


def main():
    save_dataframes_for_all_datasets(DATASETS, RADAR_DATAFRAMES_DIRECTORY)
    G, edge_labels = load_eurovoc_to_graph()
    save_graph(G, EUROVOC_GRAPH_FILEPATH)


if __name__ == "__main__":
    main()
