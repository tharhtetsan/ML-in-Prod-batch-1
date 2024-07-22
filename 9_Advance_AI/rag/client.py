import requests
import streamlit as st


# streamlit run client.py

st.title("Client Bot")
file = st.file_uploader("Choose a file", type=["pdf"])

if st.button("Submit"):
    if file is not None:
        files = {"file" : (file.name,file, file.type)}
        response = requests.post("http://localhost:8000/upload")
        st.write(response.text)

    else:
        st.write("No file uploaded.")
