# -------------------------------
# 📦 Build Chroma Vector Store
# -------------------------------

import os
import pdfplumber
import json
from langchain_text_splitters import CharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma

# -------------------------------
# 📄 Load all data
# -------------------------------
all_text = ""

# Load TXT
with open("data/crop_fertilizers.txt", "r", encoding="utf-8") as f:
    all_text += f.read() + "\n"

# Load JSON
with open("data/crop_diseases.json", "r", encoding="utf-8") as f:
    data = json.load(f)
    all_text += json.dumps(data)

# Load PDF
for file in os.listdir("data"):
    if file.endswith(".pdf"):
        with pdfplumber.open("data/" + file) as pdf:
            for page in pdf.pages:
                text = page.extract_text()
                if text:
                    all_text += text + "\n"

print("✅ Data Loaded")

# -------------------------------
# ✂️ Chunking
# -------------------------------
splitter = CharacterTextSplitter(chunk_size=500, chunk_overlap=100)
docs = splitter.create_documents([all_text])

# -------------------------------
# 🧩 Embeddings
# -------------------------------
embedding = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-mpnet-base-v2"
)

# -------------------------------
# 🗂️ Create Chroma DB
# -------------------------------
vectorstore = Chroma.from_documents(
    docs,
    embedding,
    persist_directory="chroma_db"   # 👈 replaces .pkl
)

# -------------------------------
# 💾 Persist to disk
# -------------------------------
vectorstore.persist()

print("✅ Chroma DB saved in 'chroma_db/' folder")