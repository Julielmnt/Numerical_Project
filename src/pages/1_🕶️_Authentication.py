import streamlit as st
import ee_interface_function as eef
import os

class Authentication:
    def __init__(self, session_state):
        self.title = "Authentication"
        self.session_state = session_state

    def show(self):
        image_path = '..\logo.svg'  
        st.image(image_path,  use_column_width=True, width=5)
        try:
            st.title(self.title)
            st.write("Here you can authenticate to Earth Engine with your mail and key (a json file)")

            if "mail" not in st.session_state.keys():
                st.session_state['mail'] = "jlimonet@ee-glourb.iam.gserviceaccount.com"
            if "key" not in st.session_state.keys():
                st.session_state['key'] = "ee-glourb-58e556f00841.json"
            if "uploaded_key" not in st.session_state.keys():
                st.session_state['uploaded_key_path'] = ""

            mail = st.text_input("mail", value=st.session_state['mail'], help = 'Your mail to authenticate, else use the default value')
            key = st.text_input("key", value=st.session_state['key'], help = 'If your json key is in the same folder as the app, else use the file uploader')
            uploaded_key = st.file_uploader("Upload file", type=["json"], help = 'Here you can upload your json file !')

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
                        st.write("Authentication successful ! ")
                        st.write("You can now go about your business :dark_sunglasses:")
                        self.session_state['authenticated'] = True
                        # st.write(self.session_state['authenticated'])
                        # st.write(session_state)
                    else:
                        st.write("Authentication failed")
                else:
                    st.write("Please enter mail and key, or mail and upload a JSON file.")
            else:
                st.write("Please enter your credentials.")

        except Exception as e:
            st.error(f"Error: {str(e)}")

    def run(self):
        self.show()

if __name__ == "__main__":        
    session_state = st.session_state
    authentication = Authentication(session_state)
    authentication.run()