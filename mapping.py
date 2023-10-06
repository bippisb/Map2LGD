import sqlite3
import streamlit as st
import pandas as pd
from collections import defaultdict
import base64
import multiprocessing

from pg_utils_fn import create_mapped_dataset, get_state_mappings



def create_gp_mapped_dataset(dataset, mapping):
    """
    Create a mapped dataset by associating gp codes with gp names in the dataset.
    """
    dataset['panchayat_name'] = dataset['panchayat_name'].str.strip()
    dataset['gp_code'] = dataset['panchayat_name'].str.lower().map(mapping)
    dataset.loc[dataset['gp_code'].isnull(), 'gp_code'] = -2
    return dataset

def fetch_gp_mapping():
    """
    Fetch the gp mapping from the SQLite database.

    Returns:
    - A list of tuples containing the gp entity name, LGD code, name variants, and parent entity.
    """
    # Connect to the SQLite database
    conn = sqlite3.connect('lgd_database.db')
    cursor = conn.cursor()

    # Retrieve gp data from the 'gps' table
    cursor.execute("SELECT entityName, entityLGDCode, entityNameVariants, entityParent FROM gp")
    data = cursor.fetchall()

    # Close the database connection
    conn.close()

    return data

def populate_gp_mapping():
    """
    Populates a gp mapping dictionary using data from a database and a local file.

    Returns:
        A defaultdict containing the mapping of gp names to their respective codes.
    """
    state_dataset = pd.read_csv('data.csv')
    data = fetch_gp_mapping()
    unique_rows = state_dataset.drop_duplicates(subset=['panchayat_name'])
    unique_rows_lower = unique_rows.apply(lambda x: (x['panchayat_name'].strip().lower(), x['block_code']), axis=1).tolist()

    entity_mapping = {}
    edname = "Not Available"
    for entity_name, entity_code, entity_variants, parent_code in data:
        for row in unique_rows_lower:
            entity_name_lower = row[0]
            state_code = row[1]
            if entity_name_lower == entity_name.lower() :
                if int(parent_code) == int(state_code) :
                    entity_mapping[entity_name_lower.lower()] = entity_code
                    if entity_variants:
                        for variant in entity_variants.split(','):
                            entity_mapping[variant.strip().lower()] = entity_code

    return entity_mapping



import pandas as pd


def main_gp():
    gp_dataset = pd.read_csv('data.csv')
    gp_mapping = populate_gp_mapping()

    mapped_dataset = create_gp_mapped_dataset(gp_dataset, gp_mapping)

    unmatched_names = mapped_dataset[mapped_dataset['gp_code'] == -2]['panchayat_name']
    return unmatched_names,mapped_dataset



def main_state(dataset):
    state_mapping = get_state_mappings()
    mapped_dataset = create_mapped_dataset(dataset, state_mapping)
    unmatched_names = mapped_dataset[mapped_dataset['state_code'] == -2]['state_name']

    return unmatched_names,mapped_dataset