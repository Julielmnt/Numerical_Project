#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import streamlit as st
import ee_interface_function as eef
import tempfile
import os


class HomePage:
    def __init__(self):
        self.title = "Authentification"

    def show(self):
        st.title(self.title)
        st.write("This is some content")

        if "user_input_1" not in st.session_state:
            st.session_state.user_input_1 = ""
        if "user_input_2" not in st.session_state:
            st.session_state.user_input_2 = ""
        if "user_input_2" not in st.session_state:
            st.session_state.uploaded_file = ""

        st.title("Please Enter your credentials")
        user_input_1 = st.text_input("mail", value=st.session_state.user_input_1)
        user_input_2 = st.text_input("key", value=st.session_state.user_input_2)

        # @st.cache_data()
        # def get_uploaded_file(uploaded_file):
        #     return uploaded_file

        uploaded_file = st.file_uploader("Upload file", type=["json"])
        # uploaded_file_cached = get_uploaded_file(uploaded_file)

        if st.button("Run Function"):
            if uploaded_file:
                # Create a temporary file
                temp_file = tempfile.NamedTemporaryFile(delete=False)

                # Write uploaded file content to the temporary file
                temp_file.write(uploaded_file.read())

                # Get the path of the temporary file
                uploaded_file_path = temp_file.name

                # Close the temporary file
                temp_file.close()
            else:
                uploaded_file_path = ""

            if user_input_2:
                file_path = os.path.abspath(
                    os.path.join(os.getcwd(), str(user_input_2))
                )

            if user_input_1 and user_input_2 or user_input_1 and uploaded_file:
                if eef.credentials(str(user_input_1), file_path, uploaded_file_path):
                    st.write("Authentication successful!")
                else:
                    st.write("Authentication failed")
            else:
                st.write("Please enter mail, key, and upload a JSON file.")
        else:
            st.write("Please enter a value.")


class PageOne:
    def __init__(self):
        self.title = "Page Two"

    def show(self):
        st.title(self.title)


class PageTwo:
    def __init__(self):
        self.title = "Page Two"

    def show(self):
        st.title(self.title)
        st.write("Welcome to Page Two.")


class MultiPageApp:
    def __init__(self):
        self.pages = {"Page One": PageOne(), "Page Two": PageTwo()}

    def run(self):
        st.title("Multi-Page Streamlit App")
        HomePage().show()
        selection = st.sidebar.button("Page One")  # Button for Page One
        if selection:
            self.pages["Page One"].show()

        selection = st.sidebar.button("Page Two")  # Button for Page Two
        if selection:
            self.pages["Page Two"].show()


def run():
    app = MultiPageApp()
    app.run()


if __name__ == "__main__":
    run()
