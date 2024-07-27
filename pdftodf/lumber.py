import streamlit as st
import pdfplumber
import pandas as pd
import os

def extract_tables_from_pdf(pdf_file_path):
    tables = []
    with pdfplumber.open(pdf_file_path) as pdf:
        for page in pdf.pages:
            table = page.extract_table()
            if table:
                df = pd.DataFrame(table[1:], columns=table[0])
                tables.append(df)
    return tables

st.title("PDF Table Extractor")

uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")

if uploaded_file is not None:
    temp_file_path = f"temp_{uploaded_file.name}"
    with open(temp_file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    
    tables = extract_tables_from_pdf(temp_file_path)
    os.remove(temp_file_path)

    if tables:
        for i, table in enumerate(tables):
            st.write(f"Table {i+1}")
            st.dataframe(table)
    else:
        st.write("No tables found in the PDF.")
