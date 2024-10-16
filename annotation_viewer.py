import streamlit as st
import pandas as pd
import numpy as np

# Load the CSV file
df = pd.read_csv('data_full_annotated_characters.csv')

# Normalize column names by stripping whitespace and converting to lowercase
df.columns = df.columns.str.strip().str.lower()

# Streamlit App
def main():
    st.title("Interactive Annotation Viewer")
    st.write("Filter works by century and region, then select a work to view relevant annotations.")

    # Check if required columns exist
    if 'title' not in df.columns or 'year' not in df.columns or 'region' not in df.columns or 'score_characters' not in df.columns:
        st.error("The dataset is missing required columns ('title', 'year', 'region', 'score_characters').")
        return

    # Dropdown for selecting century
    centuries = df['year'].dropna().apply(lambda x: (int(x) // 100) * 100).unique()
    selected_century = st.selectbox('Select a Century:', sorted(centuries))

    # Filter by selected century
    filtered_df = df[df['year'].apply(lambda x: (int(x) // 100) * 100) == selected_century]

    # Display average score for the selected century
    if not filtered_df.empty:
        average_century_score = filtered_df['score_characters'].mean()
        st.write(f"Average Character Score for {selected_century}s: {average_century_score:.2f}")

    # Dropdown for selecting country/region
    regions = filtered_df['region'].unique()
    selected_region = st.selectbox('Select a Region:', sorted(regions))

    # Filter by selected region
    region_filtered_df = filtered_df[filtered_df['region'] == selected_region]

    # Display average score for the selected region
    if not region_filtered_df.empty:
        average_region_score = region_filtered_df['score_characters'].mean()
        st.write(f"Average Character Score for {selected_region}: {average_region_score:.2f}")

    # Filter titles based on selected century and region
    filtered_titles = region_filtered_df['title'].unique()

    # Dropdown for selecting a work
    selected_title = st.selectbox('Select a Work:', filtered_titles)

    if selected_title:
        # Display the relevant annotation
        if 'annotation_characters' not in df.columns:
            st.error("The dataset is missing the 'annotation_characters' column.")
            return
        annotation_text = df.loc[df['title'] == selected_title, 'annotation_characters'].values[0]
        st.subheader(f"Annotations for '{selected_title}':")
        st.write(annotation_text)

if __name__ == "__main__":
    main()
