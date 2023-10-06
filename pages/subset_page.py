import base64
import streamlit as st

from pg_utils_fn import process_file


st.title("Select Specific Columns from CSV/Excel File")

#st.set_page_config(page_title="Subset Page", page_icon="📊")

st.markdown("Subset Page")
st.sidebar.header("Subset Page")
    
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