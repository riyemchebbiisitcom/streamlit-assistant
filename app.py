from dotenv import load_dotenv
import streamlit as st
import os
import google.generativeai as genai

# Load environment variables
load_dotenv()

# Configure the Generative AI model
genai.configure(api_key="AIzaSyCXQ9YVSEFtOaBjdS7A9BsNgSQSfsH2jt4")
model = genai.GenerativeModel("gemini-pro") 
chat = model.start_chat(history=[])

def get_gemini_response(question):
    response = chat.send_message(question, stream=True)
    return response

# Initialize the Streamlit app
st.set_page_config(page_title="Gemini Application")

st.header("Ask with Gemini")

# Initialize session state for chat history if it doesn't exist
if 'history' not in st.session_state:
    st.session_state['history'] = []

# Sidebar with expandable history items
st.sidebar.header("Chat History")

def delete_history(index):
    del st.session_state.history[index]

# Display history in the sidebar with expanders
for i, entry in enumerate(st.session_state.history):
    with st.sidebar.expander(f"Q{i+1}"):
        st.write(f"**Input:** {entry['input']}")
        st.write(f"**Response:** {entry['response']}")
        if st.button(f"Delete", key=f"delete_{i}"):
            delete_history(i)
            # Force rerun by setting query parameters
            st.query_params.update(deleted_index=i)

# Input and submit button for new questions
input = st.text_input("", key="input")
submit = st.button("Submit")

 # Dropdown for selecting topics
st.subheader("AI Topics")
topics = {
    "AI": "Artificial Intelligence (AI) is the simulation of human intelligence in machines that are programmed to think, learn, and make decisions like humans.",
    "ML": "Machine Learning (ML) is a subset of AI that enables machines to learn from data and improve their performance without being explicitly programmed.",
    "DL": "Deep Learning (DL) is a subset of ML that uses neural networks with many layers to analyze and learn from vast amounts of data.",
    "NLP": "Natural Language Processing (NLP) is a field of AI that focuses on enabling machines to understand, interpret, and respond to human language."
}

selected_topic = st.selectbox("Select a topic to learn more:", list(topics.keys()))
if selected_topic:
    st.write(f"**{selected_topic}:** {topics[selected_topic]}")


if submit and input:
    response = get_gemini_response(input)
    response_text = ''.join([chunk.text for chunk in response])
    st.session_state.history.append({"input": input, "response": response_text})
    st.write(response_text)
    st.query_params.update(new_question=input)

# streamlit run gemini.py