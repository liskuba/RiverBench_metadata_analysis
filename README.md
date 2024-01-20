# RiverBench_metadata_analysis

https://riverbench.github.io/

[Sowinski et al., 2023] Sowinski, P., Ganzha, M., and Paprzycki, M. (2023). Riverbench: an open rdf
streaming benchmark suite. arXiv preprint arXiv:2305.06226.]

## How to run the app?

0. Install requirements. We were running this app with python=3.10.
1. Upload all datasets (for example `.ttl` files) with metadata to Apache Jena on the standard port (3030) of localhost.
2. Also, upload EuroVoc data to Apache Jena. You can download it from https://data.europa.eu/data/datasets/eurovoc?locale=en - data `EuroVoc SKOS_AP_EU distribution` in RDF/Turtle format.
3. Run `main.py` from the preprocessing directory. It may take a while.
4. Run the app with the command `streamlit run streamlit_app/app.py`.

