import radar_plot

# TODO: zmienic directory, bo przenioslem dane do steamlit_app/data
directory = "datasets/dev#statistics-full"
path_to_radar_csv = f"{directory}/all_datasets.csv"

radar_plot.generate_radar_plot(path_to_radar_csv)
