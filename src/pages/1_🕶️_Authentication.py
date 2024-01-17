import streamlit as st
import ee_interface_function as eef
import os

class Authentication:
    def __init__(self, session_state):
        self.title = "authentication"
        self.session_state = session_state

    def show(self):
        try:
            st.title(self.title)
            st.write("This is the Home Page for authentication")

            if "mail" not in st.session_state.keys():
                st.session_state['mail'] = "jlimonet@ee-glourb.iam.gserviceaccount.com"
            if "key" not in st.session_state.keys():
                st.session_state['key'] = "ee-glourb-58e556f00841.json"
            if "uploaded_key" not in st.session_state.keys():
                st.session_state['uploaded_key_path'] = ""

            mail = st.text_input("mail", value=st.session_state['mail'])
            key = st.text_input("key", value=st.session_state['key'])
            uploaded_key = st.file_uploader("Upload file", type=["json"])

            if st.button("Authenticate"):
                if uploaded_key:
                    self.session_state['uploaded_key_path'] = eef.temp_key_path(uploaded_key)

                if key:
                    self.session_state['key_path'] = os.path.abspath(
                        os.path.join(os.getcwd(), str(key))
                    )

                if mail and key or mail and uploaded_key:
                    if eef.credentials(
                        str(mail),
                        self.session_state['key_path'],
                        self.session_state['uploaded_key_path'],
                    ):
                        st.session_state['mail'] = mail
                        st.write("Authentication successful!")
                        self.session_state['authenticated'] = True
                        st.write(self.session_state['authenticated'])
                        st.write(session_state)
                    else:
                        st.write("Authentication failed")
                else:
                    st.write("Please enter mail and key, or mail and upload a JSON file.")
            else:
                st.write("Please enter your credentials.")

        except Exception as e:
            st.error(f"Error: {str(e)}")

    def run(self):
        st.title("GEE Interface")
        self.show()

if __name__ == "__main__":        
    session_state = st.session_state
    authentication = Authentication(session_state)
    authentication.run()