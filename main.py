import streamlit as st
import langchain_helper as lch
import textwrap #to wrap text into a page 

st.title("Youtube Transcript Interpreter")

with st.sidebar:
    with st.form(key='my-form'):
        youtube_url = st.sidebar.text_area(
            label="Enter Youtube Video URL",
            max_chars=50
        )
        query = st.sidebar.text_area(
            label="What do you want to know about the video?",
            max_chars=70,
            key="query"
        )

        submit_button = st.form_submit_button(label="submit")

if(query and youtube_url):
    db = lch.create_db(youtube_url)
    response, docs = lch.get_query_response(db, query)
    st.subheader("Answer:")
    st.text(textwrap.fill(response, width=80))


