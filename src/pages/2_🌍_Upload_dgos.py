import streamlit as st
import ee_interface_function as eef
import ee
import folium
from streamlit_folium import folium_static

class PageOne:
    cities_data = eef.cities('cities.txt')

    def __init__(self, session_state):
        self.title = "Loading DGOs"
        self.shp_file = None
        self.ee_project_name = "ee-glourb"
        self.dgo_features = None
        self.session_state = session_state
        self.cities_data = eef.cities('cities.txt')
        self.list_cities = list(self.cities_data.keys())
        self.id = None
        self.map_container = st.empty() 
        self.feature_group = folium.FeatureGroup(name='DGO Features')
        self.town = None
        self.river = None
        self.matching_lines = None
        self.action = None

    def update_map(self):
        location = [self.cities_data[self.town]["latitude"], self.cities_data[self.town]["longitude"]]
        m = folium.Map(location=location, zoom_start=8, title='DGO map')

        features = self.session_state['dgo_features']
        if features:
            folium.GeoJson(data=features.getInfo()).add_to(self.feature_group)
            self.feature_group.add_to(m)

        folium_static(m)

    def show(self):
        st.title(self.title)
        dgo_dataset_path = 'dgos_dataset.txt'

        self.town = st.selectbox('Town', self.list_cities)
        self.river = st.text_input('River')

        if self.river:
            self.matching_lines = eef.dgo_to_search(self.town, self.river, dgo_dataset_path)
            if len(self.matching_lines) != 0:
                st.write('Here are the dgos already loaded as assets for the same town and river:')
                self.matching_lines = eef.dgo_to_search(self.town, self.river, dgo_dataset_path, print=True)

                st.write('Select an action:')
                self.action = st.radio('', ['Use already uploaded DGOs', 'Upload my own DGOs'])

                if self.action == 'Use already uploaded DGOs':
                    if len(self.matching_lines) > 1:
                        i = st.number_input('Number of the asset you want', 1, len(self.matching_lines), step=1)
                        self.id = self.matching_lines[i - 1].strip('|').split('|')[3]
                        st.write(f'You\'re using the asset number {i} with the id: {self.id}')
                        self.session_state['dgo_features'] = ee.FeatureCollection(self.id)
                        st.write({self.session_state['dgo_features']})

                    elif len(self.matching_lines) == 1:
                        i = 1
                        
                    else:
                        i = None

                    if i is not None:
                        self.id = self.matching_lines[i - 1].strip('|').split('|')[3]
                        st.write(f'You\'re using the asset number {i} with the id: {self.id}')
                        self.session_state['dgo_features'] = ee.FeatureCollection(self.id)
                        st.write({self.session_state['dgo_features']})

                elif self.action == 'Upload my own DGOs':
                    st.write('Do you want to replace an already loaded asset? (in order to not overcrowd the server)')
                    replace_asset = st.radio('Choose an option:', ['Yes', 'No'])

                    if replace_asset == 'Yes':
                        if len(self.matching_lines) > 1:
                            i = st.number_input('Number of the asset you want to remove', 1, len(self.matching_lines), step=1)
                            id_to_remove = self.matching_lines[i - 1].strip('|').split('|')[3]
                            update_time = self.matching_lines[i - 1].strip('|').split('|')[2]
                        elif len(self.matching_lines) == 1:
                            i = 1
                            id_to_remove = self.matching_lines[i - 1].strip('|').split('|')[3]
                            update_time = self.matching_lines[i - 1].strip('|').split('|')[2]
                            st.write(self.matching_lines)
                            st.write(id_to_remove)
                            st.write(update_time)
                        else:
                            i = None

                        if i is not None:
                            st.write(f'You\'re removing the asset number {i} with the id: {id_to_remove}')
                            if st.button('Confirm'):
                                eef.remove_line_by_criteria(dgo_dataset_path, self.town, self.river, id_to_remove, update_time)
                                st.write('Let\'s now load the dgos !')
                                self.shp_file = st.file_uploader("Upload Shape file", type=["shp"])

                    elif replace_asset == 'No':
                        self.shp_file = st.file_uploader("Upload Shape file", type=["shp"])

            else : 
                self.shp_file = st.file_uploader("Upload Shape file", accept_multiple_files = True)

        if self.shp_file:
            import io
            import os
            st.write(self.shp_file) 
            from glourbee import assets_management
            import geopandas as gpd

            dgo_shapefile = self.shp_file
            temp_dir = "./temp"
            os.makedirs(temp_dir, exist_ok=True)

            file_paths = {}
            for file in dgo_shapefile:
                file_path = os.path.join(temp_dir, file.name)
                with open(file_path, 'wb') as temp_file:
                    temp_file.write(file.read())
                file_paths[file.name] = file_path

            # Read the shapefile using GeoPandas
            try:
                gdf = gpd.read_file(file_paths['Yamuna_segm_2km_UTF8.shp'])
                st.write(gdf)
                st.write('it worked !')
            except Exception as e:
                st.error(f"Error reading the shapefile: {e}")
                return

            self.dgo_assetId, self.dgo_features = assets_management.uploadDGOs(file_paths['Yamuna_segm_2km_UTF8.shp'],  ee_project_name=self.ee_project_name, simplify_tolerance=15)

            eef.add_line(dgo_dataset_path, self.town, self.river, self.dgo_assetId)
            for file_path in file_paths.values():
                os.remove(file_path)

        self.update_map()

if __name__ == "__main__":        
    pageOne = PageOne(st.session_state)
    pageOne.show()