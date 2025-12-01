# 👔 The Virtual Boardroom: Autonomous C-Suite System

![Status](https://img.shields.io/badge/Status-Production%20Ready-success?style=flat-square)
![Architecture](https://img.shields.io/badge/Architecture-Multi--Agent-blueviolet?style=flat-square)
![Security](https://img.shields.io/badge/Security-Zero--Trust-red?style=flat-square)
![Stack](https://img.shields.io/badge/Tech-VertexAI%20%7C%20Pandas%20%7C%20Streamlit-blue?style=flat-square)

> **Kaggle AI Agents Capstone Submission 2025**
> **Track:** Enterprise Agents

---

## 📖 Executive Summary

### The Problem: The Loneliness of Leadership
Small business owners are the unsung heroes of the economy, yet they suffer from a crippling resource gap. They are drowning in raw data—spreadsheets of sales, endless receipts, and competitive noise—but they lack the time and expertise to turn that noise into signal. They don't need another chatbot that gives generic advice; they need a partner. They suffer from **"Analysis Paralysis,"** where the fear of making the wrong financial move stops them from making *any* move at all.

### The Solution: Your On-Demand Executive Team
The **Virtual Boardroom** is not just a tool; it is a **Level 3 Multi-Agent System** that acts as an autonomous, intelligent C-Suite. It effectively hires a Harvard-level CFO, a visionary CMO, and a decisive CEO to work for you 24/7.

It transforms the anxiety of a blank spreadsheet into the confidence of a strategic execution plan. By combining **Deterministic Code Execution** (for perfect math) with **Hyper-Local Market Research** (for cultural relevance), it delivers the one thing every business owner craves: **Clarity.**

---

## 🏗️ Cognitive Architecture

This system rejects the "monolithic LLM" approach. [cite_start]Instead, it implements a **Hierarchical Manager-Worker-Critic** pattern[cite: 2802]. This mimics a real corporate structure, ensuring that specialists do the work and leaders make the decisions.

![Architecture Diagram](architecture_diagram.png)

### 1. The Orchestration Layer (The Manager)
* **File:** `manager_agent.py`
* **Role:** The "Chief of Staff." It uses semantic classification to route user intent. It knows that a question about "Burn Rate" belongs to the CFO, while a question about "Viral Trends" belongs to the CMO. It ensures the right agent is awake at the right time.

### 2. The Worker Layer (The Specialists)
* **Agent A: The Virtual CFO (Financial Analyst)**
    * **The Superpower:** **Zero Hallucinations.** Unlike standard LLMs that struggle with arithmetic, this agent writes and executes **Pandas Python code** in a secure sandbox. [cite_start]It doesn't *guess* your profit margin; it *calculates* it to the penny[cite: 3337].
* **Agent B: The Virtual CMO (Market Researcher)**
    * **The Superpower:** **Contextual Awareness.** It accepts specific **Location** and **Currency** context. [cite_start]It doesn't just give generic marketing advice; it scouts *your* specific neighborhood in Mumbai, New York, or London to find hyper-local competitors and cultural trends[cite: 3483].

### 3. The Synthesis Layer (The CEO)
* **Role:** The Critic & Decision Maker.
* **The Superpower:** **Strategic Synthesis.** It takes the cold, hard numbers from the CFO (The Reality) and the ambitious ideas from the CMO (The Dream) and synthesizes them into a realistic, 3-point **Strategic Directive**. It ensures the business never spends money it doesn't have.

---

## 🚀 Key Technical Innovations

### 🛡️ 1. Zero-Trust Security Architecture
[cite_start]Adhering to **Whitepaper 5 (Prototype to Production)**, this system ensures no credentials are ever exposed[cite: 3003].
* **Local Development:** Credentials loaded via `.env` (gitignored).
* **Cloud Production:** Credentials injected via **Google Secret Manager** mount at runtime.
* **Docker Security:** A `.dockerignore` file explicitly blocks sensitive files from entering the container image.

### 🧠 2. Context Compaction (Memory Engineering)
[cite_start]To mitigate "Context Rot" in long strategic sessions[cite: 3511]:
* **Mechanism:** The `MemoryEngine` implements a **Rolling Summarization Protocol**.
* **Impact:** Instead of a linear sliding window, the system archives older strategic directives into a semantic history log. This allows the CEO to "remember" the strategy from last month's meeting without clogging the context window with outdated tokens.

### 🔭 3. Structured Observability
[cite_start]The system emits structured JSON logs (`observability.py`) for every cognitive step, providing a "Glass Box" view of the agent's reasoning chain (Input -> Tool Call -> Output)[cite: 2118].

---

## 🧪 Automated Evaluation ("LLM-as-a-Judge")

[cite_start]We validated the system using an automated evaluation pipeline (`eval.py`) against a "Golden Dataset" (Known Truth)[cite: 4613].

* **The Test:** Does the agent correctly calculate Net Profit ($2500) from a raw CSV and explain its methodology?
* **The Judge:** Gemini 2.5 Pro.

**Results:**
```text
🧪 STARTING AUTOMATED EVALUATION...
📋 Ground Truth Established: Net Profit is 2500.
🤖 Agent is running analysis...
📝 Agent Output: "I calculated this using Python code. Net Profit: 2500."
------------------------------
FINAL VERDICT: PASS
------------------------------

📂 Repository Structure
├── app.py                 # Main Orchestrator & UI Entry Point
├── manager_agent.py       # Routing & Delegation Logic
├── agent_workers.py       # Specialist Agents (CFO/CMO) & Custom Tools
├── memory_engine.py       # Persistence & Context Compaction
├── observability.py       # JSON Structured Logging
├── eval.py                # LLM-as-a-Judge QA Pipeline
├── Dockerfile             # Hardened container definition
└── requirements.txt       # Dependencies

🏃 How to Run

Option 1: Local Development
Clone the Repository
git clone [https://github.com/YOUR_USERNAME/virtual-boardroom.git](https://github.com/YOUR_USERNAME/virtual-boardroom.git)
cd virtual-boardroom

2. Install Dependencies
python -m venv venv
source venv/bin/activate  # or .\venv\Scripts\Activate on Windows
pip install -r requirements.txt

3. Configure Credentials Create a .env file in the root directory:
GCP_PROJECT_ID=your-project-id
GOOGLE_APPLICATION_CREDENTIALS=service_account.json

4. Launch
streamlit run app.py

Option 2: Docker / Cloud Run
# Build Container
gcloud builds submit --tag gcr.io/$(gcloud config get-value project)/virtual-boardroom

# Deploy with Secrets Mount (Zero-Trust)
gcloud run deploy virtual-boardroom \
  --image gcr.io/$(gcloud config get-value project)/virtual-boardroom \
  --set-secrets "/app/service_account.json=boardroom-key:latest"