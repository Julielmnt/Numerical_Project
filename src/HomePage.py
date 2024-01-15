#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import streamlit as st
import ee_interface_function as eef
import os
import argparse
from pages.Authentication import Authentication
from pages.PageOne import PageOne
from pages.PageTwo import PageTwo
from streamlit.runtime.scriptrunner import RerunData, RerunException
from streamlit.source_util import get_pages
# from streamlit_extras.switch_page_button import switch_page

# def standardize_name(name: str) -> str:
#         return name.lower().replace("_", " ")


# def switch_page(multi_page_app, page_name: str):
#     """
#     Switch page programmatically in a multipage app

#     Args:
#         multi_page_app (MultiPageApp): The instance of the MultiPageApp class
#         page_name (str): Target page name
#     """
    


#     page_name = standardize_name(page_name)

#     pages = multi_page_app.pages  # Access the pages attribute from the MultiPageApp instance

    # for page_name, page_instance in pages.items():  # Iterate over page_name, page_instance pairs
    #     if standardize_name(page_name) == page_name:
    #         raise RerunException(
    #             RerunData(
    #                 page_script_hash=page_instance,
    #                 page_name=page_name,
    #             )
    #         )

    # page_names = [standardize_name(name) for name in pages.keys()]

    # raise ValueError(f"Could not find page {page_name}. Must be one of {page_names}")

# class SessionState:
#     def __init__(self):
#         self.authenticated = False
#         self.mail = "jlimonet@ee-glourb.iam.gserviceaccount.com"
#         self.key = "ee-glourb-58e556f00841.json"
#         self.uploaded_key_path = ""
#         self.key_path = ""


class MultiPageApp:
    def __init__(self):
        self.session_state = self.get_session_state()
        self.pages = {
            "Authentication": Authentication(self.session_state),
            "Page One": PageOne(self.session_state),
            "Page Two": PageTwo(self.session_state),
        }

    @staticmethod
    @st.cache_data(persist=True)
    def get_session_state():
        return {
            "authenticated": False,
            "shared": True,
            "mail": "jlimonet@ee-glourb.iam.gserviceaccount.com",
            "key": "ee-glourb-58e556f00841.json",
            "uploaded_key_path": "",
            "key_path": ""
    }


    def run(self):
        st.title("GEE Interface")
        selection = None


        # for page_name in self.pages.keys():
        #     if st.sidebar.button(page_name):
        #         selection = page_name

        st.write(f"authentication is {self.session_state['authenticated']}")

        # if not self.session_state['authenticated']:
        #     self.pages["Authentication"].show()
        # elif selection:
        #     self.pages[selection].show()
        # else:
        #     st.write("Please select a page.")
        # if selection == "Authentication"  or selection == None:
        #     self.pages["Authentication"].show()

        # if self.session_state.authenticated and selection:
        #     self.pages[selection].show()

        # if not self.session_state.authenticated and selection:
        #     st.write("Please authenticate to access this page.")
                

        # if not self.session_state.authenticated and selection != "Authentication":
        #     switch_page(self, "Authentication")
        # elif selection:
        #     switch_page(self, selection)
        # else:
        #     st.write("Please select a page.")


def run():
    parser = argparse.ArgumentParser(
            "Google Earth Engine Interface",
            description="Interface for Google Earth Engine"
            "You can Authenticate and then load your DGOs and perform your analysis by choosing layers and metrics."
            "\n You then can visualize and download your analysis.",
        )

    args = parser.parse_args()

    app = MultiPageApp()
    app.run()


if __name__ == "__main__":
    run()
