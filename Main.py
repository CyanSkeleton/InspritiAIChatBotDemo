from openai import OpenAI
import streamlit as st

st.title("Not ChatGPT")

# Set OpenAI API key from Streamlit secrets
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# Set a default model
if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-4o-mini"

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = [{'role': 'system', 'content': 'You are a music recommender, helping users discover new'
                                                               ' songs, albums, and artists based on their tastes and'
                                                               ' listening habits. Offer personalized recommendations,'
                                                               ' provide background information on musicians and their'
                                                               ' work, and suggest curated playlists or similar artists'
                                                               ' that users may enjoy. Help users expand their musical'
                                                               ' horizons.'}]

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    if message['role'] != 'system':
        with st.chat_message(message['role']):
            st.markdown(message['content'])

# Accept user input
if prompt := st.chat_input("What is up?"):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)
    # Display assistant response in chat message container
    with st.chat_message("assistant"):
        stream = client.chat.completions.create(
            model=st.session_state["openai_model"],
            messages=[
                {"role": m["role"], "content": m["content"]}
                for m in st.session_state.messages
            ],
            stream=True,
        )
        response = st.write_stream(stream)
    st.session_state.messages.append({"role": "assistant", "content": response})
