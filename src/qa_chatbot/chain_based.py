import os

from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains.retrieval import create_retrieval_chain
from langchain_community.vectorstores import DeepLake
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI, OpenAIEmbeddings

from src.models.embedding_models import EmbeddingModels
from src.models.llm_models import OpenAILLM
from src.utils.chatbot_consts import SYSTEM_PROMPT
from dotenv import load_dotenv

load_dotenv()

llm = ChatOpenAI(model=OpenAILLM.gpt3_turbo.value)

prompt = ChatPromptTemplate.from_messages(
    [
        ("system", SYSTEM_PROMPT),
        ("human", "{input}"),
    ]
)
DEEPLAKE_ID = os.getenv("DEEPLAKE_ID")
DEEPLAKE_DATASET_NAME = os.getenv("DEEPLAKE_DATASET_NAME")

dataset_path = f"hub://{DEEPLAKE_ID}/{DEEPLAKE_DATASET_NAME}"
db = DeepLake(dataset_path=dataset_path, embedding=OpenAIEmbeddings(model=EmbeddingModels.text_embedding_ada_002.value))
retriever = db.as_retriever()

# Create a simple q/a chain
question_answer_chain = create_stuff_documents_chain(llm, prompt)
rag_chain = create_retrieval_chain(retriever, question_answer_chain)

run=True
while run:
    question = input("Ask a question about Stormlight Archive: \n")
    response = rag_chain.invoke({"input": question})
    print("Answer: \n")
    print(response["answer"])

    keep_asking = input("Do you want to keep asking? (y/n) ")

    if keep_asking not in ["yes", "y"]:
        run = False
