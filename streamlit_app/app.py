# import radar_plot
#
# path_to_radar_csv = f"streamlit_app/data/dev#statistics-full_all_datasets.csv"
#
# radar_plot.generate_radar_plot(path_to_radar_csv)
import streamlit as st
import pandas as pd
import numpy as np
import os

from streamlit_option_menu import option_menu

from radar_plot import generate_radar_plot
from line_plot import generate_line_plot
from bar_plot import generate_bar_plot
from box_plot import generate_box_plot

@st.cache_data
def load_metadata():
    def read_dataset_sizes():
        df_sizes = pd.read_csv(os.path.join('streamlit_app', 'data', 'all_datasets_sizes.csv'))
        df_stats_10k = pd.read_csv(os.path.join('streamlit_app', 'data', 'dev#statistics-10k_all_datasets.csv'))
        df_stats_100k = pd.read_csv(os.path.join('streamlit_app', 'data', 'dev#statistics-100k_all_datasets.csv'))
        df_stats_full = pd.read_csv(os.path.join('streamlit_app', 'data', 'dev#statistics-full_all_datasets.csv'))

        return df_sizes, df_stats_10k, df_stats_100k, df_stats_full

    df_sizes, df_stats_10k, df_stats_100k, df_stats_full = read_dataset_sizes()

    df_stats_10k['stream_size'] = '10k'
    df_stats_100k['stream_size'] = '100k'
    df_stats_full['stream_size'] = 'full'

    df_stats = pd.concat([df_stats_10k, df_stats_100k, df_stats_full])
    df_all = pd.merge(df_sizes, df_stats, on=['dataset', 'stream_size'], how='inner')
    df_all['metadata'] = df_all.apply(lambda row: row.metadata.split('#')[1].removesuffix('Statistics'), axis=1)

    return df_all


df = load_metadata()

# def on_change(key):
#     selection = st.session_state[key]
#     st.write(f"Selection changed to {selection}")


selected_tab = option_menu(None, ["RadarPlot", "BarPlot", "LinePlot", 'BoxPlot', 'EuroVoc'],
                           icons=['radar', 'bar-chart', "graph-up", 'box', 'balloon'],
                           key='menu', orientation="horizontal")  # on_change=on_change

datasets = st.multiselect(
    "Datasets",
    df["dataset"].unique().tolist(),
    df["dataset"].unique().tolist()[:4],
)

# if 'metadata_single' not in st.session_state:
#     st.session_state['metadata_single'] = df["metadata"].unique().tolist()[1]
# else:
#     metadata_single = st.session_state['metadata_single']

if selected_tab == "RadarPlot" or selected_tab == "BarPlot":
    metadata_multi = st.multiselect(
        "Metadata",
        df["metadata"].unique().tolist(),
        df["metadata"].unique().tolist()[:5],
    )

else:
    stateful_index = 0 if 'metadata_single' not in st.session_state else st.session_state['metadata_single']
    metadata_single = st.selectbox(
        "Metadata",
        df["metadata"].unique().tolist(),
        index=stateful_index,
    )
    st.session_state['metadata_single'] = df["metadata"].unique().tolist().index(metadata_single)



metric = st.selectbox(
    "Metric",
    ("maximum", "mean", "minimum", "standardDeviation", "sum", "uniqueCount"),  # df["metadata"].unique().tolist(),
    index=1,
)

if selected_tab == "RadarPlot":
    generate_radar_plot(df, datasets, metadata_multi, metric)
elif selected_tab == "BarPlot":
    generate_bar_plot(df, datasets, metadata_multi, metric)
elif selected_tab == "LinePlot":
    generate_line_plot(df, datasets, metadata_single, metric)
elif selected_tab == "BoxPlot":
    generate_box_plot(df, datasets, metadata_single, metric)
    #generate_bar_plot()
elif selected_tab == "EuroVoc":
    pass

# if selected == "RadarPlot":
#     st.write("home is where the heart is")
# else:
#     st.write("settings is my bettings")
