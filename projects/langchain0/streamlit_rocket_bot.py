import langchain_helper as lch
import streamlit as st
import textwrap

st.title("Rocket AI Bot")

st.write("Welcome to Rocket AI Bot! I am here to help you.")

query_selectbox = st.selectbox ("Info type", ("Brief", "Comparison"))
query = st.text_input (label="Enter rocket name/s", value="", max_chars=None)



if query_selectbox == "Brief":
    query_type_string = "Brief specs of:"
    if query:
        response = lch.generate_response(query, query_type_string)
        st.write(response)
elif query_selectbox == "Comparison":
    query_type_string = "Comparison of given rockets:"
    if query:
        response = lch.generate_response(query, query_type_string)
        st.write(response)
else:
    pass






