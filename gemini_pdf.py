
import os
import PyPDF2
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
import streamlit as st
import google.generativeai as genai
from transformers import pipeline
from PIL import Image
import speech_recognition as sr

# Configure Generative AI model
genai.configure(api_key="AIzaSyB9uvWwEgQSnBwogp93Ab6cwJN8FxFAqHw")
model_gemini = genai.GenerativeModel("gemini-1.5-flash")

# Load emotion detection model
emotion_detector = pipeline("text-classification", model="j-hartmann/emotion-english-distilroberta-base")

# Topic detection function
def detect_topic(query):
    """Basic keyword-based topic detection."""
    topics = {
        "AWS CodeBuild": ["CodeBuild", "CI/CD", "build", "pipeline"],
        "Security": ["IAM", "VPC", "encryption", "shared responsibility"],
        "Teams": ["team", "collaboration", "roles"],
    }
    for topic, keywords in topics.items():
        if any(keyword.lower() in query.lower() for keyword in keywords):
            return topic
    return "General"

# PDF Text Extraction Functions
def extract_text_from_pdf(pdf_path):
    text = ""
    try:
        with open(pdf_path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            for page in reader.pages:
                text += page.extract_text()
    except Exception as e:
        st.error(f"Error reading PDF {pdf_path}: {e}")
    return text

def load_pdfs(folder_path):
    pdf_texts = [
        extract_text_from_pdf(os.path.join(folder_path, filename))
        for filename in os.listdir(folder_path)
        if filename.endswith(".pdf")
    ]
    return pdf_texts

def build_faiss_index(texts, model):
    chunks = [text[i:i + 512] for text in texts for i in range(0, len(text), 512)]
    embeddings = model.encode(chunks)
    index = faiss.IndexFlatL2(embeddings.shape[1])
    index.add(np.array(embeddings))
    return index, chunks

def input_image_setup(uploaded_file):
    if uploaded_file is not None:
        return [{"mime_type": uploaded_file.type, "data": uploaded_file.getvalue()}]
    return None

def detect_emotion(user_input, history):
    emotion_results = emotion_detector(user_input)
    primary_emotion = max(emotion_results, key=lambda x: x['score'])['label']
    confidence = max(emotion_results, key=lambda x: x['score'])['score']

    if history:
        previous_response = history[-1]['response'] if history else ""
        combined_text = previous_response + " " + user_input
        context_emotions = emotion_detector(combined_text)
        context_primary = max(context_emotions, key=lambda x: x['score'])['label']
        return primary_emotion, confidence, context_primary
    return primary_emotion, confidence, None

def retrieve_context(query, index, chunks, model):
    query_embedding = model.encode([query])
    distances, indices = index.search(np.array(query_embedding), k=5)
    return " ".join(chunks[i] for i in indices[0])

def personalize_response(response, emotion, confidence):
    if confidence > 0.8:
        emoji_map = {"joy": "😊", "anger": "😡", "sadness": "😢"}
        prefix = emoji_map.get(emotion, "")
        return f"{prefix} {response}" if prefix else response
    return response

def get_gemini_response(query, context, image_data, history):
    history_context = "\n".join(
        [f"User: {turn['question']}\nAI: {turn['response']}" for turn in history[-5:]]
    )

    prompt = (
        f"You are an expert AI assistant focusing on {st.session_state.current_topic}.\n"
        f"Below is the conversation history:\n{history_context}\n\n"
        f"Here is the current context: {context}\n"
        f"User question: {query}\n"
        f"Respond appropriately and interactively."
    )

    input_data = [query, prompt] + (image_data if image_data else [])
    response = model_gemini.generate_content(input_data)
    return response.text

def record_voice():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        st.info("Listening... Please speak.")
        try:
            audio = recognizer.listen(source, timeout=5)
            return recognizer.recognize_google(audio)
        except sr.WaitTimeoutError:
            st.warning("No speech detected.")
        except sr.UnknownValueError:
            st.warning("Could not understand the audio.")
        except sr.RequestError as e:
            st.error(f"Request error: {e}")
    return None

# Streamlit App Configuration
st.set_page_config(page_title="Gemini Interactive Assistant")
st.header("AI Assistant with PDF, Voice, and Image Knowledge")

folder_path = "pdfs"
if not os.path.exists(folder_path):
    st.sidebar.error("The 'pdfs' folder does not exist.")
    st.stop()

pdf_texts = load_pdfs(folder_path)
if not pdf_texts:
    st.sidebar.error("No PDFs found in the folder.")
    st.stop()

model_pdf = SentenceTransformer('all-MiniLM-L6-v2')
index, chunks = build_faiss_index(pdf_texts, model_pdf)

if "history" not in st.session_state:
    st.session_state.history = []
if "current_topic" not in st.session_state:
    st.session_state.current_topic = "General"

voice_input = st.button("Record Voice")
if voice_input:
    transcription = record_voice()
    if transcription:
        st.session_state.input_query = transcription

input_query = st.text_input("Or type your question:", st.session_state.get("input_query", ""))
uploaded_file = st.file_uploader("Upload an image (optional)", type=["jpg", "jpeg", "png"])

if st.button("Submit") and input_query:
    detected_topic = detect_topic(input_query)
    st.session_state.current_topic = detected_topic
    
    user_emotion, confidence, context_emotion = detect_emotion(input_query, st.session_state.history)
    context = retrieve_context(input_query, index, chunks, model_pdf)
    image_data = input_image_setup(uploaded_file)
    response = get_gemini_response(input_query, context, image_data, st.session_state.history)
    personalized_response = personalize_response(response, user_emotion, confidence)
    
    st.session_state.history.append({"question": input_query, "response": personalized_response, "topic": detected_topic})
    st.write(f"**Topic:** {st.session_state.current_topic}")
    st.write(f"**AI:** {personalized_response}")

st.subheader("Conversation History")
for qa in st.session_state.history:
    st.write(f"**Topic:** {qa.get('topic', 'General')}")
    st.write(f"**You:** {qa['question']}")
    st.write(f"**AI:** {qa['response']}")
    st.write("---")