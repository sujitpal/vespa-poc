import dashboard_search
import dashboard_mlt

import streamlit as st

PAGES = {
    "Text Search": dashboard_search,
    "MoreLikeThis": dashboard_mlt
}
st.sidebar.title("Navigation")

selection = st.sidebar.radio("Go to", list(PAGES.keys()))
page = PAGES[selection]
page.app()
