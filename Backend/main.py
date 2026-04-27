# -------------------------------
# 🌾 Farmer Assistant API (Pinecone + Gemini)
# -------------------------------

import os
from fastapi import FastAPI
from pydantic import BaseModel
from dotenv import load_dotenv

from tavily import TavilyClient
from langchain_core.tools import tool
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from langchain.agents import create_agent

from langchain_pinecone import PineconeVectorStore
from pinecone import Pinecone

# -------------------------------
# INIT
# -------------------------------
app = FastAPI()
load_dotenv()

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
INDEX_NAME = "farmer-db"

# -------------------------------
# TOOLS INIT
# -------------------------------
tavily = TavilyClient(api_key=TAVILY_API_KEY)

# -------------------------------
# 🔥 EMBEDDINGS (API - NO TORCH)
# -------------------------------
embeddings = GoogleGenerativeAIEmbeddings(
    model="gemini-embedding-001",
    google_api_key=GOOGLE_API_KEY
)

# -------------------------------
# 🌐 PINECONE LOAD
# -------------------------------
pc = Pinecone(api_key=PINECONE_API_KEY)
index = pc.Index(INDEX_NAME)

vectorstore = PineconeVectorStore(
    index=index,
    embedding=embeddings
)

print("✅ Pinecone connected")

# -------------------------------
# 🔎 RAG TOOL
# -------------------------------
@tool
def rag_search(query: str) -> str:
    """Search crop-related knowledge from Pinecone DB."""
    try:
        docs = vectorstore.similarity_search(query, k=3)

        if not docs:
            return "No relevant data found."

        return "\n".join([doc.page_content for doc in docs])

    except Exception as e:
        print("❌ RAG ERROR:", e)
        return "RAG error"

# -------------------------------
# 🌐 WEB TOOL
# -------------------------------
@tool
def web_search(query: str) -> str:
    """Search real-time info like weather, prices."""
    try:
        response = tavily.search(query=query, max_results=3)
        results = response.get("results", [])

        if not results:
            return "No web results found."

        return "\n".join([r.get("content", "") for r in results])

    except Exception as e:
        print("❌ Web error:", e)
        return "Web search error"

# -------------------------------
# 🤖 LLM + AGENT
# -------------------------------
llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    temperature=0,
    google_api_key=GOOGLE_API_KEY
)

agent = create_agent(
    model=llm,
    tools=[rag_search, web_search],
    system_prompt="""
You are a Farmer Support Assistant.

Rules:

1. If question has multiple parts:
   - Break it into sub-questions

2. Use RAG for:
   - crops, fertilizers, soil

3. Use web_search for:
   - market prices, weather, news.

4. You can use BOTH tools if required but do not use your own knowledge.

5. Combine answers clearly.

6. explain answers simply for farmers.
"""
)

# -------------------------------
# REQUEST MODEL
# -------------------------------
class Query(BaseModel):
    question: str

# -------------------------------
# HEALTH
# -------------------------------
@app.get("/")
def health():
    return {"status": "ok"}

# -------------------------------
# ASK
# -------------------------------
@app.post("/ask")
def ask(q: Query):
    print("📩 Question:", q.question)

    try:
        response = agent.invoke({
            "messages": [{"role": "user", "content": q.question}]
        })

        text = ""

        if isinstance(response, dict):
            msgs = response.get("messages", [])

            for msg in reversed(msgs):
                if hasattr(msg, "content") and msg.content:
                    text = msg.content
                    break

        if not text.strip():
            text = "No response generated."

        return {"answer": text}

    except Exception as e:
        print("❌ ERROR:", e)
        return {"answer": "Server error"}
