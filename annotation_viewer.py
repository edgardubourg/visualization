import streamlit as st
import pandas as pd
import numpy as np

# Load the CSV file
df = pd.read_csv('data_full_annotated.csv')

# Normalize column names by stripping whitespace and converting to lowercase
df.columns = df.columns.str.strip().str.lower()

# Streamlit App
def main():
    st.title("Interactive Annotation Viewer")
    st.write("Filter works by century and region, then select a work to view relevant annotations.")

    # Check if required columns exist
    required_columns = ['title', 'century', 'zone', 'score_characters', 'annotation_characters',
                        'score_events', 'annotation_events', 'score_settings', 'annotation_settings']
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

    # Dropdown for selecting country/region with 'All' option
    regions = sorted(filtered_df['zone'].unique())
    regions.insert(0, 'All')
    selected_region = st.selectbox('Select a Region:', regions)

    # Filter by selected region
    if selected_region == 'All':
        region_filtered_df = filtered_df
    else:
        region_filtered_df = filtered_df[filtered_df['zone'] == selected_region]

    # Dropdown for selecting a dimension
    dimensions = ['Characters', 'Events', 'Settings']
    selected_dimension = st.selectbox('Select a Dimension:', dimensions)

    # Set the appropriate score and annotation columns based on the selected dimension
    score_column = f'score_{selected_dimension.lower()}'
    annotation_column = f'annotation_{selected_dimension.lower()}'

    # Display average score for the selected region and dimension
    if not region_filtered_df.empty:
        average_score = region_filtered_df[score_column].mean()
        st.write(f"Average {selected_dimension} Score for {selected_region}: {average_score:.2f}")

    # Filter titles based on selected century, region, and dimension
    filtered_titles = region_filtered_df['title'].unique()

    # Dropdown for selecting a work
    selected_title = st.selectbox('Select a Work:', filtered_titles)

    if selected_title:
        # Display the relevant annotation
        annotation_text = df.loc[df['title'] == selected_title, annotation_column].values[0]
        st.subheader(f"Annotations for '{selected_title}' - {selected_dimension}:")
        st.write(annotation_text)

if __name__ == "__main__":
    main()
