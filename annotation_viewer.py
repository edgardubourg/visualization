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
    required_columns = ['title', 'century', 'zone', 'score_characters', 'annotation_characters']
    missing_columns = [col for col in required_columns if col not in df.columns]
    if missing_columns:
        st.error(f"The dataset is missing required columns: {missing_columns}")
        return

    # Dropdown for selecting century with 'All' option
    centuries = sorted(df['century'].dropna().unique())
    centuries.insert(0, 'All')
    selected_century = st.selectbox('Select a Century:', centuries)

    # Filter by selected century
    if selected_century == 'All':
        filtered_df = df
    else:
        filtered_df = df[df['century'] == selected_century]

    # Display average score for the selected century
    if not filtered_df.empty:
        average_century_score = filtered_df['score_characters'].mean()
        st.write(f"Average Character Score for {selected_century}s: {average_century_score:.2f}")

    # Dropdown for selecting country/region with 'All' option
    regions = sorted(filtered_df['zone'].unique())
    regions.insert(0, 'All')
    selected_region = st.selectbox('Select a Region:', regions)

    # Filter by selected region
    if selected_region == 'All':
        region_filtered_df = filtered_df
    else:
        region_filtered_df = filtered_df[filtered_df['zone'] == selected_region]

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
        annotation_text = df.loc[df['title'] == selected_title, 'annotation_characters'].values[0]
        st.subheader(f"Annotations for '{selected_title}':")
        st.write(annotation_text)

if __name__ == "__main__":
    main()
