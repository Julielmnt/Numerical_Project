#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import streamlit as st
import pandas as pd


# add_selectbox = st.sidebar.selectbox(
#     "How would you like to be contacted?",
#     ("Email", "Home phone", "Mobile phone")
# )

class PageOne:
    def __init__(self):
        self.title = 'Page One'

    def show(self):
        st.title(self.title)
        st.write("This is the content for Page One.")

class PageTwo:
    def __init__(self):
        self.title = 'Page Two'

    def show(self):
        st.title(self.title)
        st.write("Welcome to Page Two.")

class MultiPageApp:
    def __init__(self):
        self.pages = {
            'Page One': PageOne(),
            'Page Two': PageTwo()
        }
    
    def run(self):
        st.title('Multi-Page Streamlit App')
        selection = st.sidebar.button("Page One")  # Button for Page One
        if selection:
            self.pages['Page One'].show()

        selection = st.sidebar.button("Page Two")  # Button for Page Two
        if selection:
            self.pages['Page Two'].show()



def main():
    app = MultiPageApp()
    app.run()

if __name__ == '__main__':
    main()