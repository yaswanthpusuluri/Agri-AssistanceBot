# -------------------------------
# 🌾 Farmer Assistant API (Pinecone + Gemini - FINAL)
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
INDEX_NAME = os.getenv("PINECONE_INDEX_NAME", "farmer-db")

# -------------------------------
# VALIDATION (prevents 502 errors)
# -------------------------------
if not GOOGLE_API_KEY:
    raise ValueError("❌ GOOGLE_API_KEY missing")

if not PINECONE_API_KEY:
    raise ValueError("❌ PINECONE_API_KEY missing")

# -------------------------------
# TOOLS INIT
# -------------------------------
tavily = TavilyClient(api_key=TAVILY_API_KEY)

# -------------------------------
# 🔥 EMBEDDINGS (NO TORCH, API BASED)
# -------------------------------
embeddings = GoogleGenerativeAIEmbeddings(
    model="gemini-embedding-001",
    google_api_key=GOOGLE_API_KEY
)

print("✅ Embeddings ready")

# -------------------------------
# 🌐 PINECONE INIT
# -------------------------------
try:
    pc = Pinecone(api_key=PINECONE_API_KEY)
    index = pc.Index(INDEX_NAME)

    vectorstore = PineconeVectorStore(
        index=index,
        embedding=embeddings
    )

    print("✅ Pinecone connected")

except Exception as e:
    print("❌ Pinecone error:", e)
    vectorstore = None

# -------------------------------
# 🔎 RAG TOOL
# -------------------------------
@tool
def rag_search(query: str) -> str:
    """Search crop-related knowledge from vector DB"""
    try:
        if vectorstore is None:
            return "Knowledge base not available."

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
    """Search real-time info like weather, prices"""
    try:
        response = tavily.search(query=query, max_results=3)
        results = response.get("results", [])

        if not results:
            return "No web results found."

        return "\n".join([r.get("content", "") for r in results])

    except Exception as e:
        print("❌ Web ERROR:", e)
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

1. Break complex questions into parts
2. Use RAG for crops, soil, fertilizers
3. Use web for weather, prices, news
4. You may use BOTH tools
5. Do NOT use your own knowledge
6. Explain simply for farmers
"""
)

# -------------------------------
# REQUEST MODEL
# -------------------------------
class Query(BaseModel):
    question: str

# -------------------------------
# HEALTH CHECK
# -------------------------------
@app.get("/")
def health():
    return {"status": "ok"}

# -------------------------------
# ASK ENDPOINT
# -------------------------------
# -------------------------------
# ASK ENDPOINT (FIXED)
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

            # Look for the last message that has content
            for msg in reversed(msgs):
                if hasattr(msg, "content") and msg.content:
                    raw_content = msg.content
                    
                    # --- FIX STARTS HERE ---
                    # If content is a list (e.g., [{'text': '...'}, ...]), extract the text
                    if isinstance(raw_content, list):
                        parts = []
                        for part in raw_content:
                            if isinstance(part, dict):
                                parts.append(part.get("text", ""))
                            else:
                                parts.append(str(part))
                        text = " ".join(parts)
                    else:
                        text = str(raw_content)
                    # --- FIX ENDS HERE ---
                    
                    if text.strip(): # Now text is guaranteed to be a string
                        break

        if not text.strip():
            text = "I couldn't find a specific answer for that. Could you rephrase?"

        print("✅ FINAL:", text)
        return {"answer": text}

    except Exception as e:
        print("❌ ERROR:", e)
        return {"answer": f"Server error: {str(e)}"}
