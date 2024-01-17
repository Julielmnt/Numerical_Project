import streamlit as st
import ee_interface_function as eef


class PageOne:
    cities_data = eef.cities('cities.txt')

    def __init__(self, session_state):
        self.title = "Loading DGOs"
        self.shp_file = None
        self.ee_project_name = "ee-glourb"
        self.dgo_features = None
        self.session_state = session_state
        self.list_cities = list(self.cities_data.keys())

    def show(self):
        if self.session_state['authenticated']:
            st.title(self.title)
            self.ee_project_name = st.text_input("Project Name", value=self.ee_project_name)
            town = st.selectbox('Town', self.list_cities)
            self.shp_file = st.file_uploader("Upload Shape file", type=["shp"])
            st.write(self.session_state)

            if self.shp_file:
                shp_key_path = eef.temp_key_path(self.shp_file)
                self.dgo_assetId, self.dgo_features = eef.assets(
                    shp_key_path,
                    ee_project_name=self.ee_project_name,
                    simplify_tolerance=15,
                )

            if self.dgo_features is not None:
                if st.button("Load Map"):
                    map_object = eef.plot_map(self.dgo_features)
                    st.pydeck_chart(map_object)  # Or use st.map(map_object) if applicable
        
        else : 
            st.write('Please, authenticate first :)')


if __name__ == "__main__":        
    pageOne = PageOne(st.session_state)
    pageOne.show()