import langchain_helper as lch
import streamlit as st
import textwrap

st.title("RS AI ChatBot")

st.write("Welcome to RS AI ChatBot! I am here to help you.")


query = st.text_input (label="Enter query", value="", max_chars=None)


if query:
    response = lch.chatbot(query)
    st.write(response)
