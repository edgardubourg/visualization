import streamlit as st
import pandas as pd
import numpy as np
import altair as alt

# Load the CSV file
df = pd.read_csv('data_full_annotated_characters.csv')

# Streamlit App
def main():
    st.title("Interactive Annotation Viewer")
    st.write("Select a work to view relevant annotations.")

    # Extract unique works
    titles = df['Title'].unique()

    # Dropdown for selecting a work
    selected_title = st.selectbox('Select a Work:', titles)

    if selected_title:
        score_label = 'Characters'

        # Ensure scores are between 0 and 6
        selected_score = df.loc[df['Title'] == selected_title, 'score_characters'].values[0]
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
        annotation_text = df.loc[df['Title'] == selected_title, 'annotation_characters'].values[0]
        st.subheader(f"Annotations for '{selected_title}' - {score_label}:")
        st.write(annotation_text)

    # Display the entire table sorted by fictionality score
    st.subheader("All Works Sorted by Fictionality Score:")
    sorted_df = df.sort_values(by='score_characters', ascending=False)
    st.dataframe(sorted_df[['Title', 'score_characters']])

if __name__ == "__main__":
    main()
