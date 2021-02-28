import pandas as pd
import streamlit as st

import demo_utils


def app():
    st.title("Demo :: Search")

    query = st.text_input("Query String:")
    title_only = st.checkbox("Search Titles only?")
    start_row = st.number_input("Start row", value=0)
    num_rows = st.number_input("Number of rows", value=10)
    
    if st.button("Query"):
        rows = demo_utils.do_search(query, title_only, start_row, num_rows)
        st.write("## Results {:d}-{:d} for '{:s}'".format(
            start_row, start_row + num_rows, query))
        results = pd.DataFrame(rows)
        st.table(results)

    
