import streamlit as st


def add_sidebar():
    # Using object notation
    st.sidebar.write("# RiverBench explorer")

    st.sidebar.write("Datasets:")
    st.sidebar.write("[assist-iot-weather](https://riverbench.github.io/datasets/assist-iot-weather/dev/)")
    st.sidebar.write("[assist-iot-weather-graphs](https://riverbench.github.io/datasets/assist-iot-weather-graphs/dev/)")
    st.sidebar.write("[citypulse-traffic](https://riverbench.github.io/datasets/citypulse-traffic/dev/)")
    st.sidebar.write("[citypulse-traffic-graph](https://riverbench.github.io/datasets/citypulse-traffic-graph/dev/)")
    st.sidebar.write("[dbpedia-live](https://riverbench.github.io/datasets/dbpedia-live/dev/)")
    st.sidebar.write("[digital-agenda-indicators](https://riverbench.github.io/datasets/digital-agenda-indicators/dev/)")
    st.sidebar.write("[linked-spending](https://riverbench.github.io/datasets/linked-spending/dev/)")
    st.sidebar.write("[lod-katrina](https://riverbench.github.io/datasets/lod-katrina/dev/)")
    st.sidebar.write("[muziekweb](https://riverbench.github.io/datasets/muziekweb/dev/)")
    st.sidebar.write("[nanopubs](https://riverbench.github.io/datasets/nanopubs/dev/)")
    st.sidebar.write("[politiquices](https://riverbench.github.io/datasets/politiquices/dev/)")
    st.sidebar.write("[yago-annotated-facts](https://riverbench.github.io/datasets/yago-annotated-facts/dev/)")

    st.sidebar.write("")
    st.sidebar.write("")
    st.sidebar.write("")
    st.sidebar.write("")
    st.sidebar.write("")
    st.sidebar.write("")
    st.sidebar.write("")
    st.sidebar.write("")
    st.sidebar.write("")

    columns = st.sidebar.columns(6)
    with columns[1]:
        st.write(
            """<div style="width:100%;text-align:center;">
            <a href="https://riverbench.github.io/" style="float:center">
            <img src="https://riverbench.github.io/assets/riverbench_vector_logo.png" width="44px" caption="xD">
            </img></a></div>""",
            unsafe_allow_html=True)

    with columns[3]:
        st.write(
            """<div style="width:100%;text-align:center;">
            <a href="https://github.com/RiverBench/RiverBench" style="float:center">
            <img src="https://github.githubassets.com/assets/GitHub-Mark-ea2971cee799.png" width="44px">
            </img></a></div>""",
            unsafe_allow_html=True)
    #
    # with columns[3]:
    #     st.write(
    #         """<div style="width:100%;text-align:center;">
    #         <a href="https://streamlit.io" style="float:center">
    #         <img src="http://www.doigtdecole.com/wp-content/uploads/2020/03/logo-rond-twitter.png" width="22px">
    #         </img></a></div>""",
    #         unsafe_allow_html=True)
