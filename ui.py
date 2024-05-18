import streamlit as st
import requests

# Setting up the base URL for FastAPI endpoints
BASE_URL = "http://localhost:8000"

def add_note_to_database(text):
    """Sends a post request to add a note to the database."""
    response = requests.post(f"{BASE_URL}/add-note/", json={"text": text})
    return response.json()

def ask_question_and_retrieve_answer(question):
    """Sends a get request to retrieve an answer based on the question."""
    response = requests.get(f"{BASE_URL}/ask-question/", params={"question": question})
    return response.json()

# Streamlit interface
st.title('My Note-taking and Question-Answering App')

# Section to add notes
st.subheader('Add a Note')
note_text = st.text_area("Enter your note here:")
if st.button('Save Note'):
    result = add_note_to_database(note_text)
    if result:
        st.success("Note added successfully!")
    else:
        st.error("An error occurred while adding the note.")

# Section to ask questions
st.subheader('Ask a Question')
question_text = st.text_input("Enter your question:")
if st.button('Get Answer'):
    answer = ask_question_and_retrieve_answer(question_text)
    if answer:
        st.text_area("Answer:", value=answer['answer'], height=300)
    else:
        st.error("An error occurred while retrieving the answer.")
