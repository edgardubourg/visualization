import streamlit as st
import pandas as pd
import requests
import os
from io import StringIO

# Load dataset using Google Drive link
@st.cache_data
def load_data_chunked():
    url = 'https://drive.google.com/uc?export=download&id=1BJU1YDKvjQy6Rhx18CkgVBAvBkuA304M'
    response = requests.get(url)
    if response.status_code == 200:
        data_iterator = pd.read_csv(StringIO(response.text), chunksize=5000)
        data = pd.concat(data_iterator, ignore_index=True)
        # Standardize column names to avoid KeyError due to mismatches
        data.columns = data.columns.str.strip().str.lower()
        return data
    else:
        st.error("Failed to download dataset. Please check the file link or try again later.")
        return pd.DataFrame()

# Load dataset
data = load_data_chunked()

# Debugging: Display the column names to confirm they match the expected names
if not data.empty:
    st.write("Dataset Columns:", data.columns.tolist())

# Define app structure
def main():
    if data.empty:
        st.error("Dataset could not be loaded. Please try again later.")
        return

    st.title("Literature Analysis App")
    st.header("Explore Fictional Works and Their Characteristics")

    # Dropdown for dataset selection
    dataset = st.selectbox("Select Dataset", ("Babel", "Other"))
    filtered_data = data[data['dataset'] == dataset]
    
    # Dropdowns for time period selection
    year = st.selectbox("Select Year", sorted(filtered_data['year'].dropna().unique()))
    filtered_data = filtered_data[filtered_data['year'] == year]
    
    decade = st.selectbox("Select Decade", sorted(filtered_data['decade'].dropna().unique()))
    filtered_data = filtered_data[filtered_data['decade'] == decade]
    
    century = st.selectbox("Select Century", sorted(filtered_data['century'].dropna().unique()))
    filtered_data = filtered_data[filtered_data['century'] == century]
    
    # Conditional selection for Babel dataset
    if dataset == "Babel":
        author = st.selectbox("Select Author", sorted(filtered_data['author'].dropna().unique()))
        filtered_data = filtered_data[filtered_data['author'] == author]
        
        language = st.selectbox("Select Language", sorted(filtered_data['language'].dropna().unique()))
        filtered_data = filtered_data[filtered_data['language'] == language]
    else:
        st.write("Author and Language selection available for Babel dataset only.")

    # Dropdown for title selection
    title = st.selectbox("Select Title", filtered_data['title'].dropna().unique())

    # Display information for selected title
    if title:
        selected_work = filtered_data[filtered_data['title'] == title].iloc[0]
        st.subheader(f"Fictiveness Score: {selected_work['fictiveness']}")

        # Display table of scores for events, characters, and settings
        st.table({
            'Events': [selected_work['score_events']],
            'Characters': [selected_work['score_characters']],
            'Settings': [selected_work['score_settings']]
        })

        # Display annotations
        st.markdown("**Events Annotation:**")
        st.text(selected_work['annotation_events'])
        st.markdown("**Characters Annotation:**")
        st.text(selected_work['annotation_characters'])
        st.markdown("**Settings Annotation:**")
        st.text(selected_work['annotation_settings'])

    # Display table of works in selected field
    st.markdown("## List of Works in Selected Field")
    sorted_works = filtered_data.sort_values(by='fictiveness', ascending=False)
    title_from_table = st.selectbox("Select from Works Table", sorted_works['title'].dropna().unique())
    if st.button("Select Work from Table") and title_from_table:
        selected_work = filtered_data[filtered_data['title'] == title_from_table].iloc[0]
        st.subheader(f"Fictiveness Score: {selected_work['fictiveness']}")
        st.table({
            'Events': [selected_work['score_events']],
            'Characters': [selected_work['score_characters']],
            'Settings': [selected_work['score_settings']]
        })
        st.markdown("**Events Annotation:**")
        st.text(selected_work['annotation_events'])
        st.markdown("**Characters Annotation:**")
        st.text(selected_work['annotation_characters'])
        st.markdown("**Settings Annotation:**")
        st.text(selected_work['annotation_settings'])

if __name__ == "__main__":
    main()
