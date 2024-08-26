import streamlit as st
from uuid import uuid4
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_community.chat_message_histories import ChatMessageHistory
from src.qa_chatbot.chain_based import conversational_rag_chain

st.title("Stormlight Archive Chatbot")

if "session_id" not in st.session_state:
    st.session_state["session_id"] = str(uuid4())

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Ask a question about Stormlight Archive."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        session_id = st.session_state["session_id"]
        
        response = conversational_rag_chain.invoke(
            {"input": prompt},
            config={"configurable": {"session_id": session_id}}
        )
        
        response_text = response["answer"]
        st.markdown(response_text)

        st.sidebar.title("Relevant context chunks")
        for idx, chunk in enumerate(response["context"]):
            st.sidebar.markdown(f"Chunk {idx + 1}:\n{chunk.page_content}\n")

    st.session_state.messages.append({"role": "assistant", "content": response_text})
