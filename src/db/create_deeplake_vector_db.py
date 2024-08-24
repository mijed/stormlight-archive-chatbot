from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import DeepLake
from dotenv import load_dotenv
import os
import polars as pl

from langchain_text_splitters import RecursiveCharacterTextSplitter

from src.utils.consts import RAW_DATA_PATH

load_dotenv()

DEEPLAKE_ID = os.getenv("DEEPLAKE_ID")
DEEPLAKE_DATASET_NAME = os.getenv("DEEPLAKE_DATASET_NAME")


data = pl.read_csv(RAW_DATA_PATH / "stormlight_wiki_raw_text_data.csv", separator=";")
data = data.drop_nulls()
texts = data.get_column("text").to_list()
embeddings_model = OpenAIEmbeddings(model="text-embedding-ada-002")
text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
docs = text_splitter.create_documents(texts)


dataset_path = f"hub://{DEEPLAKE_ID}/{DEEPLAKE_DATASET_NAME}"
db = DeepLake(dataset_path=dataset_path, embedding=embeddings_model)

# Populate the database with embeddings
db.add_documents(docs)
