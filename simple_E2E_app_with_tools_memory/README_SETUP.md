# AI Agent with Chat History - Full Stack Application

## 🏗️ Architecture

This application consists of three main components:

1. **Agent with Chat History** (`agent_with_chat_history.py`) - LangChain agent with ConversationBufferMemory
2. **FastAPI Backend** (`app.py`) - REST API server providing `/ask` endpoint
3. **Streamlit UI** (`stremlist_ui.py`) - Web-based chat interface

## 🚀 How to Run

### Option 1: Run Everything Together (Recommended)
```bash
python run_full_app.py
```
This will start both the FastAPI backend and Streamlit UI automatically.

### Option 2: Run Components Separately (For Development)

#### Start Backend Server
```bash
python run_backend.py
```
- Backend will be available at: http://127.0.0.1:8000
- API documentation at: http://127.0.0.1:8000/docs

#### Start UI (In a separate terminal)
```bash
python run_ui.py
```
- UI will be available at: http://localhost:8501

### Option 3: Manual Commands

#### Backend:
```bash
uvicorn app:app --host 127.0.0.1 --port 8000 --reload
```

#### UI:
```bash
streamlit run stremlist_ui.py --server.port 8501
```

## 🔧 Configuration

### Environment Variables
Create a `.env` file with your API keys:

```env
OPENAI_API_KEY=your_openai_api_key_here
SERPER_API_KEY=your_google_serper_api_key_here
TAVILY_API_KEY=your_tavily_api_key_here
```

### Required Dependencies
Install all dependencies with:
```bash
pip install -r requirements.txt
```

## 🧪 Testing

Test the agent directly:
```bash
python agent_with_chat_history.py
```

Test chat history functionality:
```bash
python test_chat_history.py
```

## 📊 Features

- ✅ **Persistent Chat History** - Conversations are remembered across interactions
- ✅ **Web Search Tools** - DuckDuckGo, Google Serper, Tavily search
- ✅ **Academic Search** - ArXiv and Semantic Scholar integration  
- ✅ **RESTful API** - FastAPI backend with automatic documentation
- ✅ **Modern UI** - Streamlit-based chat interface
- ✅ **Real-time Updates** - Auto-reload during development

## 🔍 API Endpoints

### POST /ask
Send a question to the AI agent.

**Request:**
```json
{
  "question": "Your question here"
}
```

**Response:**
```json
{
  "history": [
    {
      "role": "human",
      "content": "Your question here", 
      "thread_id": "thread_1"
    },
    {
      "role": "ai",
      "content": "AI response here",
      "thread_id": "thread_1" 
    }
  ]
}
```

## 🛠️ Development

The application uses:
- **LangChain** for AI agent orchestration
- **ConversationBufferMemory** for chat history persistence
- **FastAPI** for the backend API
- **Streamlit** for the user interface
- **Pydantic** for data validation

## 📝 File Structure

```
├── agent_with_chat_history.py  # Main AI agent with memory
├── app.py                     # FastAPI backend server
├── stremlist_ui.py           # Streamlit frontend
├── tools.py                  # Search and utility tools
├── run_full_app.py           # Start everything
├── run_backend.py            # Start backend only
├── run_ui.py                 # Start UI only
├── test_chat_history.py      # Test chat memory
└── requirements.txt          # Dependencies
```