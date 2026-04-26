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

## 📂 Project Structure (Production)

```text
project/
│
├── backend/
│   ├── main.py
│   ├── chroma_db/
│   ├── requirements.txt
│   ├── runtime.txt
│
├── frontend/
│   ├── app.py
│   ├── requirements.txt
│
├── README.md
```

---

## ⚙️ Local Setup

### 1. Clone Repository

```bash
git clone <your-repo-url>
cd project
```

### 2. Install Backend Dependencies

```bash
cd backend
pip install -r requirements.txt
```

### 3. Set Environment Variables

Create `.env` inside `backend/`:

```env
GOOGLE_API_KEY=your_google_api_key
TAVILY_API_KEY=your_tavily_api_key
```

### 4. Run Backend

```bash
uvicorn main:app --reload
```

### 5. Run Frontend

```bash
cd ../frontend
pip install -r requirements.txt
streamlit run app.py
```

---

# 🚀 Production Deployment

## 🔹 Backend Deployment (Render)

1. Push repo to GitHub
2. Go to Render → **New Web Service**
3. Connect repo

### Settings:

* **Root Directory:** `backend`
* **Build Command:**

```bash
pip install -r requirements.txt
```

* **Start Command:**

```bash
uvicorn main:app --host 0.0.0.0 --port 10000
```

### Add Environment Variables:

```env
GOOGLE_API_KEY=xxxx
TAVILY_API_KEY=xxxx
HF_TOKEN=xxxx (optional)
```

👉 After deploy:

```
https://your-backend.onrender.com/ask
```

---

## 🔹 Frontend Deployment (Streamlit Cloud)

1. Go to Streamlit Cloud
2. Connect same GitHub repo
3. Select file:

```
frontend/app.py
```

### Update API URL in `app.py`:

```python
API_URL = "https://your-backend.onrender.com/ask"
```

---

## 💡 Example Queries

* “What fertilizer is best for rice crops?”
* “Today tomato price in India”
* “How to improve soil fertility?”
* “Weather forecast for farming this week”

---

## 🔍 Key Highlights

* Combines **RAG + Real-time Search**
* Demonstrates **tool-using AI agents**
* Implements **streaming UI like ChatGPT**
* Designed for **real-world agricultural use cases**

---

## ⚠️ Limitations

* Streaming is simulated
* Depends on external APIs
* Vector database must be pre-built

---

## 🔮 Future Improvements

* 🌍 Multilingual support (Telugu, Hindi)
* 🎤 Voice input
* ⚡ True token streaming
* 📱 Mobile-friendly UI

---

## 👨‍💻 Author

Built as a **resume-ready AI project** demonstrating:

* RAG pipelines
* AI agents with tools
* Full-stack AI system

---

## 🎯 Why This Project Matters

* Shows **end-to-end AI system design**
* Demonstrates **real-world GenAI usage**
* Combines **LLMs + tools + APIs**

---

⭐ Star this repo if you found it useful!
