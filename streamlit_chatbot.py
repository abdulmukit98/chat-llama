import streamlit as st
import ollama

st.title("Deepseek R1:1.5b model")

if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": "How can I help you?"}] 


# Write message history
for msg in st.session_state.messages:
    if msg["role"] == "user":
        st.chat_message(msg["role"] ).write(msg["content"])
    else:
        st.chat_message(msg["role"]).write(msg["content"])

def generate_response():
    response = ollama.chat(model="deepseek-r1:1.5b", stream=True, messages=st.session_state.messages)
    for partial_response in response:
        token = partial_response["message"]["content"]
        st.session_state["full_message"] += token
        yield token

if prompt := st.chat_input():
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)
    st.session_state["full_message"] = ""
    st.chat_message("assistant").write_stream(generate_response)
    st.session_state.messages.append({"role": "assistant", "content": st.session_state["full_message"]})

## streamlit run chatbot.py
