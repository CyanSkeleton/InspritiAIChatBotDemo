from openai import OpenAI
import streamlit as st

st.title("ChefGPT")

# Set OpenAI API key from Streamlit secrets
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# Set a default model
if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-4o-mini"

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = [{'role': 'system', 'content': 'You are ChefGPT, a warm and enthusiastic culinary '
                                                               'assistant. Your goal is to help users cook delicious '
                                                               'meals by providing personalized recipes, practical '
                                                               'cooking tips, and substitution ideas. You guide users '
                                                               'through steps clearly, offer adaptations for dietary '
                                                               'needs, and explain techniques simply. You bring flavor'
                                                               ' and fun to every recipe, making home cooking exciting'
                                                               ' and approachable.'}]

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
