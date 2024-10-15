import streamlit as st
import pandas as pd
import numpy as np
import altair as alt

# Load the CSV files
df_with = pd.read_csv('without.csv')
df_without = pd.read_csv('with.csv')

# Streamlit App
def main():
    st.title("Interactive Annotation Viewer")
    st.write("Compare annotations with and without contextual consideration.")

    # Extract unique works
    titles = df_with['Title'].unique()

    # Dropdown for selecting a work
    selected_title = st.selectbox('Select a Work:', titles)

    if selected_title:
        scores = ['score_characters', 'score_events', 'score_settings']
        score_labels = ['Characters', 'Events', 'Settings']

        # Ensure scores are between 0 and 4 for both datasets
        selected_scores_with = df_with.loc[df_with['Title'] == selected_title, scores].values[0]
        selected_scores_with = np.clip(selected_scores_with, 0, 4)

        selected_scores_without = df_without.loc[df_without['Title'] == selected_title, scores].values[0]
        selected_scores_without = np.clip(selected_scores_without, 0, 4)

        # Create dataframes for scores
        score_data_with = pd.DataFrame({'Dimension': score_labels, 'Score': selected_scores_with})
        score_data_without = pd.DataFrame({'Dimension': score_labels, 'Score': selected_scores_without})

        # Create two columns for side-by-side comparison
        col1, col2 = st.columns(2)

        # Display scores with contextual consideration
        with col1:
            st.subheader("With mention: \"Consider the standards and context of the time.\"")
            chart_with = alt.Chart(score_data_with).mark_bar().encode(
                x=alt.X('Dimension', sort=None),
                y=alt.Y('Score', scale=alt.Scale(domain=[0, 4]))
            ).properties(
                width=300,
                height=400
            )
            st.altair_chart(chart_with, use_container_width=True)

            # Display the relevant annotation
            st.subheader(f"Annotations for '{selected_title}' (With Mention):")
            for dimension in score_labels:
                annotation_column = f'annotation_{dimension.lower()}'
                annotation_text = df_with.loc[df_with['Title'] == selected_title, annotation_column].values[0]
                st.write(f"{dimension}: {annotation_text}")

        # Display scores without contextual consideration
        with col2:
            st.subheader("Without mention: \"Consider the standards and context of the time.\"")
            chart_without = alt.Chart(score_data_without).mark_bar().encode(
                x=alt.X('Dimension', sort=None),
                y=alt.Y('Score', scale=alt.Scale(domain=[0, 4]))
            ).properties(
                width=300,
                height=400
            )
            st.altair_chart(chart_without, use_container_width=True)

            # Display the relevant annotation
            st.subheader(f"Annotations for '{selected_title}' (Without Mention):")
            for dimension in score_labels:
                annotation_column = f'annotation_{dimension.lower()}'
                annotation_text = df_without.loc[df_without['Title'] == selected_title, annotation_column].values[0]
                st.write(f"{dimension}: {annotation_text}")

if __name__ == "__main__":
    main()
