import base64
import streamlit as st
import pandas as pd
from pg_utils_fn import create_entity_name_list, fetch_block_mapping, fetch_gp_mapping
from pg_utils_fn import fetch_district_mapping
from pg_utils_fn import populate_entity_mapping
from pg_utils_fn import load_file
from utils import update_all_data
from pg_utils_fn import create_village_mapped_dataset, populate_village_mapping, process_file
from pg_utils_fn import create_sub_district_mapped_dataset, populate_sub_district_mapping
from pg_utils_fn import create_gp_mapped_dataset, populate_gp_mapping
from pg_utils_fn import create_block_mapped_dataset, populate_block_mapping
from pg_utils_fn import generate_download_link
from pg_utils_fn import update_variations
from pg_utils_fn import create_district_mapped_dataset
from pg_utils_fn import create_mapped_dataset, get_state_mappings
from databasefn import insert_record



"""
    Generates the state mapping page which allows users to upload a CSV or Excel file containing a 'state_name' column. 
    It then creates a mapped dataset which contains a state_code column based on the state_name column in the uploaded dataset. 
    It also allows users to update the state name variations and download the mapped dataset. 
    If the district_mapping_button is clicked, it redirects to the district mapping page. 
    
    Parameters:
    ----------
    dataset_selected: bool, optional
        Default value is False. If True, the 'dataset_file' is obtained from the session state. If False, it prompts the user to upload a dataset file.

    Returns:
    ----------
    None
"""


st.title('State LGD Mapping')
#st.set_page_config(page_title="State Mapping Page", page_icon="📊")

st.markdown("State Mapping Page")
st.sidebar.header("State Mapping Page")
dataset_selected = False

if not dataset_selected:
    dataset_file = st.file_uploader('Upload dataset', type=['csv', 'xlsx'])
    if dataset_file is None:
        st.warning("Please upload a dataset file.")
else:
    dataset_file = st.session_state['dataset_file']

dataset = process_file(dataset_file)

if dataset_file is None:
    st.warning("Please upload a dataset file.")
if 'state_name' not in dataset.columns:
    st.error("Error: The dataset does not contain the 'state_name' column.")

st.subheader("Before State LGD Mapping")
st.write(dataset.head())
with st.spinner("Processing..."):
    state_mapping = get_state_mappings()
    mapped_dataset = create_mapped_dataset(dataset, state_mapping)
    unmatched_names = mapped_dataset[mapped_dataset['state_code'] == -2]['state_name']

if unmatched_names.empty:
    st.success('No Unmatched State Names')
    mapped_dataset.to_csv('data.csv', index=False)

    st.subheader("After State LGD Mapping")
    with st.spinner("Processing..."):
        st.write(mapped_dataset.head())
        generate_download_link(mapped_dataset)

    if st.button('Start District Mapping', key='district_mapping_button'):
        if 'district_name' not in mapped_dataset.columns:
            st.error("Error: The dataset does not contain the 'district_name' column.")
            
else:
    st.subheader('Unmatched State Names')
    st.write(unmatched_names.unique())
    note = "Please provide the state name variations separated by commas or a single state name."
    st.info(note)
    st.subheader('Update State Name Variations')
    state_mapping = get_state_mappings()
    mapped_dataset = create_mapped_dataset(dataset, state_mapping)
    unmatched_names = mapped_dataset[mapped_dataset['state_code'] == -2]['state_name']
    entity_table_name = "states"
    update_variations(unmatched_names.unique(), state_mapping, entity_table_name)
    unmatched_names = mapped_dataset[mapped_dataset['state_code'] == -2]['state_name']
    
    if unmatched_names.empty:
        st.write(mapped_dataset.head())
        mapped_dataset.to_csv('data.csv', index=False)
        generate_download_link(mapped_dataset)
        if st.button('Start District Mapping', key='district_mapping_button'):
            if 'district_name' not in mapped_dataset.columns:
                st.error("Error: The dataset does not contain the 'district_name' column.")
                