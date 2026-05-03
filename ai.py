"""
ai.py provides answers to users input questions
by using AzureOpenAI
Functions as a travel advisor to the users
"""
import streamlit as st
from openai import AzureOpenAI

def get_response(system_prompt, placeholder="Ask me anything about travel!", chat_key="messages"):
    """ Renders an AI Chatbot interface using Azure OpenAI,
    takes a system prompt to define teh AI's role, a placeholder for the chat input,
    and a chat_key to store separate conversation histories for diff pages"""
    openai_api_key = st.secrets["AZURE_OPENAI_API_KEY"]
    openai_api_endpoint = st.secrets["AZURE_OPENAI_ENDPOINT"]
    # set up the client
    client = AzureOpenAI(
        api_key=openai_api_key,
        api_version="2024-02-15-preview",
        azure_endpoint=openai_api_endpoint
    )
    # create chat input
    if chat_key not in st.session_state:
        st.session_state[chat_key] = []  # if no input messages, return empty
    # show the chat history
    for message in st.session_state[chat_key]:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # handle user input, use the text box at the bottom
    if prompt := st.chat_input(placeholder):
        st.session_state[chat_key].append({"role": "user", "content": prompt})  # add the message to history
        with st.chat_message("user"):
            st.markdown(prompt)

        # get response from ai
        with st.chat_message("assistant"):
            stream = client.chat.completions.create(
                model=st.secrets["AZURE_OPENAI_MODEL"],
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": prompt}
                ],
                stream=True,
            )
            response = st.write_stream(stream)
        st.session_state[chat_key].append({"role": "assistant", "content": response})  # save the ai to history
