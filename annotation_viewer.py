import streamlit as st
import pandas as pd

# Load the CSV file
df = pd.read_csv('test_annotated_1.csv')

# Ensure scores are between 0 and 3
score_columns = ['score_characters', 'score_events', 'score_geography', 'score_biology', 'score_physics']
df[score_columns] = df[score_columns].clip(0, 3)

# Streamlit App
def main():
    st.title("Interactive Annotation Viewer")
    st.write("Select a work and a dimension to view relevant annotations and compare scores.")

    # Extract unique works
    titles = df['Title'].unique()

    # Dropdown for selecting a work
    selected_title = st.selectbox('Select a Work:', titles)

    # Display score bars for the selected work and mean scores
    if selected_title:
        scores = ['score_characters', 'score_events', 'score_geography', 'score_biology', 'score_physics']
        score_labels = ['Characters', 'Events', 'Geography', 'Biology', 'Physics']
        selected_scores = df.loc[df['Title'] == selected_title, scores].values[0]

        # Calculate mean scores
        mean_scores = df[scores].mean().values

        st.subheader(f"Scores for '{selected_title}':")
        score_data = pd.DataFrame({
            'Dimension': score_labels,
            'Selected Work Score': selected_scores,
            'Mean Score': mean_scores
        })

        # Display the bar chart with selected work's score and mean score
        st.bar_chart(score_data.set_index('Dimension'))

        # Display the mean scores alongside the selected work's scores with a legend
        st.write("""
            **Legend:**
            - *Selected Work Score*: Score for the selected work
            - *Mean Score*: Average score across all works
        """)

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
