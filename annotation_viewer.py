import streamlit as st
import pandas as pd
import numpy as np
import altair as alt

# Load the CSV file
df = pd.read_csv('data_annotated_4.csv')

# Streamlit App
def main():
    st.title("Interactive Annotation Viewer")
    st.write("Select a work and a dimension to view relevant annotations.")

    # Extract unique works
    titles = df['Title'].unique()

    # Dropdown for selecting a work
    selected_title = st.selectbox('Select a Work:', titles)

    if selected_title:
        scores = ['score_characters', 'score_events', 'score_settings']
        score_labels = ['Characters', 'Events', 'Settings']

        # Ensure scores are between 0 and 5
        selected_scores = df.loc[df['Title'] == selected_title, scores].values[0]
        selected_scores = np.clip(selected_scores, 0, 5)

        # Display scores
        st.subheader(f"Scores for '{selected_title}':")
        score_data = pd.DataFrame({'Dimension': score_labels, 'Score': selected_scores})

        # Use Altair to display a bar chart with fixed y-axis limits
        chart = alt.Chart(score_data).mark_bar().encode(
            x=alt.X('Dimension', sort=None),
            y=alt.Y('Score', scale=alt.Scale(domain=[0, 5]))
        ).properties(
            width=600,
            height=400
        )

        st.altair_chart(chart, use_container_width=True)

        # Dropdown for selecting a dimension
        selected_dimension = st.selectbox('Select a Dimension:', score_labels)

        # Display the relevant annotation
        if selected_dimension:
            annotation_column = f'annotation_{selected_dimension.lower()}'
            annotation_text = df.loc[df['Title'] == selected_title, annotation_column].values[0]
            st.subheader(f"Annotations for '{selected_title}' - {selected_dimension}:")
            st.write(annotation_text)

    # Display the entire table sorted by fictionality score
    st.subheader("All Works Sorted by Fictionality Score:")
    df['fictionality'] = df['score_characters'] + df['score_events'] + df['score_settings']
    sorted_df = df.sort_values(by='fictionality', ascending=False)
    st.dataframe(sorted_df[['Title', 'score_characters', 'score_events', 'score_settings', 'fictionality']])

if __name__ == "__main__":
    main()
