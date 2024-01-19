import numpy as np
import pandas as pd
import plotly.graph_objects as go
import streamlit as st


def generate_box_plot(df, datasets, metadata, metric):
    pass
    # df = df[(df.stream_size == 'full') & (df.stream_type == 'stream')]
    #
    # data = []
    #
    # fig = go.Figure()
    #
    # # for i in range(len(datasets)):
    # #     y1 = np.random.randn(50) + 1  # shift mean
    # #     fig.add_trace(go.Box(y=[]*len(datasets)))#[[]*len(datasets)])),#df[(df.dataset == datasets[i]) & (df.metadata == metadata)]['mean'].to_numpy(),
    # #                         # name=datasets[i],#)#)
    # #                         #  q1=df[(df.dataset == datasets[i]) & (df.metadata == metadata)]['mean'].to_numpy(),
    # #                         #  median=df[(df.dataset == datasets[i]) & (df.metadata == metadata)]['mean'].to_numpy(),
    # #                         #  q3=df[(df.dataset == datasets[i]) & (df.metadata == metadata)]['mean'].to_numpy(),
    # #                         #  lowerfence=df[(df.dataset == datasets[i]) & (df.metadata == metadata)][
    # #                         #      'minimum'].to_numpy(),
    # #                         #  upperfence=df[(df.dataset == datasets[i]) & (df.metadata == metadata)][
    # #                         #      'maximum'].to_numpy(),
    # #                         #  mean=df[(df.dataset == datasets[i]) & (df.metadata == metadata)]['mean'].to_numpy(),
    # #                         #  sd=df[(df.dataset == datasets[i]) & (df.metadata == metadata)][
    # #                         #      'standardDeviation'].to_numpy())
    # #                   #)
    #
    #     # fig.add_trace(go.Box(y=y1, name='Sample B',
    #     #                      marker_color='lightseagreen'))
    # # for i in range(len(datasets)):
    # #     fig.add_trace(go.Box(name=datasets[i],
    # #                          y=[1, 2, 3, 4],#)#)
    # #                          q1=df[(df.dataset == datasets[i]) & (df.metadata == metadata)]['mean'].to_numpy(),
    # #                          median=df[(df.dataset == datasets[i]) & (df.metadata == metadata)]['mean'].to_numpy(),
    # #                          q3=df[(df.dataset == datasets[i])& (df.metadata == metadata)]['mean'].to_numpy(),
    # #                          lowerfence=df[(df.dataset == datasets[i])& (df.metadata == metadata)][
    # #                              'minimum'].to_numpy(),
    # #                          upperfence=df[(df.dataset == datasets[i]) & (df.metadata == metadata)][
    # #                              'maximum'].to_numpy(),
    # #                          mean=df[(df.dataset == datasets[i]) & (df.metadata == metadata)]['mean'].to_numpy(),
    # #                          sd=df[(df.dataset == datasets[i]) & (df.metadata == metadata)][
    # #                              'standardDeviation'].to_numpy()))
    #
    # fig.add_trace()
    # fig.add_trace(go.Box(y=[
    #     [0, 1],
    #     [0, 1],
    #     [0, 1],
    #     [0, 1]
    # ], name="Precompiled Quartiles", boxpoints=False, ))
    #
    #
    #     # fig.add_trace(go.Box(y=[[None] * len(datasets)
    #     #                         ], name="Precompiled Quartiles"))
    #
    #     # fig.update_traces(q1=[1, 2, 3], median=[4, 5, 6],
    #     #                   q3=[7, 8, 9], lowerfence=[-1, 0, 1],
    #     #                   upperfence=[5, 6, 7], mean=[2.2, 2.8, 3.2],
    #     #                   sd=[0.2, 0.4, 0.6], notchspan=[0.2, 0.4, 0.6])
    #     #
    # fig.update_traces(
    #    # name=df[(df.dataset.isin(datasets)) & (df.metadata == metadata)]['dataset'].to_numpy(),
    #     q1=df[(df.dataset.isin(datasets)) & (df.metadata == metadata)]['mean'].to_numpy(),
    #     median=df[(df.dataset.isin(datasets)) & (df.metadata == metadata)]['mean'].to_numpy(),
    #     q3=df[(df.dataset.isin(datasets)) & (df.metadata == metadata)]['mean'].to_numpy(),
    #     lowerfence=df[(df.dataset.isin(datasets)) & (df.metadata == metadata)]['minimum'].to_numpy(),
    #     upperfence=df[(df.dataset.isin(datasets)) & (df.metadata == metadata)]['maximum'].to_numpy(),
    #     mean=df[(df.dataset.isin(datasets)) & (df.metadata == metadata)]['mean'].to_numpy(),
    #     sd=df[(df.dataset.isin(datasets)) & (df.metadata == metadata)]['standardDeviation'].to_numpy())
    #     #notchspan=[0.2, 0.4, 0.6])
    #
    # st.write(fig)
