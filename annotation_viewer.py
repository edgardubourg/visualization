import streamlit as st
import pandas as pd
import requests

# Function to download file from Google Drive
@st.cache_data
def download_data_from_google_drive():
    url = 'https://drive.google.com/uc?id=1BJU1YDKvjQy6Rhx18CkgVBAvBkuA304M'
    response = requests.get(url)
    open('/tmp/full_annotated.csv', 'wb').write(response.content)
    return pd.read_csv('/tmp/full_annotated.csv')

# Load dataset using Google Drive link
data = download_data_from_google_drive()

# Standardize column names to avoid KeyError due to mismatches
data.columns = data.columns.str.strip().str.lower()

# Define app structure
def main():
    st.title("Literature Analysis App")
    st.header("Explore Fictional Works and Their Characteristics")

    # Dropdown for dataset selection
    dataset = st.selectbox("Select Dataset", ("Babel", "Other"))
    
    # Dropdowns for time period selection
    year = st.selectbox("Select Year", sorted(data['year'].dropna().unique()))
    decade = st.selectbox("Select Decade", sorted(data['decade'].dropna().unique()))
    century = st.selectbox("Select Century", sorted(data['century'].dropna().unique()))
    
    # Conditional selection for Babel dataset
    if dataset == "Babel":
        author = st.selectbox("Select Author", sorted(data[data['dataset'] == 'babel']['author'].dropna().unique()))
        language = st.selectbox("Select Language", sorted(data[data['dataset'] == 'babel']['language'].dropna().unique()))
    else:
        st.write("Author and Language selection available for Babel dataset only.")
        author = None
        language = None

    # Filtering dataset based on user selections
    filtered_data = data[data['dataset'] == dataset]
    filtered_data = filtered_data[filtered_data['year'] == year]
    filtered_data = filtered_data[filtered_data['decade'] == decade]
    filtered_data = filtered_data[filtered_data['century'] == century]
    if author:
        filtered_data = filtered_data[filtered_data['author'] == author]
    if language:
        filtered_data = filtered_data[filtered_data['language'] == language]

    # Dropdown for title selection
    title = st.selectbox("Select Title", filtered_data['title'].dropna().unique())

    # Display information for selected title
    if title:
        selected_work = filtered_data[filtered_data['title'] == title].iloc[0]
        st.subheader(f"Fictiveness Score: {selected_work['fictiveness_score']}")

        # Display table of scores for events, characters, and settings
        st.table({
            'Events': [selected_work['events_score']],
            'Characters': [selected_work['characters_score']],
            'Settings': [selected_work['settings_score']]
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
    sorted_works = filtered_data.sort_values(by='fictiveness_score', ascending=False)
    title_from_table = st.selectbox("Select from Works Table", sorted_works['title'].dropna().unique())
    if st.button("Select Work from Table") and title_from_table:
        selected_work = filtered_data[filtered_data['title'] == title_from_table].iloc[0]
        st.subheader(f"Fictiveness Score: {selected_work['fictiveness_score']}")
        st.table({
            'Events': [selected_work['events_score']],
            'Characters': [selected_work['characters_score']],
            'Settings': [selected_work['settings_score']]
        })
        st.markdown("**Events Annotation:**")
        st.text(selected_work['annotation_events'])
        st.markdown("**Characters Annotation:**")
        st.text(selected_work['annotation_characters'])
        st.markdown("**Settings Annotation:**")
        st.text(selected_work['annotation_settings'])

if __name__ == "__main__":
    main()
