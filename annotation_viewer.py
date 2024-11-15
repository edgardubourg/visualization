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

# Define app structure
def main():
    st.title("Literature Analysis App")
    st.header("Explore Fictional Works and Their Characteristics")

    # Dropdown for dataset selection
    dataset = st.selectbox("Select Dataset", ("Babel", "Other"))
    
    # Dropdowns for time period selection
    year = st.selectbox("Select Year", sorted(data['Year'].unique()))
    decade = st.selectbox("Select Decade", sorted(data['Decade'].unique()))
    century = st.selectbox("Select Century", sorted(data['Century'].unique()))
    
    # Conditional selection for Babel dataset
    if dataset == "Babel":
        author = st.selectbox("Select Author", sorted(data[data['Dataset'] == 'Babel']['Author'].unique()))
        language = st.selectbox("Select Language", sorted(data[data['Dataset'] == 'Babel']['Language'].unique()))
    else:
        st.write("Author and Language selection available for Babel dataset only.")
        author = None
        language = None

    # Filtering dataset based on user selections
    filtered_data = data[(data['Dataset'] == dataset) & (data['Year'] == year) &
                         (data['Decade'] == decade) & (data['Century'] == century)]
    if author:
        filtered_data = filtered_data[filtered_data['Author'] == author]
    if language:
        filtered_data = filtered_data[filtered_data['Language'] == language]

    # Dropdown for title selection
    title = st.selectbox("Select Title", filtered_data['Title'].unique())

    # Display information for selected title
    selected_work = filtered_data[filtered_data['Title'] == title].iloc[0]
    st.subheader(f"Fictiveness Score: {selected_work['Fictiveness_Score']}")

    # Display table of scores for events, characters, and settings
    st.table({
        'Events': [selected_work['Events_Score']],
        'Characters': [selected_work['Characters_Score']],
        'Settings': [selected_work['Settings_Score']]
    })

    # Display annotations
    st.markdown("**Events Annotation:**")
    st.text(selected_work['Annotation_Events'])
    st.markdown("**Characters Annotation:**")
    st.text(selected_work['Annotation_Characters'])
    st.markdown("**Settings Annotation:**")
    st.text(selected_work['Annotation_Settings'])

    # Display table of works in selected field
    st.markdown("## List of Works in Selected Field")
    sorted_works = filtered_data.sort_values(by='Fictiveness_Score', ascending=False)
    if st.button("Select Work from Table"):
        title_from_table = st.selectbox("Select from Works Table", sorted_works['Title'])
        if title_from_table:
            main(title_from_table)
    

if __name__ == "__main__":
    main()

