import sqlite3
import streamlit as st
import pandas as pd
from collections import defaultdict
import base64
import multiprocessing



def load_file():
    data = pd.read_csv('data.csv')
    return data

def process_file(file):
    """
    Processes a file and returns a DataFrame containing selected columns.

    Parameters:
        file (File): The file to be processed.

    Returns:
        DataFrame: A pandas DataFrame containing the selected columns from the file.

    Raises:
        ValueError: If the file format is invalid or none of the specified columns are present.
    """
    try:
        if file.type == 'text/csv':
            df = pd.read_csv(file)
        elif file.type == 'application/vnd.ms-excel':
            df = pd.read_excel(file)
        else:
            raise ValueError("Invalid file format. Only CSV and Excel files are supported.")

        # Get the present columns based on the intersection of specified columns and available columns
        specified_columns = ["state_name", "district_name", "sub_district_name", "block_name", "gp_name", "village_name"]
        present_columns = list(set(specified_columns).intersection(df.columns))
        
        if not present_columns:
            raise ValueError("None of the specified columns are present in the file.")
        
        # Select only the present columns
        st.write("Dataset Information:")
        st.write(df.head())
        df = df[present_columns]
        
        return df
    
    except Exception as e:
        st.error("An error occurred during file processing: " + str(e))
        return None

# Streamlit app

def get_state_mappings():
    """
    This function retrieves state names, codes, and variants from an SQLite database and returns a dictionary
    containing the state mappings. No parameters are required. The keys of the dictionary are the state names and
    variants in lowercase, and the values are the corresponding state codes. Returns a dictionary.
    """
    with sqlite3.connect('lgd_database.db') as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT entityName, entityLGDCode, entityNameVariants FROM states")
        data = cursor.fetchall()

    mapping_dict = {}
    for state_name, state_code, state_variants in data:
        mapping_dict[state_name.lower()] = state_code
        if state_variants:
            for variant in state_variants.split(','):
                mapping_dict[variant.strip().lower()] = state_code

    return mapping_dict

def create_mapped_dataset(dataset, mapping):

    dataset['state_name'] = dataset['state_name'].str.strip()
    dataset['state_code'] = dataset['state_name'].str.lower().map(mapping)
    dataset.loc[dataset['state_code'].isnull(), 'state_code'] = -2
    return dataset 



def create_selectbox_widget(name, values):
    """
    Creates a select box widget using the Streamlit library. The select box widget allows the user to choose a value from a list of values.

    :param name: The name of the select box widget.
    :type name: str
    :param values: A list of values to be displayed in the select box.
    :type values: list
    :return: The selected value from the select box.
    :rtype: any
    """
    return st.selectbox(f'{name}', values, key=name)


def query_state_data():
    """
    Connects to an SQLite database and retrieves all the entity names and their variants from the 'states' table.

    :return: A list of tuples containing the entity names and their variants.
    """
    conn = sqlite3.connect('lgd_database.db')
    cursor = conn.cursor()
    cursor.execute("SELECT entityName, entityNameVariants FROM states")
    state_data = cursor.fetchall()
    conn.close()
    return state_data

def update_state_variants(state_name, name_variant, state_data):
    """
    Updates the variants of a state name in the state_data dictionary.

    Parameters:
        state_name (str): The name of the state to update the variants for.
        name_variant (str): The new name variant to add.
        state_data (dict): A dictionary containing state names and their variants.

    Returns:
        tuple or None: A tuple containing the updated state name and its variants if the state name is found and updated in the dictionary. Otherwise, returns None.
    """
    for state_name_db, entityNameVariants in state_data:
        if state_name.lower() == state_name_db.lower():
            new_variants = f"{entityNameVariants}, {name_variant}" if entityNameVariants else name_variant
            conn = sqlite3.connect('lgd_database.db')
            cursor = conn.cursor()
            cursor.execute("UPDATE states SET entityNameVariants = ? WHERE entityName = ?", (new_variants, state_name_db))
            conn.commit()
            conn.close()
            return state_name_db, new_variants
    return None, None

def process_unmatched_names(unmatched_names, state_mapping):
    """
    Process unmatched names and update state data.

    Parameters:
    - unmatched_names (list): A list of unmatched names.
    - state_mapping (dict): A dictionary mapping state names to their data.

    Returns:
    None
    """
    state_data = query_state_data()
    for unmatched_name_index, unmatched_name in enumerate(unmatched_names):
        st.write(f'Unmatched Name: {unmatched_name}')
        state_name = create_selectbox_widget(f'Enter state name {unmatched_name_index}:', list(state_mapping.keys()))
        state_exists = state_name.lower() in state_mapping.keys()

        if state_name and not state_exists:
            st.error('State name not found in the table. Please enter a valid state name.')

        name_variant = st.text_input(f'Enter name variant {unmatched_name_index}:')

        if state_name and name_variant and state_exists:
            state_name_db, new_variants = update_state_variants(state_name, name_variant, state_data)
            if state_name_db and new_variants:
                st.success(f'State Name: {state_name_db} Variations: {new_variants} Updated Successfully.')

        st.write('---')


def fetch_district_mapping():
    """
    Fetch the district mapping from the SQLite database.

    Returns:
    - A list of tuples containing the district entity name, LGD code, name variants, and parent entity.
    """
    # Connect to the SQLite database
    conn = sqlite3.connect('lgd_database.db')
    cursor = conn.cursor()

    # Retrieve district data from the 'districts' table
    cursor.execute("SELECT entityName, entityLGDCode, entityNameVariants, entityParent FROM district")
    data = cursor.fetchall()

    # Close the database connection
    conn.close()

    return data

def populate_entity_mapping(data,column_name,parent_column_name):
    """
    Populates a entity mapping dictionary using data from a database and a local file.

    Returns:
        A defaultdict containing the mapping of entity names to their respective codes.
    """
    # Load unique entity data
    dataset = pd.read_csv('data.csv')
    unique_rows = dataset.drop_duplicates(subset=[column_name])
    unique_rows_lower = unique_rows.apply(lambda x: (x[column_name].strip().lower(), x[parent_column_name]), axis=1).tolist()

    entity_mapping = {}
    for entity_name, entity_code, entity_variants, parent_code in data:
        for row in unique_rows_lower:
            entity_name_lower = row[0]
            state_code = row[1]
            if int(parent_code) == int(state_code):
                if entity_name_lower.strip() == entity_name.strip().lower():
                    entity_mapping[entity_name_lower] = entity_code
                    #print(entity_name_lower)
                else:
                    if entity_variants:
                        for variant in entity_variants.split(','):
                            if variant.strip().lower() == entity_name_lower.strip():
                                entity_mapping[variant.strip().lower()] = entity_code
                                print(variant.strip().lower())

    return entity_mapping






def process_district_name(district_name, mapping):
    """
    Process a district name by stripping, converting to lowercase, and mapping to a code.
    """
    district_name = district_name.strip().lower()
    return district_name, mapping.get(district_name, -2)

def create_district_mapped_dataset(dataset, mapping):
    """
    Create a mapped dataset by associating state codes with district names in the dataset.
    """
    pool = multiprocessing.Pool()
    results = pool.starmap(process_district_name, zip(dataset['district_name'], [mapping]*len(dataset)))
    dataset['district_name'], dataset['district_code'] = zip(*results)
    return dataset


import sqlite3

def update_variations(unmatched_names, mapping, entity_table_name, chunk_size=1):
    """
    Updates the variations of unmatched names in the given mapping dictionary for a specific entity table.

    Parameters:
    - unmatched_names (list): A list of unmatched names to update the variations for.
    - mapping (dict): A dictionary mapping entity names to their variations.
    - entity_table_name (str): The name of the entity table to update the variations in.
    - chunk_size (int): The size of each processing chunk.

    Returns:
    - str: The message "Done" indicating that the variations have been updated successfully.
    """
    try:
        conn = sqlite3.connect('lgd_database.db')
        cursor = conn.cursor()

        num_unmatched = len(unmatched_names)
        num_chunks = (num_unmatched + chunk_size - 1) // chunk_size

        chunk_index = 0  # Initialize chunk index

        while chunk_index < num_chunks:
            start_idx = chunk_index * chunk_size
            end_idx = min((chunk_index + 1) * chunk_size, num_unmatched)
            current_chunk = unmatched_names[start_idx:end_idx]

            for index, unmatched_name in enumerate(current_chunk):
                entity_name = create_selectbox_widget(f'Select {entity_table_name} name {start_idx + index + 1}:', list(mapping))
                if not entity_name:
                    continue

                entity_exists = entity_name in mapping
                if not entity_exists:
                    st.error(f'{entity_table_name} name not found in the table. Please enter a valid {entity_table_name} name.')
                    continue

                name_variant = st.text_input(f'Select an appropriate value for the following variant {unmatched_name}:')
                if not name_variant:
                    continue

                cursor.execute(f"SELECT entityName, entityNameVariants, entityLGDCode FROM {entity_table_name}")
                entity_data = cursor.fetchall()

                for entity_name_db, entityNameVariants, entity_LGD_Code in entity_data:
                    if entity_name.lower() == entity_name_db.lower():
                        new_variants = f"{entityNameVariants.strip()}, {name_variant.strip()}" if entityNameVariants else name_variant
                        cursor.execute(f"UPDATE {entity_table_name} SET entityNameVariants = ? WHERE entityLGDCode = ?", (new_variants.strip(), int(entity_LGD_Code)))
                        st.success(f'{entity_name_db} Variation Updated Successfully.')
                        break

                conn.commit()
                st.write('---')

            chunk_index += 1  # Increment chunk index

            if chunk_index < num_chunks:
                unique_button_key = f"load_next_button_{chunk_index}"
                load_next_button = st.button("Load Next Chunk", key=unique_button_key)
                if not load_next_button:
                    break  # Break the loop if button is not clicked

        conn.close()

    except Exception as e:
        st.error(f"An error occurred: {str(e)}")
    return "Done"









def update_variationsold(unmatched_names, mapping, entity_table_name):
    """
    Updates the variations of unmatched names in the given mapping dictionary for a specific entity table.

    Parameters:
    - unmatched_names (list): A list of unmatched names to update the variations for.
    - mapping (dict): A dictionary mapping entity names to their variations.
    - entity_table_name (str): The name of the entity table to update the variations in.

    Returns:
    - str: The message "Done" indicating that the variations have been updated successfully.
    """
    try:
        conn = sqlite3.connect('lgd_database.db')
        cursor = conn.cursor()

        for index, unmatched_name in enumerate(unmatched_names):
            entity_name = create_selectbox_widget(f'Select {entity_table_name} name {index+1}:', list(mapping))
            if not entity_name:
                continue

            entity_exists = entity_name in mapping
            if not entity_exists:
                st.error(f'{entity_table_name} name not found in the table. Please enter a valid {entity_table_name} name.')
                continue

            name_variant = st.text_input(f'Select an appropriate value for the following variant {unmatched_name}:')
            if not name_variant:
                continue

            cursor.execute(f"SELECT entityName, entityNameVariants, entityLGDCode FROM {entity_table_name}")
            entity_data = cursor.fetchall()

            for entity_name_db, entityNameVariants, entity_LGD_Code in entity_data:
                if entity_name.lower() == entity_name_db.lower():
                    new_variants = f"{entityNameVariants.strip()}, {name_variant.strip()}" if entityNameVariants else name_variant
                    cursor.execute(f"UPDATE {entity_table_name} SET entityNameVariants = ? WHERE entityLGDCode = ?", (new_variants.strip(), int(entity_LGD_Code)))
                    st.success(f'{entity_name_db} Variation Updated Successfully.')
                    break

            conn.commit()
            st.write('---')

        conn.close()

    except Exception as e:
        st.error(f"An error occurred: {str(e)}")
    return "Done"


def update_variationso(unmatched_names, mapping, entity_table_name):
    """
    Updates the variations of a given entity in the database.

    Parameters:
    - unmatched_names (list): A list of unmatched names.
    - mapping (dict): A dictionary mapping entity names to their corresponding values.
    - entity_table_name (str): The name of the entity table.

    Returns:
    - str: The status message indicating the success of the function.
    """
    try:
        entity_name = create_selectbox_widget(f'Select {entity_table_name} name :', list(mapping))
        if not entity_name:
            return

        entity_exists = entity_name in mapping
        if not entity_exists:
            st.error(f'{entity_table_name} name not found in the table. Please enter a valid {entity_table_name} name.')
            return

        name_variant = st.text_input(f'Enter name variant {unmatched_names[0]}:')
        if not name_variant:
            return

        conn = sqlite3.connect('lgd_database.db')
        cursor = conn.cursor()

        cursor.execute(f"SELECT entityName, entityNameVariants, entityLGDCode FROM {entity_table_name}")
        entity_data = cursor.fetchall()

        for entity_name_db, entityNameVariants, entity_LGD_Code in entity_data:
            if entity_name.lower() == entity_name_db.lower():
                new_variants = f"{entityNameVariants.strip()}, {name_variant.strip()}" if entityNameVariants else name_variant
                cursor.execute(f"UPDATE {entity_table_name} SET entityNameVariants = ? WHERE entityLGDCode = ?", (new_variants.strip(), int(entity_LGD_Code)))
                st.success(f'{entity_name_db} Variation Updated Successfully.')
                break

        conn.commit()
        conn.close()
        st.write('---')

    except Exception as e:
        st.error(f"An error occurred: {str(e)}")
    return "Done"


def update_variations_without_parent(unmatched_names, mapping, entity_table_name):

    try:

        entity_name = create_selectbox_widget(f'Select {entity_table_name} name :', list(mapping))

        entity_exists = entity_name in mapping

       
        if entity_name and not entity_exists:

            st.error(f'{entity_table_name} name not found in the table. Please enter a valid {entity_table_name} name.')

 
        name_variant = st.text_input(f'Enter name variant {unmatched_names[0]}:')

        if entity_name and name_variant and entity_exists:

            conn = sqlite3.connect('lgd_database.db')

            cursor = conn.cursor()

            cursor.execute(f"SELECT entityName, entityNameVariants, entityLGDCode FROM {entity_table_name}")

            entity_data = cursor.fetchall()

            for entity_name_db, entityNameVariants, entity_LGD_Code in entity_data:

                if entity_name.lower() == entity_name_db.lower():

                    new_variants = f"{entityNameVariants.strip()}, {name_variant.strip()}" if entityNameVariants else name_variant

                    cursor.execute(f"UPDATE {entity_table_name} SET entityNameVariants = ? WHERE entityLGDCode = ?", (new_variants.strip(), int(entity_LGD_Code)))

                    st.success(f'{entity_name_db} Variation Updated Successfully.')

                   

 

            conn.commit()

            conn.close()

            st.write('---')

 

    except Exception as e:

        st.error(f"An error occurred: {str(e)}")

    return "Done"




import concurrent.futures



def generate_download_link(mapped_dataset):

    csv_file = mapped_dataset.to_csv(index=False)
    b64 = base64.b64encode(csv_file.encode()).decode()
    href = f'<a href="data:file/csv;base64,{b64}" download="mapped_dataset.csv">Download</a>'
    st.success('Download Mapped Dataset')
    st.markdown(href, unsafe_allow_html=True) 


def fetch_block_mapping():
    """
    Fetch the block mapping from the SQLite database.

    Returns:
    - A list of tuples containing the block entity name, LGD code, name variants, and parent entity.
    """
    # Connect to the SQLite database
    conn = sqlite3.connect('lgd_database.db')
    cursor = conn.cursor()

    # Retrieve block data from the 'blocks' table
    cursor.execute("SELECT entityName, entityLGDCode, entityNameVariants, entityParent FROM block")
    data = cursor.fetchall()

    # Close the database connection
    conn.close()

    return data

def populate_block_mapping():

    state_dataset = pd.read_csv('data.csv')
    
    unique_rows = state_dataset.drop_duplicates(subset=['block_name'])
    unique_rows_lower = unique_rows.apply(lambda x: (x['block_name'].strip().lower(), x['district_code']), axis=1).tolist()

    district_mapping = {}
    edname = "Not Available"

    for district_name, district_code, district_variants, parent_code in data:
        for row in unique_rows_lower:
            district_name_lower = row[0]
            state_code = row[1]
            if district_name_lower == district_name.lower():
                if int(parent_code) == int(state_code):
                    district_mapping[district_name.lower()] = district_code
                    if district_variants:
                        for variant in district_variants.split(','):
                            district_mapping[variant.strip().lower()] = district_code
    

    for district_name, district_code, district_variants, parent_code in data:
        if edname.lower() == district_name.lower():
            if int(parent_code) == int(0):
                district_mapping[district_name.lower()] = district_code
                if district_variants:
                    for variant in district_variants.split(','):
                        district_mapping[variant.strip().lower()] = district_code
    

    return district_mapping



def create_block_mapped_dataset(dataset, mapping):
    """
    Create a mapped dataset by associating block codes with block names in the dataset.
    """
    dataset['block_name'] = dataset['block_name'].str.strip()
    dataset['block_code'] = dataset['block_name'].str.lower().map(mapping)
    dataset.loc[dataset['block_code'].isnull(), 'block_code'] = -2
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

def fetch_village_mapping():
    """
    Fetch the gp mapping from the SQLite database.

    Returns:
    - A list of tuples containing the gp entity name, LGD code, name variants, and parent entity.
    """
    # Connect to the SQLite database
    conn = sqlite3.connect('lgd_database.db')
    cursor = conn.cursor()

    # Retrieve gp data from the 'gps' table
    cursor.execute("SELECT villageNameEnglish, villageCode, entityNameVariants FROM villages")
    data = cursor.fetchall()

    # Close the database connection
    conn.close()

    return data

def create_entity_name_list():
    data = fetch_gp_mapping()
    entity_name_list = [entity_name for entity_name, _, _, _ in data]
    return entity_name_list
def populate_gp_mapping():
    """
    Populates a gp mapping dictionary using data from a database and a local file.

    Returns:
        A dictionary containing the mapping of gp names to their respective codes.
    """
    state_dataset = pd.read_csv('data.csv')
    data = fetch_gp_mapping()
    unique_rows = state_dataset.drop_duplicates(subset=['gp_name'])
    unique_rows_lower = unique_rows.apply(lambda x: (str(x['gp_name']).strip().lower(), x['block_code']), axis=1).tolist()

    entity_mapping = {}

    # Populate mapping for entity name and variants
    for entity_name, entity_code, entity_variants, parent_code in data:
        for row in unique_rows_lower:
            entity_name_lower = row[0]
            state_code = row[1]
            if entity_name_lower == entity_name.lower() and int(parent_code) == int(state_code):
                entity_mapping[entity_name_lower] = entity_code
                if entity_variants:
                    for variant in entity_variants.split(','):
                        entity_mapping[variant.strip().lower()] = entity_code

    # Populate mapping for special case entity name
    edname = "Not Available"
    for entity_name, entity_code, entity_variants, parent_code in data:
        if edname.lower() == entity_name.lower() and str(parent_code) == str(0):
            entity_mapping[entity_name.lower()] = entity_code
            if entity_variants:
                for variant in entity_variants.split(','):
                    entity_mapping[variant.strip().lower()] = entity_code

    return entity_mapping


def populate_village_mapping():
    """
    Populates a gp mapping dictionary using data from a database and a local file.

    Returns:
        A defaultdict containing the mapping of gp names to their respective codes.
    """
    state_dataset = pd.read_csv('data.csv')
    data = fetch_village_mapping()
    unique_rows = state_dataset.drop_duplicates(subset=['village_name'])
    unique_rows_lower = unique_rows.apply(lambda x: (x['village_name'].strip().lower(), x['panchayat_name']), axis=1).tolist()

    district_mapping = {}

    for district_name, district_code, district_variants, parent_code in data:
        for row in unique_rows_lower:
            district_name_lower = row[0]
            state_code = row[1]
            if district_name_lower == district_name.lower():
                if int(parent_code) == int(state_code):
                    district_mapping[district_name_lower] = district_code
                    if district_variants:
                        for variant in district_variants.split(','):
                            district_mapping[variant.strip().lower()] = district_code

    return district_mapping



def create_gp_mapped_dataset(dataset, mapping):
    """
    Create a mapped dataset by associating gp codes with gp names in the dataset.
    """
    dataset['gp_name'] = dataset['gp_name'].str.strip()
    dataset['gp_code'] = dataset['gp_name'].str.lower().map(mapping)
    dataset.loc[dataset['gp_code'].isnull(), 'gp_code'] = -2
    return dataset

def create_village_mapped_dataset(dataset, mapping):
    """
    Create a mapped dataset by associating gp codes with gp names in the dataset.
    """
    dataset['village_name'] = dataset['village_name'].str.strip()
    dataset['village_code'] = dataset['village_name'].str.lower().map(mapping)
    dataset.loc[dataset['village_code'].isnull(), 'village_code'] = -2
    return dataset

def fetch_sub_district_mapping():
    """
    Fetch the Sub-District mapping from the SQLite database.

    Returns:
    - A list of tuples containing the Sub-District entity name, LGD code, name variants, and parent entity.
    """
    # Connect to the SQLite database
    conn = sqlite3.connect('lgd_database.db')
    cursor = conn.cursor()

    # Retrieve Sub-District data from the 'Sub-Districts' table
    cursor.execute("SELECT entityName, entityLGDCode, entityNameVariants, entityParent FROM sub_district")
    data = cursor.fetchall()

    # Close the database connection
    conn.close()
    return data

def populate_sub_district_mapping():
    """
    Populates a sub_district mapping dictionary using data from a database and a local file.

    Returns:
        A defaultdict containing the mapping of sub_district names to their respective codes.
    """
    state_dataset = pd.read_csv('data.csv')
    data = fetch_sub_district_mapping()
    unique_rows = state_dataset.drop_duplicates(subset=['sub_district_name'])
    unique_rows_lower = unique_rows.apply(lambda x: (x['sub_district_name'].strip().lower(), x['district_code']), axis=1).tolist()
    district_mapping = {}
    for district_name, district_code, district_variants, parent_code in data:
        for row in unique_rows_lower:
            district_name_lower = row[0]
            state_code = row[1]
            if district_name_lower == district_name.lower():
                if int(parent_code) == int(state_code):
                    district_mapping[district_name_lower] = district_code
                    if district_variants:
                        for variant in district_variants.split(','):
                            district_mapping[variant.strip().lower()] = district_code

    return district_mapping



def create_sub_district_mapped_dataset(dataset, mapping):
    """
    Create a mapped dataset by associating Sub-District codes with Sub-District names in the dataset.
    """
    dataset['sub_district_name'] = dataset['sub_district_name'].str.strip()
    dataset['sub_district_code'] = dataset['sub_district_name'].str.lower().map(mapping)
    dataset.loc[dataset['sub_district_code'].isnull(), 'sub_district_code'] = -2
    return dataset