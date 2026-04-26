 ## 🌾 Farmer Assistant (RAG + AI Agent)

An AI-powered Farmer Assistant that provides accurate answers to agriculture-related questions by combining **local knowledge (RAG)** with **real-time web search**.

The system uses an intelligent AI agent to dynamically choose between a **vector database (Chroma)** and **web search (Tavily)**, then generates clear and simple responses using **Google Gemini**.

---

## 🚀 Features

* 📄 **RAG-based Knowledge Search**
  Retrieves crop, soil, and fertilizer information from a local vector database.

* 🌐 **Real-time Web Search**
  Fetches live data such as weather updates, market prices, and agricultural news.

* 🤖 **AI Agent Decision Making**
  Automatically selects the best tool (RAG or Web) based on the query.

* ⚡ **Streaming Responses**
  Provides a ChatGPT-like typing experience in the UI.

* 💬 **Interactive Chat UI**
  Built with Streamlit, including chat history.

---

## 🧠 How It Works

```text
User Question
      ↓
   AI Agent
      ↓
 ┌───────────────┬────────────────┐
 │               │                │
RAG Search   Web Search     (if needed both)
(Chroma)     (Tavily API)
 │               │
 └───────┬───────┘
         ↓
   Gemini LLM
         ↓
   Final Answer (Streamed)
```

---

## 🛠️ Tech Stack

* **Backend:** FastAPI
* **Frontend:** Streamlit
* **LLM:** Google Gemini (via LangChain)
* **Agent Framework:** LangChain
* **Vector Database:** Chroma
* **Embeddings:** Sentence Transformers
* **Web Search:** Tavily API
* **PDF Processing:** pdfplumber

---

## 📂 Project Structure

```text
project/
│── app.py                # Streamlit UI
│── main.py               # FastAPI backend (API + Agent)
│── chroma_db/            # Persisted Chroma vector database
│── requirements.txt      # Dependencies
│── .env                  # API keys
```

---

## ⚙️ Setup Instructions

### 1. Clone the Repository

```bash
git clone <your-repo-url>
cd <your-project-folder>
```

---

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

---

### 3. Set Environment Variables

Create a `.env` file:

```env
GOOGLE_API_KEY=your_google_api_key
TAVILY_API_KEY=your_tavily_api_key
```

---

### 4. (Optional) Build Vector Database

If `chroma_db/` is not included:

```bash
python build_vectordb.py
```

---

### 5. Run Backend (FastAPI)

```bash
uvicorn main:app --reload
```

---

### 6. Run Frontend (Streamlit)

```bash
streamlit run app.py
```

---

## 💡 Example Queries

* “What fertilizer is best for rice crops?”
* “Today tomato price in India”
* “How to improve soil fertility?”
* “Weather forecast for farming this week”

---

## 🔍 Key Highlights

* Combines **RAG + Real-time Search** in a single system
* Demonstrates **tool-using AI agents**
* Implements **streaming UI like ChatGPT**
* Designed for **real-world agricultural use cases**

---

## ⚠️ Limitations

* Streaming is simulated (character-by-character)
* Depends on external APIs (Gemini, Tavily)
* Vector database must be pre-built or included

---

## 🔮 Future Improvements

* 🌍 Multilingual support (Telugu, Hindi)
* 🎤 Voice input for farmers
* ⚡ True token-level streaming
* ☁️ Cloud deployment (Railway)
* 📱 Mobile-friendly UI

---

## 👨‍💻 Author

Built as a **resume-ready AI project** demonstrating:

* RAG pipelines
* AI agents with tools
* Full-stack AI application (API + UI)

---

## 🎯 Why This Project Matters

This project demonstrates the ability to:

* Build **end-to-end AI systems**
* Integrate **LLMs with external tools**
* Design **real-world solutions using Generative AI**

---

⭐ If you found this useful, consider giving it a star!
