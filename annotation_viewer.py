{\rtf1\ansi\ansicpg1252\cocoartf2818
\cocoatextscaling0\cocoaplatform0{\fonttbl\f0\fswiss\fcharset0 Helvetica;}
{\colortbl;\red255\green255\blue255;}
{\*\expandedcolortbl;;}
\paperw11900\paperh16840\margl1440\margr1440\vieww11520\viewh8400\viewkind0
\pard\tx720\tx1440\tx2160\tx2880\tx3600\tx4320\tx5040\tx5760\tx6480\tx7200\tx7920\tx8640\pardirnatural\partightenfactor0

\f0\fs24 \cf0 import streamlit as st\
import pandas as pd\
\
# Load the CSV file\
df = pd.read_csv('test_annotated_1.csv')\
\
# Streamlit App\
def main():\
    st.title("Interactive Annotation Viewer")\
    st.write("Select a work and a dimension to view relevant annotations.")\
\
    # Extract unique works\
    titles = df['Title'].unique()\
\
    # Dropdown for selecting a work\
    selected_title = st.selectbox('Select a Work:', titles)\
\
    # Dropdown for selecting a dimension\
    dimensions = ['Characters', 'Events', 'Geography', 'Biology', 'Physics']\
    selected_dimension = st.selectbox('Select a Dimension:', dimensions)\
\
    # Display the relevant annotation\
    if selected_title and selected_dimension:\
        annotation_column = f'annotation_\{selected_dimension.lower()\}'\
        annotation_text = df.loc[df['Title'] == selected_title, annotation_column].values[0]\
        st.subheader(f"Annotations for '\{selected_title\}' - \{selected_dimension\}:")\
        st.write(annotation_text)\
\
if __name__ == "__main__":\
    main()}