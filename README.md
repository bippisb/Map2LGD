# Map2LGD LGD Mapping App

Welcome to the "Map2LGD" LGD Mapping App! 🌟 This app simplifies the process of mapping LGD (Local Government Directory) codes for different administrative levels such as states, districts, sub-districts, blocks, gram panchayats, and villages in India. Whether you're a researcher, data analyst, or just curious about India's geography, this app is designed to make mapping a breeze.

### Basic Information

This Streamlit web application, named "Map2LGD" is developed to facilitate the mapping of LGD codes across various administrative levels in India. The app allows users to upload CSV or Excel files containing location data and then performs LGD code mapping based on the provided data. It offers mapping for states, districts, sub-districts, blocks, gram panchayats (GPs), and villages.

The app is structured into different sections for each administrative level, and it guides users through the mapping process, starting from states down to villages. The user is required to upload files containing location data for each level, and the app performs the mapping using predefined mappings and variations.

### Architecture

The Map2LGD is built using Python and the Streamlit library, which allows for the creation of interactive web applications with minimal code. The app follows a modular architecture, with different functions responsible for specific tasks such as data processing, mapping, variation updates, and page navigation.

Here's a brief overview of the components and architecture of the app:

- **Import Statements**: The app starts by importing necessary libraries, including Streamlit, pandas, and custom utility functions from various modules.

- **Page Routing**: The `page_route()` function reads query parameters from the URL to determine which page to display. It routes users to different pages based on their selection, including state mapping, district mapping, block mapping, GP mapping, village mapping, and sub-district mapping.

- **Main App Logic**: The `main()` function sets up the Streamlit configuration and calls the `page_route()` function to start the app's main logic.

- **Mapping Functions**: The app uses separate functions for mapping data at different administrative levels (state, district, block, GP, village, sub-district). These functions handle data processing, mapping, unmatched name handling, and user input for name variations.

- **Utility Functions**: The app includes utility functions for loading files, fetching mapping data, creating mapped datasets, generating download links, updating variations, and more.

- **Web Interface**: The web interface is created using Streamlit's user interface components. It features buttons, file uploaders, data displays, information messages, and interactive elements to guide users through the mapping process.


### Features

- Streamlined mapping process for states, districts,sub-districts, blocks, gram panchayats and villages .
- Handling of unmatched names by updating variations for accurate mapping.

### Usage Instructions

1. **Home Page**: Upon launching the app, users are greeted with an introduction and instructions for using the app. The home page provides a button to start the mapping process.

2. **State Mapping Page**: This page allows users to upload a dataset with a 'state_name' column and perform LGD mapping for states. Unmatched state names can be updated with variations.

3. **District Mapping Page**: After mapping states, users can navigate to this page to map districts. Users can also update district name variations.
4. **Sub-District Mapping Page**: If sub-districts are included in the data, this page allows users to map them and update variations for unmatched names.

5. **Block Mapping Page**: Users can proceed to map blocks after mapping districts. Similar to previous steps, unmatched block names can be updated with variations.

6. **Gram Panchayat Mapping Page**: This page facilitates mapping of gram panchayats. The process includes handling unmatched GP names and providing name variations.

7. **Village Mapping Page**: Users can map villages on this page, with options to update variations for unmatched village names.

8. **Download Mapped Data**: At each mapping step, the app generates a downloadable CSV file containing the mapped data. Users can download these files for further analysis.

Please note that variations for unmatched names should be provided carefully to ensure accurate mapping.


### Getting Started

Follow the instructions below to get the Map2LGD LGD Mapping App up and running on your local machine for development and testing purposes.

### Prerequisites

- Python 3.9.4
- Streamlit (`pip install streamlit`)
- pandas (`pip install pandas`)

### Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/bippisb/Map2LGD.git
   ```

2. Navigate to the project directory:

   ```bash
   cd Map2LGD
   ```

3. Install the required dependencies:

   ```bash
   pip install -r requirements.txt
   ```

### Usage

1. Run the Streamlit app:

   ```bash
   streamlit run app.py
   ```

2. The app will open in your default web browser.

3. Follow the on-screen instructions to upload your data files, perform LGD code mapping, and generate mapped datasets.




### References

- Streamlit Documentation: [Streamlit](https://streamlit.io/)
- LGD Data: [Local Government Directory](https://lgdirectory.gov.in/)

### Contact Information

For questions, feedback, or concerns, please contact [Email](saurabh_harak@isb.edu) .

### Important Note

Before using the app, please ensure that your data files have appropriate column names. The column names required for each administrative level are specified on the home page.

Feel free to explore, map LGD codes, and enjoy a hassle-free mapping experience with the Map2LGD LGD Mapping App! 🗺️🚀







