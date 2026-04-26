
#  Farmer Assistant API

import os
from fastapi import FastAPI
from pydantic import BaseModel
from dotenv import load_dotenv

from tavily import TavilyClient
from langchain_core.tools import tool
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.agents import create_agent
from fastapi.responses import StreamingResponse

from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma

# -------------------------------
# INIT
# -------------------------------
app = FastAPI()


# ENV
load_dotenv()

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")


# TOOLS INIT

tavily = TavilyClient(api_key=TAVILY_API_KEY)


# VECTOR STORE (LOAD ON STARTUP)

print("📦 Loading embeddings + Chroma DB...")

persist_dir = os.path.join(os.getcwd(), "chroma_db")

embedding = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2",
    model_kwargs={"device": "cpu"}  # important for Render
)

vectorstore = Chroma(
    persist_directory=persist_dir,
    embedding_function=embedding
)

print("✅ Vector DB Loaded")


# RAG TOOL

@tool
def rag_search(query: str) -> str:
    """Search crop-related knowledge from local database."""

    docs = vectorstore.similarity_search(query, k=5)

    results = [doc.page_content for doc in docs]

    if not results:
        return "No relevant data found."

    return "\n".join(results)


# WEB TOOL

@tool
def web_search(query: str) -> str:
    """Search real-time info like market prices, weather."""

    try:
        response = tavily.search(query=query, max_results=3)

        results = response.get("results", [])

        if not results:
            return "No web results found."

        output = []
        for r in results:
            output.append(r.get("content"))

        return "\n".join(output)

    except Exception as e:
        print("❌ Web search failed:", e)
        return "Web search error"


# LLM + AGENT

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
1. Use RAG for crops, fertilizers, soil.
2. Use web_search for prices, weather, news.
3. You can use BOTH tools.
4. Explain simply for farmers.
"""
)


# REQUEST MODEL

class Query(BaseModel):
    question: str


# HEALTH CHECK

@app.get("/")
def health():
    return {"status": "ok"}

# API ENDPOINT

@app.post("/ask")
def ask(q: Query):

    def stream():
        try:
            response = agent.invoke({
                "messages": [{"role": "user", "content": q.question}]
            })

            # ✅ SAFE EXTRACTION (FIXED)
            text = ""

            if isinstance(response, dict) and "messages" in response:
                msgs = response["messages"]

                if msgs:
                    last = msgs[-1]

                    if hasattr(last, "content"):
                        text = last.content
                    else:
                        text = str(last)

            else:
                text = str(response)

            # fallback if empty
            if not text:
                text = "No response generated."

            # ✅ STREAM OUTPUT
            for char in text:
                yield char

        except Exception as e:
            print("❌ ERROR:", e)
            yield "Error occurred"

    return StreamingResponse(stream(), media_type="text/plain")

# RUN SERVER

if __name__ == "__main__":
    import uvicorn

    port = int(os.environ.get("PORT", 10000))
    print(f"🚀 Starting server on port {port}")

    uvicorn.run("main:app", host="0.0.0.0", port=port)
