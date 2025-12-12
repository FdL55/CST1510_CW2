import streamlit as st
from google import genai

# Hide Streamlit default sidebar nav
st.markdown("""
    <style>
        /* Hide built-in page navigation */
        div[data-testid="stSidebarNav"] {
            display: none !important;
        }
    </style>
""", unsafe_allow_html=True)

st.sidebar.title("📌 Navigation")

st.sidebar.page_link("pages/Home.py", label="🏠 Home")
st.sidebar.page_link("pages/1_Login.py", label="🔐 Login")
st.sidebar.page_link("pages/Cybersecurity.py", label="🛡️ Cybersecurity")
st.sidebar.page_link("pages/Data_Science.py", label="📊 Data Science")
st.sidebar.page_link("pages/IT_Operations.py", label="🛠️ IT Operations")
st.sidebar.page_link("pages/3_AI_Assistant.py", label="🤖 AI Assistant")

def userGeminiAPI(queryText):
    client = genai.Client(api_key="AIzaSyBTuNNCzTn1w7ZOXKoF016xeFNmRgCseuA")
    response = client.models.generate_content(
        model='gemini-2.5-flash',
        contents= queryText
    )

    #print(response['model_version'])
    return (response)

st.title('Gemini AI Assistant')

# 1. st.chat_input
# 2. st.chat_message
if st.button("copy the response"):
    print(st.session_state.message)
# define session state to store historic information for a given session
if 'message' not in st.session_state:
    st.session_state.message = []

# to display the previous query data
if len(st.session_state.message)==0:
    st.write("Please start your query using the prompt box below")
for message in st.session_state.message:
    with st.chat_message('user'):
        st.markdown(message)

prompt = st.chat_input('Hello, please type your query here! ')

if prompt:
    st.session_state.message.append(prompt)
    response = userGeminiAPI(prompt)
    # this will execute if we receive some input
    with st.chat_message('user'):
        st.markdown(prompt)
        st.markdown(response)
    #st.markdown(prompt)
    #if "geminiResponse" in st.session_state:
        #for chunk in st.session_state.geminiResponse:
            #st.markdown(chunk.text, end="")