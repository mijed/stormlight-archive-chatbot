import polars as pl
from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma
from langchain_text_splitters import RecursiveCharacterTextSplitter

from src.models.embedding_models import EmbeddingModels
from src.utils.consts import RAW_DATA_PATH



data = pl.read_csv(RAW_DATA_PATH / "stormlight_wiki_raw_text_data.csv", separator=";")
data = data.drop_nulls()
texts = data.get_column("text").to_list()
text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
docs = text_splitter.create_documents(texts)

embeddings_function = OpenAIEmbeddings(model=EmbeddingModels.text_embedding_ada_002.value)

vector_store = Chroma(
    collection_name="stormlight_archive_rag_db",
    embedding_function=embeddings_function,
    persist_directory="./stormlight_chroma_db"
)

vector_store.add_documents(docs)