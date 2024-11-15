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
    if 'year' in data.columns:
        year = st.selectbox("Select Year", sorted(data['year'].unique()))
    else:
        year = None
    if 'decade' in data.columns:
        decade = st.selectbox("Select Decade", sorted(data['decade'].unique()))
    else:
        decade = None
    if 'century' in data.columns:
        century = st.selectbox("Select Century", sorted(data['century'].unique()))
    else:
        century = None
    
    # Conditional selection for Babel dataset
    if dataset == "Babel":
        if 'dataset' in data.columns and 'babel' in data['dataset'].str.lower().unique():
            if 'author' in data.columns:
                author = st.selectbox("Select Author", sorted(data[data['dataset'] == 'babel']['author'].unique()))
            else:
                author = None
            if 'language' in data.columns:
                language = st.selectbox("Select Language", sorted(data[data['dataset'] == 'babel']['language'].unique()))
            else:
                language = None
        else:
            st.write("Author and Language selection available for Babel dataset only.")
            author = None
            language = None
    else:
        st.write("Author and Language selection available for Babel dataset only.")
        author = None
        language = None

    # Filtering dataset based on user selections
    filtered_data = data[data['dataset'] == dataset]
    if year is not None:
        filtered_data = filtered_data[filtered_data['year'] == year]
    if decade is not None:
        filtered_data = filtered_data[filtered_data['decade'] == decade]
    if century is not None:
        filtered_data = filtered_data[filtered_data['century'] == century]
    if author:
        filtered_data = filtered_data[filtered_data['author'] == author]
    if language:
        filtered_data = filtered_data[filtered_data['language'] == language]

    # Dropdown for title selection
    if 'title' in filtered_data.columns:
        title = st.selectbox("Select Title", filtered_data['title'].unique())
    else:
        title = None

    # Display information for selected title
    if title:
        selected_work = filtered_data[filtered_data['title'] == title].iloc[0]
        if 'fictiveness_score' in selected_work:
            st.subheader(f"Fictiveness Score: {selected_work['fictiveness_score']}")

        # Display table of scores for events, characters, and settings
        if {'events_score', 'characters_score', 'settings_score'}.issubset(filtered_data.columns):
            st.table({
                'Events': [selected_work['events_score']],
                'Characters': [selected_work['characters_score']],
                'Settings': [selected_work['settings_score']]
            })

        # Display annotations
        if 'annotation_events' in selected_work:
            st.markdown("**Events Annotation:**")
            st.text(selected_work['annotation_events'])
        if 'annotation_characters' in selected_work:
            st.markdown("**Characters Annotation:**")
            st.text(selected_work['annotation_characters'])
        if 'annotation_settings' in selected_work:
            st.markdown("**Settings Annotation:**")
            st.text(selected_work['annotation_settings'])

    # Display table of works in selected field
    if 'fictiveness_score' in filtered_data.columns:
        st.markdown("## List of Works in Selected Field")
        sorted_works = filtered_data.sort_values(by='fictiveness_score', ascending=False)
        if st.button("Select Work from Table"):
            title_from_table = st.selectbox("Select from Works Table", sorted_works['title'])
            if title_from_table:
                main(title_from_table)

if __name__ == "__main__":
    main()
