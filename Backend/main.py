# -------------------------------
# 🌾 Farmer Assistant API
# -------------------------------

import os
from fastapi import FastAPI
from pydantic import BaseModel
from dotenv import load_dotenv

from tavily import TavilyClient
from langchain_core.tools import tool
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.agents import create_agent
from fastapi.responses import StreamingResponse

# ✅ NEW IMPORTS (Chroma)
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma

# -------------------------------
# INIT
# -------------------------------
app = FastAPI()

# -------------------------------
# ENV
# -------------------------------
load_dotenv()

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")

# -------------------------------
# LOAD TOOLS
# -------------------------------
tavily = TavilyClient(api_key=TAVILY_API_KEY)

# ✅ REPLACED VECTOR DB LOADING
embedding = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-mpnet-base-v2"
)

vectorstore = Chroma(
    persist_directory="chroma_db",
    embedding_function=embedding
)

# -------------------------------
# RAG TOOL
# -------------------------------
@tool
def rag_search(query: str) -> str:
    """Search crop-related knowledge from local database."""

    docs = vectorstore.similarity_search(query, k=5)

    # extract text
    results = [doc.page_content for doc in docs]

    if not results:
        return "NOTFOUND"

    return "\n".join(results)

# -------------------------------
# WEB TOOL
# -------------------------------
@tool
def web_search(query: str) -> str:
    """Search real-time info like market prices, weather."""

    try:
        response = tavily.search(query=query, max_results=3)

        results = response.get("results", [])

        if not results:
            return "NOTFOUND"

        output = []
        for r in results:
            output.append(r.get("content"))

        return "\n".join(output)

    except Exception as e:
        print("❌ Web search failed:", e)
        return "WEB_ERROR"

# -------------------------------
# LLM + AGENT
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
# API ENDPOINT
# -------------------------------
@app.post("/ask")
def ask(q: Query):

    def stream():
        try:
            response = agent.invoke({
                "messages": [{"role": "user", "content": q.question}]
            })

            last = response["messages"][-1]
            content = last.content if hasattr(last, "content") else str(last)

            if isinstance(content, str):
                text = content

            elif isinstance(content, list):
                text = ""
                for item in content:
                    if isinstance(item, dict) and "text" in item:
                        text += item["text"]

            else:
                text = str(content)

            for char in text:
                yield char

        except Exception as e:
            print("❌ ERROR:", e)
            yield "Error occurred"

    return StreamingResponse(stream(), media_type="text/plain")
