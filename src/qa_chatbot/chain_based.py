import os
from uuid import uuid4

from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains.retrieval import create_retrieval_chain
from langchain.chains import create_history_aware_retriever
from langchain_chroma import Chroma
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_openai import ChatOpenAI, OpenAIEmbeddings

from src.models.embedding_models import EmbeddingModels
from src.models.llm_models import OpenAILLM
from src.utils.chatbot_consts import CONTEXTUALIZE_Q_SYSTEM_PROMPT, SYSTEM_PROMPT
from dotenv import load_dotenv

load_dotenv()




llm = ChatOpenAI(model=OpenAILLM.gpt3_turbo.value)


contextualize_q_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", CONTEXTUALIZE_Q_SYSTEM_PROMPT),
        MessagesPlaceholder("chat_history"),
        ("human", "{input}"),
    ]
)

prompt = ChatPromptTemplate.from_messages(
    [
        ("system", SYSTEM_PROMPT),
        MessagesPlaceholder("chat_history"),
        ("human", "{input}"),
    ]
)

db = Chroma(
    collection_name="stormlight_archive_rag_db",
    embedding_function=OpenAIEmbeddings(model=EmbeddingModels.text_embedding_ada_002.value),
    persist_directory="./stormlight_chroma_db"
)



retriever = db.as_retriever()

history_aware_retriever = create_history_aware_retriever(
    llm, retriever, contextualize_q_prompt
)

# Create a simple q/a chain
question_answer_chain = create_stuff_documents_chain(llm, prompt)
rag_chain = create_retrieval_chain(history_aware_retriever, question_answer_chain)


### Statefully manage chat history ###
store = {}


def get_session_history(session_id: str) -> BaseChatMessageHistory:
    if session_id not in store:
        store[session_id] = ChatMessageHistory()
    return store[session_id]


conversational_rag_chain = RunnableWithMessageHistory(
    rag_chain,
    get_session_history,
    input_messages_key="input",
    history_messages_key="chat_history",
    output_messages_key="answer",
)

run=True
print("Ask a question about Stormlight Archive.")

session_id = uuid4()
while run:
    question = input("")
    response = conversational_rag_chain.invoke(
        {"input": question},
        config={
        "configurable": {"session_id": session_id}
    }
        )
    print("Answer: \n")
    print(response["answer"])

    keep_asking = input("Do you want to keep asking? (y/n) ")

    if keep_asking not in ["yes", "y"]:
        run = False
