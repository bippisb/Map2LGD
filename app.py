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


def home_page():

    # Add an attractive header
    st.title('CodeYatra')
    #st.image('mandala.jpg')  # Replace 'your_logo.png' with the path to your logo image
    st.sidebar.success("Select a page")
    # Write a brief and engaging introduction
    st.write(
        "Welcome to the CodeYatra LGD Mapping App! 🌟 This app makes mapping a breeze, allowing "
        "you to explore states, districts, sub-districts, blocks, gram panchayats, and villages LGD Mapping with ease. "
        "Whether you're a researcher 👩‍🔬, a data analyst 📊, or simply curious about India's geography, this app is "
        "the perfect resource for you. Say goodbye to tedious manual searches and say hello to accurate and "
        "up-to-date mapping at your fingertips. Let's embark on an exciting journey of exploration and "
        "discovery with the CodeYatra LGD Code Mapping App! 🗺️🚀"
    )


    st.warning("⚠️ **Important Notice:** ")
    st.write(" To ensure smooth operation of the application, please update the column names as follows:")
    st.write("- State: Change the state column name to 'state_name'")
    st.write("- District: Change the district column name to 'district_name'")
    st.write("- Sub District: Change the sub district column name to 'sub_district_name'")
    st.write("- Block: Change the block column name to 'block_name'")
    st.write("- Gram Panchayat (GP): Change the gp column name to 'gp_name'")
    st.write("- Village: Change the village column name to 'village_name'")



    # Add visually appealing images or illustrations to showcase the app's features
    #st.image('your_app_features.png', use_column_width=True)  # Replace 'your_app_features.png' with the path to your app features image

    st.subheader('Start Mapping Now')
    st.write('Ready to explore and map LGD codes? Click the button below to get started.')
    

    if st.button('Start Mapping', key='sub_mapping_button'):
        #redirect_to_subset_dataset_page()
        redirect_to_state_mapping_page()


def redirect_to_update_dataset_page():
    # Modify the URL parameters to navigate to the state mapping page
    state_mapping_url = st.experimental_set_query_params(page='update')
    page_route()
    st.experimental_rerun()
def redirect_to_subset_dataset_page():
    # Modify the URL parameters to navigate to the state mapping page
    state_mapping_url = st.experimental_set_query_params(page='subset')
    page_route()
    st.experimental_rerun()
def redirect_to_state_mapping_page():
    # Modify the URL parameters to navigate to the state mapping page
    state_mapping_url = st.experimental_set_query_params(page='state')
    page_route()
    st.experimental_rerun()

def redirect_to_district_page():
    # Modify the URL parameters to navigate to the district page
    district_url = st.experimental_set_query_params(page='district')
    page_route()
    st.experimental_rerun()
def redirect_to_block_page():
    # Modify the URL parameters to navigate to the block page
    block_url = st.experimental_set_query_params(page='block')
    page_route()
    st.experimental_rerun()

def redirect_to_panchayat_page():
    # Modify the URL parameters to navigate to the block page
    panchayat_url = st.experimental_set_query_params(page='panchayat')
    page_route()
    st.experimental_rerun()

def redirect_to_village_page():
    # Modify the URL parameters to navigate to the block page
    panchayat_url = st.experimental_set_query_params(page='village')
    page_route()
    st.experimental_rerun()
def redirect_to_sub_district_page():
    # Modify the URL parameters to navigate to the district page
    subdistrict_url = st.experimental_set_query_params(page='subdistrict')
    page_route()
    st.experimental_rerun()


def page_route():
    query_params = st.experimental_get_query_params()
    if "page" in query_params and query_params["page"][0] == "state":
        state_mapping_page()
    elif "page" in query_params and query_params["page"][0] == "subset":
        subset_page()
    elif "page" in query_params and query_params["page"][0] == "update":
        update_data()
    elif "page" in query_params and query_params["page"][0] == "district":
        district_page()
    elif "page" in query_params and query_params["page"][0] == "block":
        block_page()
    elif "page" in query_params and query_params["page"][0] == "panchayat":
        gp_page()
    elif "page" in query_params and query_params["page"][0] == "subdistrict":
        sub_district_page()
    elif "page" in query_params and query_params["page"][0] == "village":
        village_page()
    elif "page" in query_params and query_params["page"][0] == "insertRecord":
        pass
        #insert_record()
    else:
        home_page()

# Main app logic
def main():
    st.set_page_config(
        page_title="CodeYatra",
        page_icon="🌟",
        layout="centered",
        initial_sidebar_state="expanded",
    )
    page_route()

def update_data():
     st.title("Update the Corpus of LGD codes")
     if st.button('Update Corpus', key='corpus_button'):   
        update_all_data()


#sub set
def subset_page():
    st.title("Select Specific Columns from CSV/Excel File")
    
    # File uploader
    file = st.file_uploader("Upload a CSV or Excel file", type=["csv", "xlsx"])
    
    if file is not None:
        # Process the file
        
        df = process_file(file)
        if df is not None:
            # Display the processed DataFrame
            st.write('Subsetted Columns')
            st.write(df.head())
            st.info("Important: To perform LGD mapping accurately, please download the subsetted file. It contains the selected columns required for mapping. Without the subsetted file, LGD mapping cannot be done effectively.")
            st.warning("⚠️ **Important Notice:** Please upload the subsetted file on the next page for LGD mapping. It contains the required columns for accurate mapping.")

            # Download button
            csv = df.to_csv(index=False)
            b64 = base64.b64encode(csv.encode()).decode()
            href = f'<a href="data:file/csv;base64,{b64}" download="processed_data.csv">Download CSV</a>'
            st.markdown(href, unsafe_allow_html=True)

        if st.button('Start Mapping', key='mapping_button'):
                    redirect_to_state_mapping_page()
# State Mapping Code
def state_mapping_page(dataset_selected=False):
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


    if not dataset_selected:
        dataset_file = st.file_uploader('Upload dataset', type=['csv', 'xlsx'])
        if dataset_file is None:
            st.warning("Please upload a dataset file.")
            return
    else:
        dataset_file = st.session_state['dataset_file']

    dataset = pd.read_csv(dataset_file) if dataset_file.name.endswith('.csv') else pd.read_excel(dataset_file)
    if 'state_name' not in dataset.columns:
        st.error("Error: The dataset does not contain the 'state_name' column.")
        return
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
                return
            redirect_to_district_page()
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
                    return
                redirect_to_district_page()

def district_page():
    """
    This function is responsible for displaying the District LGD mapping page. It fetches the district mapping dataset,
    maps the dataset, and downloads the mapped dataset. If there are any unmatched district names, it prompts the user to
    provide the district name variations. Once the district name variations are provided, it updates the entityNameVariants
    column in the SQLite table and generates a new mapped dataset for download. If the 'Start Sub-District/Block Mapping'
    button is clicked, it does nothing. 
    """
    st.title('District LGD Mapping')
    st.subheader("Before District LGD Mapping")
    state_dataset = load_file()
    st.write(state_dataset.head())
    # Apply district mapping and create a new dataset
    data  = fetch_district_mapping()
    district_mapping = populate_entity_mapping(data,'district_name','state_code')
    mapped_dataset = create_district_mapped_dataset(state_dataset, district_mapping)
    # Check if there are any unmatched names
    unmatched_names = mapped_dataset[mapped_dataset['district_code'] == -2]['district_name']

    if unmatched_names.empty:
        # Display a message if there are no unmatched names
        st.success('No Unmatched district Names')
        mapped_dataset.to_csv("data.csv",index=False)
        # Create a CSV file in memory
        st.subheader("After District LGD Mapping")
        st.write(state_dataset.head())
        generate_download_link(mapped_dataset)
        condition = True 
        if 'sub_district_name' not in mapped_dataset.columns:
            condition = False

        if st.button('Start Block Mapping', key='block_mapping_button'):
            if 'block_name' not in mapped_dataset.columns:
                    st.error("Error: The dataset does not contain the 'block_name' column.")
                    return
            redirect_to_block_page()

        if condition:    
            if st.button('Start Sub-District Mapping', key='sub-district_mapping_button'):
                if 'sub_district_name' not in mapped_dataset.columns:
                        st.error("Error: The dataset does not contain the 'sub_district_name' column.")
                        return
                redirect_to_sub_district_page()
    else:
            # Display the dataset with unmatched names
            st.subheader('Unmatched District Names')
            st.write(f'Unmatched District Count: '+str(len(unmatched_names.unique())))
            st.write(unmatched_names.unique())
            # Display the note
            note = "Please provide the district name variations separated by commas or a single district name."
            st.info(note)
            # Accept comma-separated values or single value only
            st.subheader('Update District Name Variations')
            #district_mapping = populate_entity_mapping(data,'district_name','state_code')
            #mapped_dataset = create_district_mapped_dataset(state_dataset, district_mapping)
            # Check if there are any unmatched names
            #unmatched_names = mapped_dataset[mapped_dataset['district_code'] == -2]['district_name']
            district_names = [row[0] for row in data]
            entity_table_name = "district"
            update_variations(unmatched_names.unique(), district_names, entity_table_name)
            #unmatched_names = mapped_dataset[mapped_dataset['district_code'] == -2]['district_name']
            if unmatched_names.empty:
                st.success('District Name Variations Updated Successfully.')
                # Create a CSV file in memory
                mapped_dataset.to_csv("data.csv",index=False)
                st.subheader("After District LGD Mapping")
                st.write(mapped_dataset.head())
                generate_download_link(mapped_dataset)

                if 'block_name' in mapped_dataset.columns:
                    if st.button('Start Block Mapping', key='block_mapping_button'):
                        if 'block_name' not in mapped_dataset.columns:
                            st.error("Error: The dataset does not contain the 'block_name' column.")
                            return
                        redirect_to_block_page()

                if 'sub_district_name' in mapped_dataset.columns:
                    if st.button('Start Sub-District Mapping', key='sub-district_mapping_button'):
                        if 'sub_district_name' not in mapped_dataset.columns:
                            st.error("Error: The dataset does not contain the 'sub_district_name' column.")
                            return
                        redirect_to_sub_district_page()

# Block mapping
def block_page():
    """
    This function is responsible for displaying the block LGD mapping page. It fetches the block mapping dataset,
    maps the dataset, and downloads the mapped dataset. If there are any unmatched block names, it prompts the user to
    provide the block name variations. Once the block name variations are provided, it updates the entityNameVariants
    column in the SQLite table and generates a new mapped dataset for download. If the 'Start Sub-block/Block Mapping'
    button is clicked, it does nothing. 
    """
    st.title('Block LGD Mapping')
    st.subheader("Before Block LGD Mapping")
    block_dataset = pd.read_csv('data.csv')
    st.write(block_dataset.head())
    data = fetch_block_mapping()
    # Apply block mapping and create a new dataset
    block_mapping = populate_entity_mapping(data,'block_name','district_code')
    mapped_dataset = create_block_mapped_dataset(block_dataset, block_mapping)
    # Check if there are any unmatched names
    unmatched_names = mapped_dataset[mapped_dataset['block_code'] == -2]['block_name']

    if unmatched_names.empty:
        # Display a message if there are no unmatched names
        st.success('No Unmatched Block Names')

        # Create a CSV file in memory
        
        st.subheader("After Block LGD Mapping")
        mapped_dataset.to_csv("data.csv",index=False)
        st.write(mapped_dataset.head())
        generate_download_link(mapped_dataset)
        if st.button('Start Panchayat Mapping', key='Panchayat_mapping_button'):
            if 'gp_name' not in mapped_dataset.columns:
                        st.error("Error: The dataset does not contain the 'gp_name' column.")
                        return
            redirect_to_panchayat_page()

    else:
        # Display the dataset with unmatched names
        st.subheader('Unmatched block Names')
        st.write(f'Unmatched block Count: '+str(len(unmatched_names.unique())))
        st.write(unmatched_names.unique())

        # Display the note
        note = "Please provide the block name variations separated by commas or a single block name."
        st.warning(note)

        # Accept comma-separated values or single value only
        st.subheader('Update Block Name Variations')

        entity_table_name = "block"
        block_mapping = populate_entity_mapping(data,'block_name','district_code')
        mapped_dataset = create_block_mapped_dataset(block_dataset, block_mapping)
        block_names = [row[0] for row in data]
        unmatched_names = mapped_dataset[mapped_dataset['block_code'] == -2]['block_name']
        unmatched_names = unmatched_names.unique()
        update_variations(unmatched_names, block_names, entity_table_name)
        # Display a success message
        unmatched_names = mapped_dataset[mapped_dataset['block_code'] == -2]['block_name']
        if unmatched_names.empty:
            st.success('Block Name Variations Updated Successfully.')
            # Create a CSV file in memory
            st.subheader("After block LGD Mapping")
            mapped_dataset.to_csv("data.csv",index=False)
            st.write(mapped_dataset.head())
            generate_download_link(mapped_dataset)

            if st.button('Start Panchayat Mapping', key='Panchayat_mapping_button'):
                if 'gp_name' not in mapped_dataset.columns:
                            st.error("Error: The dataset does not contain the 'gp_name' column.")
                            return
                redirect_to_panchayat_page()

#GP Mapping 



def gp_page():
    """
    This function is responsible for displaying the gp LGD mapping page. It fetches the gp mapping dataset,
    maps the dataset, and downloads the mapped dataset. If there are any unmatched gp names, it prompts the user to
    provide the gp name variations. Once the gp name variations are provided, it updates the entityNameVariants
    column in the SQLite table and generates a new mapped dataset for download. If the 'Start Sub-gp/gp Mapping'
    button is clicked, it does nothing. 
    """
    st.title('GP LGD Mapping')
    st.subheader("Before GP LGD Mapping")
    gp_dataset = pd.read_csv('data.csv')
    data= fetch_gp_mapping()
    st.write(gp_dataset.head())
    unmatched_names = None
    # Apply gp mapping and create a new dataset
    
    #gp_mapping = populate_gp_mapping()
    gp_mapping = populate_entity_mapping(data,'gp_name','block_code')
    mapped_dataset = create_gp_mapped_dataset(gp_dataset, gp_mapping)

    # Check if there are any unmatched names
    unmatched_names = mapped_dataset[mapped_dataset['gp_code'] == -2]['gp_name']
    if unmatched_names.empty:
        # Display a message if there are no unmatched names
        st.success('No Unmatched GP Names')

        # Create a CSV file in memory
        csv_file = mapped_dataset.to_csv(index=False)
        st.subheader("After GP LGD Mapping")
        st.write(mapped_dataset.head())

        generate_download_link(mapped_dataset)

        if st.button('Start Village Mapping', key='village_mapping_button'):
            if 'village_name' not in mapped_dataset.columns:
                        st.error("Error: The dataset does not contain the 'village_name' column.")
                        return
            redirect_to_panchayat_page()

    else:
        # Display the dataset with unmatched names
        st.subheader('Unmatched GP Names')
        st.write(f'Unmatched GP Count: '+str(len(unmatched_names.unique())))
        st.write(unmatched_names.unique())
        
        # Display the note
        note = "Please provide the GP name variations separated by commas or a single GP name."
        st.info(note)

        # Accept comma-separated values or single value only
        st.subheader('Update GP Name Variations')
        gp_mapping = populate_gp_mapping()
        mapped_dataset = create_gp_mapped_dataset(gp_dataset, gp_mapping)
        entity_name = create_entity_name_list()
        # Check if there are any unmatched names
        unmatched_names = mapped_dataset[mapped_dataset['gp_code'] == -2]['gp_name']
        update_variations(unmatched_names.unique(), entity_name, "gp")
        unmatched_names = mapped_dataset[mapped_dataset['gp_code'] == -2]['gp_name']
        if unmatched_names.empty:
            st.success('GP Name Variations Updated Successfully.')
            # Create a CSV file in memory
            mapped_dataset.to_csv("data.csv",index=False)
            st.subheader("After GP LGD Mapping")
            st.write(mapped_dataset.head())
            # Generate download link for the CSV file
            generate_download_link(mapped_dataset)
            if st.button('Start Village Mapping', key='village_mapping_button'):
                if 'village_name' not in mapped_dataset.columns:
                            st.error("Error: The dataset does not contain the 'village_name' column.")
                            return
                redirect_to_panchayat_page()


#village page

def village_page():
    """
    This function is responsible for displaying the village LGD mapping page. It fetches the village mapping dataset,
    maps the dataset, and downloads the mapped dataset. If there are any unmatched village names, it prompts the user to
    provide the village name variations. Once the village name variations are provided, it updates the entityNameVariants
    column in the SQLite table and generates a new mapped dataset for download. If the 'Start Sub-village/village Mapping'
    button is clicked, it does nothing. 
    """
    st.title('village LGD Mapping')
    st.subheader("Before village LGD Mapping")
    village_dataset = pd.read_csv('data.csv')
    st.write(village_dataset.head())
    # Apply village mapping and create a new dataset
    village_mapping = populate_village_mapping()

    mapped_dataset = create_village_mapped_dataset(village_dataset, village_mapping)

    # Check if there are any unmatched names
    unmatched_names = mapped_dataset[mapped_dataset['village_code'] == -2]['village_name']

    if unmatched_names.empty:
        # Display a message if there are no unmatched names
        st.success('No Unmatched Village Names')
        # Create a CSV file in memory
        st.subheader("After village LGD Mapping")
        st.write(mapped_dataset.head())
        generate_download_link(mapped_dataset)

    else:
        # Display the dataset with unmatched names
        st.subheader('Unmatched village Names')
        st.write(f'Unmatched villages Count: '+str(len(unmatched_names.unique())))
        st.write(unmatched_names.unique())
        # Display the note
        note = "Please provide the village name variations separated by commas or a single village name."
        st.info(note)
        # Accept comma-separated values or single value only
        st.subheader('Update village Name Variations')
        village_mapping = populate_village_mapping()
        mapped_dataset = create_village_mapped_dataset(village_dataset, village_mapping)
        # Check if there are any unmatched names
        unmatched_names = mapped_dataset[mapped_dataset['village_code'] == -2]['panchayat_name']
        update_variations(unmatched_names.unique(), village_mapping, "villages")
        unmatched_names = mapped_dataset[mapped_dataset['village_code'] == -2]['panchayat_name']
        if unmatched_names.empty:
            st.success('village Name Variations Updated Successfully.')
            # Create a CSV file in memory
            mapped_dataset.to_csv("data.csv",index=False)
            st.subheader("After village LGD Mapping")
            st.write(mapped_dataset.head())
            # Generate download link for the CSV file
            generate_download_link(mapped_dataset)
            


#sub-district mapping
def sub_district_page():
    """
    This function is responsible for displaying the Sub-District LGD mapping page. It fetches the Sub-District mapping dataset,
    maps the dataset, and downloads the mapped dataset. If there are any unmatched Sub-District names, it prompts the user to
    provide the Sub-District name variations. Once the Sub-District name variations are provided, it updates the entityNameVariants
    column in the SQLite table and generates a new mapped dataset for download. If the 'Start Sub-Sub-District/Sub-District Mapping'
    button is clicked, it does nothing. 
    """
    st.title('Sub-District LGD Mapping')
    st.subheader("Before Sub-District LGD Mapping")
    sub_district_dataset = pd.read_csv('data.csv')
    st.write(sub_district_dataset.head())
    # Apply Sub-District mapping and create a new dataset
    sub_district_mapping = populate_sub_district_mapping()

    mapped_dataset = create_sub_district_mapped_dataset(sub_district_dataset, sub_district_mapping)

    # Check if there are any unmatched names
    unmatched_names = mapped_dataset[mapped_dataset['sub_district_code'] == -2]['sub_district_name']

    if unmatched_names.empty:
        # Display a message if there are no unmatched names
        st.success('No Unmatched Sub-District Names')
        mapped_dataset.to_csv("data.csv",index=False)
        # Create a CSV file in memory
        generate_download_link(mapped_dataset)
        if st.button('Start Panchayat Mapping', key='Panchayat_mapping_button'):
                if 'panchayat_name' not in mapped_dataset.columns:
                            st.error("Error: The dataset does not contain the 'panchayat_name' column.")
                            return
                redirect_to_panchayat_page()

    else:
        # Display the dataset with unmatched names
        st.subheader('Unmatched Sub-District Names')
        st.write(f'Unmatched Sub-District Count: '+str(len(unmatched_names.unique())))
        st.write(unmatched_names)

        # Display the note
        note = "Please provide the Sub-District name variations separated by commas or a single Sub-District name."
        st.info(note)

        # Accept comma-separated values or single value only
        st.subheader('Update Sub-District Name Variations')
        sub_district_mapping = populate_sub_district_mapping()
        mapped_dataset = create_sub_district_mapped_dataset(sub_district_dataset, sub_district_mapping)
        unmatched_names = mapped_dataset[mapped_dataset['sub_district_code'] == -2]['sub_district_name']
        update_variations(unmatched_names.unique(), sub_district_mapping, "sub_district")
        unmatched_names = mapped_dataset[mapped_dataset['sub_district_code'] == -2]['sub_district_name']
        if unmatched_names.empty:
            # Display a success message
            st.success('Sub-District Name Variations Updated Successfully.')
            # Create a CSV file in memory
            csv_file = mapped_dataset.to_csv(index=False)
            st.subheader("After Sub-District LGD Mapping")
            st.write(mapped_dataset.head())
            mapped_dataset.to_csv("data.csv",index=False)
            st.write(mapped_dataset.head())
            # Generate download link for the CSV file
            generate_download_link(mapped_dataset)


            if st.button('Start Panchayat Mapping', key='Panchayat_mapping_button'):
                if 'panchayat_name' not in mapped_dataset.columns:
                            st.error("Error: The dataset does not contain the 'panchayat_name' column.")
                            return
                redirect_to_panchayat_page()
    



if __name__ == "__main__":
    main()