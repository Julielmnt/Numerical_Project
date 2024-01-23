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

def dgo_to_search(town_to_search, river_to_search):
    
    list_assets = ee.data.listAssets('projects/ee-glourb/assets/dgos')['assets']
    id=[]
    update_times = []
    for i in range(len(list_assets)):
            id.append(ee.data.listAssets('projects/ee-glourb/assets/dgos')['assets'][i]['id'])
            update_times.append(ee.data.listAssets('projects/ee-glourb/assets/dgos')['assets'][i]['updateTime'])

    matching_lines = []
    matching_times = []
    for i in range(len(list_assets)):
        if town_to_search.lower() in id[i].lower() or river_to_search.lower() in id[i].lower():
            matching_lines.append(id[i])
            matching_times.append(update_times[i])

    
    return matching_lines, matching_times

def remove_line_by_criteria( id_to_remove):
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
------------------------------------------------------ Metrics --------------------------------------------------------
------------------------------------------------------------------------------------------------------------------"""

def getResults(run_id, properties_list, ee_project_name, overwrite=False, remove_tmp=False):
    ee_tasks = ee.data.getTaskList()
    stacked_uris = [t['destination_uris'] for t in ee_tasks if f'run {run_id}' in t['description'] and t['state'] == 'COMPLETED']
    uris = [uri.split(f'{ee_project_name}/assets/')[1] for sublist in stacked_uris for uri in sublist]

    assets = [f'projects/{ee_project_name}/assets/{uri}' for uri in uris]
    temp_csv_list = [os.path.join(tempdir, f'{os.path.basename(a)}.tmp.csv') for a in assets]

    

    # Create a list to store data for Streamlit file download
    download_data = []

    for assetName, path in zip(assets, temp_csv_list):
        if not os.path.exists(path) or overwrite:
            asset = ee.FeatureCollection(assetName)
            clean_fc = asset.select(propertySelectors=properties_list, retainGeometry=False)

            try:
                # Use Streamlit's st.file_download to add data for download
                st.file_download(path, label=f'Download {os.path.basename(assetName)} CSV')
            except HTTPError:
                # Handle the case if download fails
                st.warning(f"Failed to download {os.path.basename(assetName)} CSV.")

                # If it's impossible to download the cleaned asset, download the complete asset and clean it locally
                st.info(f"Downloading the complete asset {os.path.basename(assetName)} and cleaning it locally.")
                urlretrieve(asset.getDownloadUrl(), path)
                df = pd.read_csv(path, index_col=None, header=0)
                df = df[properties_list]
                df.to_csv(path)
        else:
            continue

        # Add data for Streamlit file download
        download_data.append({
            'asset_name': os.path.basename(assetName),
            'file_path': path
        })

    # You can use download_data for customizing download behavior in Streamlit
    st.write(download_data)

    # You may choose to remove the temporary files if needed
    if remove_tmp:
        for filename in temp_csv_list:
            os.remove(filename)


def run():
    pass
if __name__ == '__main__':
    run()