import streamlit as st
import pandas as pd
import numpy as np
import altair as alt

# Load the CSV file
df = pd.read_csv('data_full_annotated_characters.csv')

# Normalize column names by stripping whitespace and converting to lowercase
df.columns = df.columns.str.strip().str.lower()

# Streamlit App
def main():
    st.title("Interactive Annotation Viewer")
    st.write("Select a work to view relevant annotations.")

    # Debugging: Display available columns
    st.write("Available columns in dataset:", df.columns.tolist())

    # Extract unique works
    if 'title' not in df.columns:
        st.error("The dataset is missing the 'Title' column.")
        return
    titles = df['title'].unique()

    # Dropdown for selecting a work
    selected_title = st.selectbox('Select a Work:', titles)

    if selected_title:
        score_label = 'Characters'

        # Ensure scores are between 0 and 6
        if 'score_characters' not in df.columns:
            st.error("The dataset is missing the 'score_characters' column.")
            return
        selected_score = df.loc[df['title'] == selected_title, 'score_characters'].values[0]
        selected_score = np.clip(selected_score, 0, 6)

        # Display score
        st.subheader(f"Score for '{selected_title}':")
        score_data = pd.DataFrame({'Dimension': [score_label], 'Score': [selected_score]})

        # Use Altair to display a bar chart with fixed y-axis limits
        chart = alt.Chart(score_data).mark_bar().encode(
            x=alt.X('Dimension', sort=None),
            y=alt.Y('Score', scale=alt.Scale(domain=[0, 6]))
        ).properties(
            width=600,
            height=400
        )

        st.altair_chart(chart, use_container_width=True)

        # Display the relevant annotation
        if 'annotation_characters' not in df.columns:
            st.error("The dataset is missing the 'annotation_characters' column.")
            return
        annotation_text = df.loc[df['title'] == selected_title, 'annotation_characters'].values[0]
        st.subheader(f"Annotations for '{selected_title}' - {score_label}:")
        st.write(annotation_text)

    # Display the entire table sorted by characters score
    if 'score_characters' in df.columns:
        st.subheader("All Works Sorted by Character Score:")
        sorted_df = df.sort_values(by='score_characters', ascending=False)
        st.dataframe(sorted_df[['title', 'score_characters']])

if __name__ == "__main__":
    main()
