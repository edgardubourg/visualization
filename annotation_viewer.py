import streamlit as st
import pandas as pd
import numpy as np
import altair as alt

# Load the CSV file
df = pd.read_csv('test_annotated_1.csv')

# Streamlit App
def main():
    st.title("Interactive Annotation Viewer")
    st.write("Select a work and a dimension to view relevant annotations.")

    # Extract unique works
    titles = df['Title'].unique()

    # Dropdown for selecting a work
    selected_title = st.selectbox('Select a Work:', titles)

    # Display score bars for the selected work
    if selected_title:
        scores = ['score_characters', 'score_events', 'score_geography', 'score_biology', 'score_physics']
        score_labels = ['Characters', 'Events', 'Geography', 'Biology', 'Physics']
        
        # Ensure scores are between 0 and 3
        selected_scores = df.loc[df['Title'] == selected_title, scores].values[0]
        selected_scores = np.clip(selected_scores, 0, 3)  # Clip values to ensure they are within the 0-3 range

        st.subheader(f"Scores for '{selected_title}':")
        score_data = pd.DataFrame({'Dimension': score_labels, 'Score': selected_scores})
        
        # Use Altair to display a bar chart with fixed y-axis limits
        chart = alt.Chart(score_data).mark_bar().encode(
            x=alt.X('Dimension', sort=None),
            y=alt.Y('Score', scale=alt.Scale(domain=[0, 3]))
        ).properties(
            width=600,
            height=400
        )

        st.altair_chart(chart, use_container_width=True)

    # Dropdown for selecting a dimension
    dimensions = ['Characters', 'Events', 'Geography', 'Biology', 'Physics']
    selected_dimension = st.selectbox('Select a Dimension:', dimensions)

    # Display the relevant annotation
    if selected_title and selected_dimension:
        annotation_column = f'annotation_{selected_dimension.lower()}'
        annotation_text = df.loc[df['Title'] == selected_title, annotation_column].values[0]
        st.subheader(f"Annotations for '{selected_title}' - {selected_dimension}:")
        st.write(annotation_text)

if __name__ == "__main__":
    main()
