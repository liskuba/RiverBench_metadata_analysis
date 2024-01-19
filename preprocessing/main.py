from constants import (AVG_SHORTEST_PATH_FILEPATH, DATASETS,
                       DATASETS_THEMES_FILEPATH, EUROVOC_GRAPH_FILEPATH,
                       RADAR_DATAFRAMES_DIRECTORY)
from create_dataframes_for_radar import save_dataframes_for_all_datasets
from eurovoc_shortest_path import (calculate_all_avg_shortest_path,
                                   load_eurovoc_to_graph, save_graph,
                                   save_themes_for_datasets)


def main():
    save_dataframes_for_all_datasets(DATASETS, RADAR_DATAFRAMES_DIRECTORY)
    G, edge_labels = load_eurovoc_to_graph()
    save_graph(G, EUROVOC_GRAPH_FILEPATH)
    save_themes_for_datasets(DATASETS, DATASETS_THEMES_FILEPATH)
    calculate_all_avg_shortest_path(
        DATASETS,
        AVG_SHORTEST_PATH_FILEPATH,
        EUROVOC_GRAPH_FILEPATH,
        DATASETS_THEMES_FILEPATH,
    )


if __name__ == "__main__":
    main()
