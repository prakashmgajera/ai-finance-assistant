import os
import yaml
import requests
from bs4 import BeautifulSoup
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np

DATA_PATH = os.path.join(os.path.dirname(__file__), '../data/knowledge_base_sources.yaml')
VECTOR_DB_PATH = os.path.join(os.path.dirname(__file__), 'vector_db.faiss')

# Load sources
with open(DATA_PATH, 'r') as f:
    SOURCES = yaml.safe_load(f)["sources"]

# Initialize embedding model
model = SentenceTransformer('all-MiniLM-L6-v2')

# Crawl and chunk content
chunks = []
chunk_sources = []
for url in SOURCES:
    try:
        resp = requests.get(url, timeout=10)
        soup = BeautifulSoup(resp.text, 'html.parser')
        # Get all text from paragraphs
        paragraphs = [p.get_text() for p in soup.find_all('p')]
        for para in paragraphs:
            if len(para.strip()) > 50:
                chunks.append(para.strip())
                chunk_sources.append(url)
    except Exception as e:
        print(f"Failed to fetch {url}: {e}")

# Embed chunks
embeddings = model.encode(chunks)
embeddings = np.array(embeddings).astype('float32')

# Build FAISS index
index = faiss.IndexFlatL2(embeddings.shape[1])
index.add(embeddings)
faiss.write_index(index, VECTOR_DB_PATH)

# Save chunk sources for retrieval
with open(os.path.join(os.path.dirname(__file__), 'chunk_sources.yaml'), 'w') as f:
    yaml.dump({'chunks': chunks, 'sources': chunk_sources}, f)

print(f"Vector store built with {len(chunks)} chunks from {len(SOURCES)} sources.")
