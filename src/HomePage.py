#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import streamlit as st
import ee_interface_function as eef
import os
import argparse
# from pages.Authentication import Authentication
# from pages.PageOne import PageOne
# from pages.PageTwo import PageTwo
from streamlit.runtime.scriptrunner import RerunData, RerunException
from streamlit.source_util import get_pages

class MultiPageApp:
    def __init__(self):
        self.session_state = self.get_session_state()
        # self.pages = {
        #     "Authentication": Authentication(self.session_state),
        #     "Page One": PageOne(self.session_state),
        #     "Page Two": PageTwo(self.session_state),
        # }
        # self.selected_page = st.sidebar.selectbox("Select a page", list(self.pages.keys()))


    @staticmethod
    @st.cache_data(persist=True)
    def get_session_state():
        return {
            "authenticated": False,
            "mail": "jlimonet@ee-glourb.iam.gserviceaccount.com",
            "key": "ee-glourb-58e556f00841.json",
            "uploaded_key_path": "",
            "key_path": ""
    }


    def run(self):
        st.title("GEE Interface")
        st.write("Hello")
        st.write(session_state)
        # self.pages[self.selected_page].show()

if __name__ == "__main__":
    
    session_state = st.session_state 
    if "authenticated" not in st.session_state:
        st.session_state['authenticated'] = False
        
    app = MultiPageApp()
    
    app.run()




# def run():
#     parser = argparse.ArgumentParser(
#             "Google Earth Engine Interface",
#             description="Interface for Google Earth Engine"
#             "You can Authenticate and then load your DGOs and perform your analysis by choosing layers and metrics."
#             "\n You then can visualize and download your analysis.",
#         )

#     args = parser.parse_args()

#     app = MultiPageApp()
#     app.run()