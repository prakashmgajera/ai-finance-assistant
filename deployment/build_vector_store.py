import json
import os
from llama_index.core import Document, VectorStoreIndex
from llama_index.vector_stores.qdrant import QdrantVectorStore
from qdrant_client import QdrantClient
from llama_index.embeddings.openai import OpenAIEmbedding

# Load repaired crawled data
with open('crawled_finance_docs_repaired.json', 'r') as f:
    crawled_docs = json.load(f)

# Convert crawled data to LlamaIndex Documents
llama_docs = []
for doc in crawled_docs:
    llama_docs.append(
        Document(
            text=doc.get('content', ''),
            metadata={
                'source_url': doc.get('url', ''),
                'title': doc.get('title', '')
            }
        )
    )




# Build and persist vector store in Qdrant Cloud using QdrantClient
api_key = os.getenv("QDRANT_API_KEY")
if not api_key:
    raise ValueError("QDRANT_API_KEY environment variable not set. Please provide your Qdrant Cloud API key via the UI or environment.")
qdrant_client = QdrantClient(
    url="https://6f1a0c83-2778-4e95-af4e-6b6506891a53.us-west-2-0.aws.cloud.qdrant.io",
    api_key=api_key
)
vector_store = QdrantVectorStore(client=qdrant_client, collection_name="finance_docs")
index = VectorStoreIndex(vector_store, embed_model=OpenAIEmbedding())
index.add_documents(llama_docs)

print(f"Indexed {len(llama_docs)} documents into Qdrant vector store.")
