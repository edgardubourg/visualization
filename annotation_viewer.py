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
    st.write("Select a work to view relevant annotations.")

    # Extract unique works
    if 'title' not in df.columns:
        st.error("The dataset is missing the 'Title' column.")
        return
    titles = df['title'].unique()

    # Dropdown for selecting a work
    selected_title = st.selectbox('Select a Work:', titles)

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
