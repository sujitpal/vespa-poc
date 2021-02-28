import pandas as pd
import streamlit as st

import demo_utils


def app():
    st.title("Demo :: More Like This")

    cord_uid = st.text_input("Doc ID for 'This' document:")
    num_rows = st.number_input("Number of similar documents", value=10)

    if st.button("More Like This"):
        doc_title, rows = demo_utils.do_mlt(cord_uid, num_rows)
        st.write("## Top {:d} MLT Results for '{:s}' ({:s}))".format(
            num_rows, doc_title, cord_uid))
        results = pd.DataFrame(rows)
        st.table(results)

