#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import ee
import geemap
import tempfile
import streamlit as st
import geopandas as gpd
import os
import numpy as np




"""-----------------------------------------------------------------------------------------------------------------
-------------------------------------------------- Authentication --------------------------------------------------
------------------------------------------------------------------------------------------------------------------"""

def credentials(mail = 'jlimonet@ee-glourb.iam.gserviceaccount.com', key1 = './ee-glourb-58e556f00841.json' , key2 = './ee-glourb-58e556f00841.json'):
    if key1 != "":
        try:
            credentials = ee.ServiceAccountCredentials(mail, key1)
            ee.Initialize(credentials)
            return(True)
            
        except ee.EEException as e:
            return(False) 
        
    if key2 != "":
        try:
            credentials = ee.ServiceAccountCredentials(mail, key2)
            ee.Initialize(credentials)
            return(True)
            
        except ee.EEException as e:
            return(False)

"""-----------------------------------------------------------------------------------------------------------------
------------------------------------------------------ DGOs --------------------------------------------------------
------------------------------------------------------------------------------------------------------------------"""

def upload_dgos(DGO = './example_data/Yamuna_segm_2km_UTF8.shp' , ee_project_name = 'ee-glourb'):
    from glourbee import assets_management
    dgo_assetId, dgo_features = assets_management.uploadDGOs(DGO, ee_project_name=ee_project_name, simplify_tolerance=15)
    return(dgo_assetId, dgo_features)



def display_map(title, location = [0,0], dgo_features = None, zoom = 8):
    import folium
    import geemap
    from streamlit_folium import folium_static

    # Create a folium map
    m = folium.Map(location=location, zoom_start=zoom, title=title)

    if dgo_features:
        features = dgo_features
        folium.GeoJson(data=features.getInfo(), name='DGO Features').add_to(m)

    return(m)


def cities(file_path = 'cities.txt'):
    import re
    with open(file_path, 'r') as file:
        lines = file.readlines()

    pattern = re.compile(r'(\S+),\((-?\d+\.\d+),(-?\d+\.\d+),(-?\d+\.\d+),(-?\d+\.\d+)\)')

    # Create a dictionary to store the extracted data
    city_data = {}

    # Iterate over the lines and extract data
    for line in lines:
        match = pattern.match(line)
        if match:
            city_name, lat1, lon1, lat2, lon2 = match.groups()
            city_data[city_name] = {
                'latitude': (float(lat1) + float(lat2)) /2,
                'longitude': (float(lon1) + float(lon2)) / 2,
        }
    
    return(city_data)

def dgo_to_search(town_to_search, river_to_search, dgo_dataset_path = 'dgos_dataset.txt', print = False):
    with open(dgo_dataset_path, 'r') as file:
        lines = file.readlines()

    matching_lines = [line for line in lines if town_to_search.lower() in line.lower() and river_to_search.lower() in line.lower()]

    if print == True:
        for i,line in enumerate(matching_lines):
            line_parts = line.strip('|').split('|')
            st.write(f'{i+1}- River : {line_parts[0]}, Town : {line_parts[1]}, Uploaded time = {line_parts[2]} \nand id = {line_parts[3]}')
            
    return matching_lines

def remove_line_by_criteria(file_path, town, river, id_to_remove, update_time):
    with open(file_path, 'r') as file:
        lines = file.readlines()

    for i, line in enumerate(lines):
        if town in line and river in line and id_to_remove in line and update_time in line:
            del lines[i]
            break

    # Write the modified content back to the text file
    with open(file_path, 'w') as file:
        file.writelines(lines)

    asset_path_to_delete = id_to_remove
    try:
        ee.data.deleteAsset(asset_path_to_delete)

    except Exception as e:
                st.error(f"Error: {str(e)}")

def add_line(file_path, town, river, id_to_add):
    with open(file_path, 'r') as file:
        lines = file.readlines()
    import pandas as pd
    from datetime import datetime

    df = pd.DataFrame({
        'river': river,
        'town': town,
        'update_time': [datetime.now().strftime("%Y-%m-%d %H:%M")],
        'asset_id': id_to_add
    })
    formatted_rows = df.apply(lambda row: f"|{row['river']}|{row['town']}|{row['update_time']}|{row['asset_id']}|\n", axis=1)

    # Save the formatted rows to a text file
    with open('dgos_dataset.txt', 'a') as file:
        file.write("".join(formatted_rows))


def temp_file_path(uploaded_file):
    # Extract the original file name
    original_filename = uploaded_file.filename  # Assuming the uploaded file has a 'filename' attribute

    # Create a temporary file with the same name and a .shp extension
    with tempfile.NamedTemporaryFile(delete=False, suffix=".shp", prefix=os.path.splitext(original_filename)[0] + "_", mode='wb') as temp_file:
        # Write uploaded file content to the temporary file
        temp_file.write(uploaded_file.read())

        # Get the path of the temporary file
        uploaded_file_path = temp_file.name

    return uploaded_file_path

def uploadDGOs(dgo_shapefile, file_name, simplify_tolerance=15, ee_project_name='ee-glourb'):
    from fiona import drvsupport
    import fiona    
    from glourbee import assets_management
    # Check if drvsupport is None
    # if drvsupport is None:
    #     drvsupport = gpd.io.file.fiona._loading.supported_drivers
    # else:
    #     # Set SHAPE_RESTORE_SHX to YES
    #     drvsupport.supported_drivers['ESRI Shapefile'] = 'YES'

    # # Save the uploaded file to a temporary file
    # temp_file_path = f'./{file_name}'
    # with open(temp_file_path, 'wb') as temp_file:
    #     temp_file.write(dgo_shapefile.read())

    # # Enable support for ESRI Shapefile
    # fiona.drvsupport.supported_drivers['ESRI Shapefile'] = 'YES'

    # Read the shapefile using GeoPandas
    gdf = gpd.read_file(dgo_shapefile)
    gdf['geometry'] = gdf.simplify(simplify_tolerance)

    # If there are fewer than 80 DGOs, import directly into GEE
    if gdf.shape[0] <= 80:
        # Convert GeoDataFrame to Earth Engine FeatureCollection
        dgo_shp = geemap.gdf_to_ee(gdf)

        # Upload the asset
        assetName = f'{os.path.splitext(os.path.basename(file_name))[0]}_{uuid.uuid4().hex}'
        assetId = f'projects/{ee_project_name}/assets/dgos/{assetName}'
        
        if assets_management.uploadAsset(dgo_shp, 'DGOs uploaded from glourbee notebook', assetId):
            # Return the exported asset and its ID
            return assetId, ee.FeatureCollection(assetId)
        else:
            return  # TODO: replace by raise error

    # If there are more than 80 DGOs, split the shapefile for upload and then reassemble
    else:
        nsplit = round(gdf.shape[0] / 80)
        splitted_gdf = np.array_split(gdf, nsplit)

        assets_list = []
        task_list = []

        for n, subgdf in enumerate(splitted_gdf):
            dgo_shp = geemap.gdf_to_ee(subgdf)

            # Upload the asset
            assetName = f'{os.path.splitext(os.path.basename(file_name))[0]}_{uuid.uuid4().hex}'
            assetId = f'projects/{ee_project_name}/assets/dgos/tmp/{assetName}'
            taskid = assets_management.uploadAsset(dgo_shp, 'DGOs uploaded from glourbee notebook', assetId, wait=False)

            if taskid:
                # Add the assetId to the list to merge
                assets_list.append(assetId)

                # Add the taskid to the list of tasks to monitor
                task_list.append(taskid)

                print(f'Import DGOs part {n + 1}/{len(splitted_gdf)} started.')
            else:
                return  # TODO: replace by raise error

        # Wait for the uploads to finish
        assets_management.waitTasks(task_list=task_list)

        # Merge the uploaded assets into one
        output_fc = ee.FeatureCollection([ee.FeatureCollection(asset) for asset in assets_list]).flatten()

        # Upload the asset
        assetName = f'{os.path.splitext(os.path.basename(file_name))[0]}_final_{uuid.uuid4().hex}'
        assetId = f'projects/{ee_project_name}/assets/dgos/{assetName}'
        
        if assets_management.uploadAsset(output_fc, 'DGOs uploaded from glourbee notebook', assetId):
            # Delete temporary assets
            for asset in assets_list:
                ee.data.deleteAsset(asset)

            # Return the final asset and its assetId
            return assetId, ee.FeatureCollection(assetId)
        else:
            return  # TODO: replace by raise error
        

"""-----------------------------------------------------------------------------------------------------------------
------------------------------------------------------ DGOs --------------------------------------------------------
------------------------------------------------------------------------------------------------------------------"""

def run():
    pass
if __name__ == '__main__':
    run()