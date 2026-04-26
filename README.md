## 🌾 Farmer Assistant (RAG + AI Agent)

An AI-powered Farmer Assistant that provides accurate answers to agriculture-related questions by combining **local knowledge (RAG)** with **real-time web search**.

The system uses an intelligent AI agent to dynamically choose between a **vector database (Chroma)** and **web search (Tavily)**, then generates clear, simple responses using **Google Gemini**.

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

```text id="flow1"
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

```text id="struct1"
project/
│
├── backend/
│   ├── main.py
│   ├── build_vectorstore.py   # Script to create vector DB
│   ├── chroma_db/             # Persisted Chroma vector database
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

## ⚙️ Setup Instructions (Local)

### 1. Clone the Repository

```bash id="cmd1"
git clone <your-repo-url>
cd project
```

### 2. Install Backend Dependencies

```bash id="cmd2"
cd backend
pip install -r requirements.txt
```

### 3. Set Environment Variables

Create a `.env` file inside `backend/`:

```env id="env1"
GOOGLE_API_KEY=your_google_api_key
TAVILY_API_KEY=your_tavily_api_key
```

---

## 🧩 Build Vector Database (Important)

Before running the app, you need to create the vector database.

### Run:

```bash id="cmd3"
python build_vectorstore.py
```

👉 This will generate:

```text id="out1"
chroma_db/
```

---

### ⚠️ Embedding Model Choice

* ✅ **Best accuracy:**
  `sentence-transformers/all-mpnet-base-v2`

* ⚡ **Used in this project (for deployment):**
  `sentence-transformers/all-MiniLM-L6-v2`

### 💡 Why?

* `mpnet-base-v2` → better semantic understanding (more accurate retrieval)
* `MiniLM-L6-v2` → much faster, lighter, and suitable for cloud deployment

👉 For production systems with more resources, **mpnet is recommended**
👉 For fast deployment (like Render free tier), **MiniLM is used**

---

## ▶️ Run the Application

### Backend

```bash id="cmd4"
uvicorn main:app --reload
```

### Frontend

```bash id="cmd5"
cd ../frontend
pip install -r requirements.txt
streamlit run app.py
```

---

# 🚀 Production Deployment

## 🔹 Backend Deployment (Render)

1. Push code to GitHub
2. Go to Render → New Web Service
3. Connect repository

### Settings:

* **Root Directory:** `backend`
* **Build Command:**

```bash id="cmd6"
pip install -r requirements.txt
```

* **Start Command:**

```bash id="cmd7"
uvicorn main:app --host 0.0.0.0 --port $PORT
```

### Environment Variables:

```env id="env2"
GOOGLE_API_KEY=your_key
TAVILY_API_KEY=your_key
HF_HOME=/opt/render/.cache/huggingface
TRANSFORMERS_CACHE=/opt/render/.cache
```

---

## 🔹 Frontend Deployment (Streamlit Cloud)

1. Go to Streamlit Cloud
2. Connect GitHub repo
3. Select:

```text id="cmd8"
frontend/app.py
```

### Update API URL:

```python id="code1"
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

* Streaming is simulated (character-by-character)
* Depends on external APIs (Gemini, Tavily)
* First request may be slow due to model loading

---

## 🔮 Future Improvements

* 🌍 Multilingual support (Telugu, Hindi)
* 🎤 Voice input for farmers
* ⚡ True token-level streaming
* ☁️ GPU-based deployment for faster inference
* 📱 Mobile-friendly UI

---

## 👨‍💻 Author

Built as a **resume-ready AI project** demonstrating:

* RAG pipelines
* AI agents with tools
* Full-stack AI application

---

## 🎯 Why This Project Matters

This project demonstrates the ability to:

* Build **end-to-end AI systems**
* Integrate **LLMs with external tools**
* Design **real-world solutions using Generative AI**

---

⭐ If you found this useful, consider giving it a star!
