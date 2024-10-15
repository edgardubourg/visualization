ChatGPT 4o with canvas
Vous avez dit :
Data Annotated 1


ADapt this "import streamlit as st
import pandas as pd
import numpy as np
import altair as alt

# Load the CSV file
df = pd.read_csv('data_annotated_1.csv')

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
    main()"
For this dataset (only 3 scores , not the same names etc
ChatGPT a dit :

ChatGPT
Thanks for sharing the data. Based on the structure of your dataset, I'll adapt the Streamlit app to work with the three scores you provided: score_characters, score_events, and score_settings. Additionally, I'll use the appropriate annotation columns for each dimension. Here is the updated version of the app: ​​

I've updated the Streamlit app to use the relevant columns from your dataset, including the three scores (score_characters, score_events, score_settings) and the corresponding annotations. Let me know if you need further adjustments or additional features!








ChatGPT peut faire des erreurs. Envisagez de vérifier les informations importantes.
?
ChatGPT dit : I've updated the Streamlit app to use the relevant columns from your dataset, including the three scores (`score_characters`, `score_events`, `score_settings`) and the corresponding annotations. Let me know if you need further adjustments or additional features!

Annotation Viewer App
1
2
3
4
5
6
7
8
9
10
11
12
13
14
15
16
17
18
19
20
21
22
23
24
25
26
27
28
29
30
31
32
33
34
35
36
37
38
39
40
41
42
43
44
45
46
47
48
49
50
51
52
53
54
55
import streamlit as st
import pandas as pd
import numpy as np
import altair as alt

# Load the CSV file
df = pd.read_csv('data_annotated_1.csv')

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
        scores = ['score_characters', 'score_events', 'score_settings']
        score_labels = ['Characters', 'Events', 'Settings']
        
        # Ensure scores are between 0 and 4
        selected_scores = df.loc[df['Title'] == selected_title, scores].values[0]
        selected_scores = np.clip(selected_scores, 0, 4)  # Clip values to ensure they are within the 0-4 range

        st.subheader(f"Scores for '{selected_title}':")
        score_data = pd.DataFrame({'Dimension': score_labels, 'Score': selected_scores})
        
        # Use Altair to display a bar chart with fixed y-axis limits
        chart = alt.Chart(score_data).mark_bar().encode(
            x=alt.X('Dimension', sort=None),
            y=alt.Y('Score', scale=alt.Scale(domain=[0, 4]))
        ).properties(
            width=600,
            height=400
        )

        st.altair_chart(chart, use_container_width=True)

    # Dropdown for selecting a dimension
    dimensions = ['Characters', 'Events', 'Settings']
    selected_dimension = st.selectbox('Select a Dimension:', dimensions)

    # Display the relevant annotation
    if selected_title and selected_dimension:
        annotation_column = f'annotation_{selected_dimension.lower()}'
        annotation_text = df.loc[df['Title'] == selected_title, annotation_column].values[0]
        st.subheader(f"Annotations for '{selected_title}' - {selected_dimension}:")
        st.write(annotation_text)

if __name__ == "__main__":
    main()
