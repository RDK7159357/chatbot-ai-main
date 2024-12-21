import streamlit as st
import requests
import google.generativeai as genai

st.title("Plagiarism Checking System")

# Configure APIs
API_KEY = "AIzaSyDLvrG1Vhb5ymn9iWmFPn91el1hGEpE7yA"  # Replace with your actual API key
CUSTOM_SEARCH_ENGINE_ID = "653666bda19864851"  # Replace after creating a Programmable Search Engine
GENAI_MODEL_NAME = "gemini-1.5-flash"

genai.configure(api_key=API_KEY)

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display previous messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Helper function to check plagiarism
def check_plagiarism(text):
    snippets = text.split('.')
    plagiarism_report = []
    for snippet in snippets:
        if snippet.strip():
            query = f'"{snippet.strip()}"'
            url = f"https://www.googleapis.com/customsearch/v1?q={query}&key={API_KEY}&cx={CUSTOM_SEARCH_ENGINE_ID}"
            response = requests.get(url)
            if response.status_code == 200:
                result = response.json()
                if "items" in result:
                    plagiarism_report.append(
                        {"snippet": snippet, "matches": len(result["items"])}
                    )
    return plagiarism_report

# User input
if prompt := st.chat_input("What is up?"):
    # Save user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Call Google Gemini API
    with st.chat_message("assistant"):
        try:
            # Generate response using Gemini
            model = genai.GenerativeModel(GENAI_MODEL_NAME)
            response = model.generate_content(prompt)
            reply = response.text

            # Save assistant response
            st.session_state.messages.append({"role": "assistant", "content": reply})
            st.markdown(reply)

            # Optionally check plagiarism on the user's input
            st.subheader("Plagiarism Check Results")
            plagiarism_results = check_plagiarism(prompt)
            for result in plagiarism_results:
                st.write(
                    f"Snippet: `{result['snippet']}` - Matches found: {result['matches']}"
                )

        except Exception as e:
            st.error(f"Error: {e}")
