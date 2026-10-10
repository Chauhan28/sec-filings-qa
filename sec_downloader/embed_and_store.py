import os
import json
import time
from typing import List
from langchain_community.vectorstores import FAISS

from langchain_core.documents import Document
from langchain_huggingface import HuggingFaceEmbeddings



# === Define Directories ===
base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../"))
parsed_dir = os.path.join(base_dir, "data/parsed")
faiss_dir = os.path.join(base_dir, "data/faiss_index")
os.makedirs(faiss_dir, exist_ok=True)

# === Load All JSON Chunks ===
documents: List[Document] = []
for file in os.listdir(parsed_dir):
    if file.endswith("_chunks.json"):
        ticker = file.replace("_chunks.json", "")
        with open(os.path.join(parsed_dir, file), "r", encoding="utf-8") as f:
            chunks = json.load(f)
        for chunk in chunks:
            documents.append(Document(
                page_content=chunk["page_content"],
                metadata={"ticker": ticker}
            ))

print(f"✅ Loaded {len(documents)} documents.")

# === Embedding Model ===
embedding_model = HuggingFaceEmbeddings(
    model_name="BAAI/bge-small-en-v1.5",
    encode_kwargs={"normalize_embeddings": True},
)

# === Batched Embedding with Throttling ===
batch_size = 500
faiss_index = None

for i in range(0, len(documents), batch_size):
    batch = documents[i:i + batch_size]
    print(f"🔄 Processing batch {i // batch_size + 1}/{(len(documents) + batch_size - 1) // batch_size} with {len(batch)} docs...")

    if faiss_index is None:
        faiss_index = FAISS.from_documents(batch, embedding_model)
    else:
        new_index = FAISS.from_documents(batch, embedding_model)
        faiss_index.merge_from(new_index)

    time.sleep(2)  # Optional: Pause between batches to avoid rate limit

# === Save Vector DB ===
faiss_index.save_local(faiss_dir)
print(f"✅ FAISS index saved to {faiss_dir}")
