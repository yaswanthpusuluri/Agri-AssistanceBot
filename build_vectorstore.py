# -------------------------------
# 🌾 Build Pinecone Vector DB
# -------------------------------

import os
import json
import pdfplumber
from dotenv import load_dotenv

from langchain_text_splitters import CharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_pinecone import PineconeVectorStore

from pinecone import Pinecone, ServerlessSpec

# -------------------------------
# INIT
# -------------------------------
load_dotenv()

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")

INDEX_NAME = "farmer-db"

# -------------------------------
# 📄 LOAD DATA
# -------------------------------
all_text = ""

# TXT
with open("data/crop_fertilizers.txt", "r", encoding="utf-8") as f:
    all_text += f.read() + "\n"

# JSON
with open("data/crop_diseases.json", "r", encoding="utf-8") as f:
    data = json.load(f)
    all_text += json.dumps(data)

# PDF
for file in os.listdir("data"):
    if file.endswith(".pdf"):
        with pdfplumber.open(os.path.join("data", file)) as pdf:
            for page in pdf.pages:
                text = page.extract_text()
                if text:
                    all_text += text + "\n"

print("✅ Data Loaded")

# -------------------------------
# ✂️ CHUNKING
# -------------------------------
splitter = CharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=100
)

docs = splitter.create_documents([all_text])

print(f"📚 Total chunks: {len(docs)}")

# -------------------------------
# 🔥 EMBEDDINGS (API - NO TORCH)
# -------------------------------
embeddings = GoogleGenerativeAIEmbeddings(
    model="models/embedding-001",
    google_api_key=GOOGLE_API_KEY
)

print("✅ Embeddings ready")

# -------------------------------
# 🌐 PINECONE INIT
# -------------------------------
pc = Pinecone(api_key=PINECONE_API_KEY)

# Create index if not exists
if INDEX_NAME not in [i["name"] for i in pc.list_indexes()]:
    print("⚡ Creating Pinecone index...")

    pc.create_index(
        name=INDEX_NAME,
        dimension=768,   # Gemini embedding dimension
        metric="cosine",
        spec=ServerlessSpec(
            cloud="aws",
            region="us-east-1"
        )
    )

print("✅ Pinecone index ready")

# Connect index
index = pc.Index(INDEX_NAME)

# -------------------------------
# 🚀 UPLOAD TO PINECONE
# -------------------------------
vectorstore = PineconeVectorStore(
    index=index,
    embedding=embeddings
)

vectorstore.add_documents(docs)

print("🚀 Data uploaded to Pinecone successfully!")
