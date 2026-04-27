# -------------------------------
# 📦 Build Chroma Vector Store (NOMIC VERSION)
# -------------------------------

import os
import pdfplumber
import json
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from langchain_text_splitters import RecursiveCharacterTextSplitter



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
    all_text += json.dumps(data) + "\n"

# Load PDFs
for file in os.listdir("data"):
    if file.endswith(".pdf"):
        with pdfplumber.open(os.path.join("data", file)) as pdf:
            for page in pdf.pages:
                text = page.extract_text()
                if text:
                    all_text += text + "\n"

print("✅ Data Loaded")

# -------------------------------
# ✂️ Chunking (optimized)
# -------------------------------
splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=100
)

docs = splitter.create_documents([all_text])

print(f"📚 Total chunks: {len(docs)}")

# -------------------------------
# 🧩 NOMIC EMBEDDINGS
# -------------------------------
print("⚡ Loading Nomic embeddings...")

embedding = HuggingFaceEmbeddings(
    model_name="nomic-ai/nomic-embed-text-v1",
    model_kwargs={"trust_remote_code": True}
)

print("✅ Embeddings ready")

# -------------------------------
# 🗂️ Create Chroma DB
# -------------------------------
vectorstore = Chroma.from_documents(
    docs,
    embedding=embedding,
    persist_directory="chroma_db"
)



print("✅ Chroma DB saved in 'chroma_db/' folder")
