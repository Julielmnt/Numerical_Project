import streamlit as st

class PageTwo:
    def __init__(self, session_state):
        self.title = "Page Two"
        self.session_state = session_state

    
    def show(self):
        st.title(self.title)
        st.write("Welcome to Page Two.")