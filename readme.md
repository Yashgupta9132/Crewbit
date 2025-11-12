HR AI AGENT - Project Setup and Usage Guide

===========================================================================================================================
Prerequisites
===========================================================================================================================

1. Install the following software on your machine:

   - Python 3.11 or higher: https://www.python.org/downloads/
   - Node.js (LTS recommended) and npm: https://nodejs.org/
   - Ollama platform CLI: https://ollama.com/docs/install
     (Ensure Ollama CLI is added to your system PATH)

2. Confirm installations by running in Command Prompt or PowerShell:

   python --version
   node --version
   npm --version
   ollama --version

If any of these commands are not recognized, please install them or fix your PATH.

---

===========================================================================================================================
Project Structure Overview
===========================================================================================================================

HR-AI-AGENT/
│
├── backend/
│   ├── main.py                 # FastAPI backend, main AI API logic
│   ├── requirements.txt        # Python dependencies for backend
│   ├── hr_agent.py             # LLM officer logic, answer generator
│   ├── sentiment.py            # Sentiment analysis pipeline
│   ├── vectorstore.py          # Vector store utility functions
│   ├── ...                     # Other backend Python files/modules
│
├── frontend/
│   ├── package.json            # React app dependencies
│   ├── package-lock.json       # Locked versions for npm install
│   ├── public/                 # Public assets (index.html, favicon, etc.)
│   ├── src/                    # All React source code (components, pages, API logic)
│   ├── README.md               # Frontend-specific README (optional)
│   └── ...                     # Any other frontend files
│
├── setup.bat                   # Windows setup script: installs dependencies & Ollama models
├── README.txt                  # Main project setup & usage instructions (this file)
└── ...                         # (Add other top-level files here if needed)


---

===========================================================================================================================
Setup Instructions
===========================================================================================================================

1. Open Command Prompt or PowerShell in the project root folder (HR-AI-AGENT/).

2. Run the setup script:

   .\setup.bat    (if using PowerShell)
   OR
   setup.bat      (if using Command Prompt)

3. What the script does:
   - Verifies if Ollama CLI is installed.
   - Pulls the required Ollama models:
         - llama3.2
         - mxbai-embed-large
   - Creates a Python virtual environment in `backend/venv`.
   - Installs all Python backend dependencies.
   - Installs Node.js frontend dependencies.

4. If prompted with any errors (like missing Ollama CLI), follow the instructions in the terminal to fix and rerun the script.

---

===========================================================================================================================
Running the Backends and Frontend
===========================================================================================================================

### 1. FastAPI Backend Server (main AI API)

   a. Activate backend virtual environment:

      cd backend
      call venv\Scripts\activate

   b. Run the FastAPI server:

      uvicorn main:app --reload --port 9001

   c. The AI backend will be running at: http://localhost:9001

---

### 2. Express Backend with MongoDB 

   a. Go to backend directory:

      cd backend

   b. Run the Mongo/Node server:

      npm run dev

   c. The Node backend will be running at: http://localhost:8000

---

### 3. Frontend (React App)

   a. In a new terminal window, start the frontend:

      cd frontend
      npm start

   b. The React app will open automatically at: http://localhost:3000

---

===========================================================================================================================
Using the Application
===========================================================================================================================

- Access the app frontend at http://localhost:3000
- Use the navigation buttons to:
   - Upload multiple HR policy PDF files on the "HR Policy Upload" page.
   - Ask questions on the "Employee Query" page and see chat history.
- Uploaded PDFs are stored in `backend/policy_uploads/`
- Embedded data (vector store) is saved in `backend/chrome_langchain_db/`

---

===========================================================================================================================
Ollama Model Management Notes
===========================================================================================================================

- Ollama platform and required models must be installed on the same machine running the backend(s).
- These models are reused by the backend to embed and respond to queries.
- You can list installed models by running:

     ollama list

- To update or add new models, use:

     ollama pull <model-name>

- For more info, visit: https://ollama.com/docs

---

===========================================================================================================================
Stopping the Application
===========================================================================================================================

- Stop any backend (FastAPI or Node) by pressing Ctrl+C in its terminal.
- Stop frontend by pressing Ctrl+C in its terminal.

---

Thank you for using the HR AI Agent!
