import streamlit as st

import streamlit as st
import ee_interface_function as eef
import ee


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
        dgo_dataset_path = 'dgos_dataset.txt'

        if self.session_state['authenticated']:
            st.title(self.title)
            self.ee_project_name = st.text_input("Project Name", value=self.ee_project_name)
            town = st.selectbox('Town', self.list_cities)
            river = st.text_input('River')

            matching_lines = eef.dgo_to_search(town, river, dgo_dataset_path)
            if river:
                if len(matching_lines) != 0:
                    st.write('Here are the dgos already loaded as assets for the same town and river')
                    matching_lines = eef.dgo_to_search(town, river, dgo_dataset_path, print = True)


                    st.write('Do you want to use the already uploaded asset or upload your own (it will take time and careful to not upload something already on the server)')
                    col1, col2 = st.columns(2)
                    if col1.button('Use already uploaded DGOs'):
                        if len(matching_lines) > 1:
                            i = st.number_input('Number of the asset you want', 1, len(matching_lines), step = 1)
                            id = matching_lines[i-1].strip('|').split('|')[3]
                            self.dgo_features = ee.FeatureCollection(id)
                            if st.button('Display Map'):
                                map_object = eef.plot_map(self.dgo_features)
                                st.pydeck_chart(map_object)  

                            

                if col2.button('Upload my own DGOs'):
                    st.write('Do you want to replace an already loaded asset ?')
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
                if st.button("Display Map"):
                    map_object = eef.plot_map(self.dgo_features)
                    st.pydeck_chart(map_object)  
        
        else : 
            st.write('Please, authenticate first :)')


if __name__ == "__main__":        
    pageOne = PageOne(st.session_state)
    pageOne.show()