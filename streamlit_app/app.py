import radar_plot
import sidebar


sidebar.add_sidebar()

directory = "datasets/dev#statistics-full"
path_to_radar_csv = f"{directory}/all_datasets.csv"
radar_plot.generate_radar_plot(path_to_radar_csv)
