# CareerGuide AI

### AI-Powered Career, Job & Business Guidance Agent

CareerGuide AI is a cloud-hosted AI decision-support platform that helps
users explore careers, understand job requirements, identify skill gaps,
build learning roadmaps, research opportunities, and evaluate business
ideas.

> **CareerGuide AI guides decisions --- it doesn't make decisions for
> you.**

## 🚀 Live Demo

https://career-guide-ai-fpvk.onrender.com

## ✨ Features

-   **Career Mode** --- explore careers, required skills, learning
    paths, projects, internships, and interview preparation.
-   **Job Mode** --- analyze target roles, requirements, skill gaps,
    portfolio needs, interview preparation, and applications.
-   **Business Mode** --- explore business ideas, customers,
    competitors, value propositions, business models, costs, risks,
    validation, and growth.
-   **AI Web Research** --- retrieves current information when freshness
    matters.
-   **Personalized Guidance** --- uses education, experience, skills,
    goals, available time, learning style, and constraints.
-   **Specialist Agents** --- dedicated Career, Job, and Business
    specialist agents support the Manager Agent.
-   **Persistent Sessions** --- conversation history and user profiles
    are stored in Supabase/PostgreSQL.
-   **Multi-user Storage** --- user data is separated by user ID.
-   **Guardrails** --- input and output checks help keep responses
    focused and reduce overconfident answers.
-   **Model Fallback** --- an OpenRouter-based fallback path is
    available when the primary model path is unavailable.
-   **Instant Common Responses** --- greetings and exit commands are
    handled locally without an unnecessary model request.
-   **Cloud Deployment** --- deployed on Render for browser-based
    access.

## 🧠 How It Works

``` text
                         USER
                           │
                           ▼
                  ┌─────────────────┐
                  │   Web Frontend  │
                  │   HTML/CSS/JS   │
                  └────────┬────────┘
                           │
                           ▼
                  ┌─────────────────┐
                  │ FastAPI Backend │
                  └────────┬────────┘
                           │
                           ▼
                ┌──────────────────────┐
                │ CareerGuide Manager  │
                │       Agent          │
                └──────────┬───────────┘
                           │
             ┌─────────────┼─────────────┐
             ▼             ▼             ▼
       Web Research   User Profile   Specialist Agents
                         / DB             │
                                  ┌───────┼────────┐
                                  ▼       ▼        ▼
                               Career    Job    Business
                               Agent    Agent     Agent
                                  │       │        │
                                  └───────┼────────┘
                                          ▼
                                 Research + Reasoning
                                          │
                                          ▼
                                  Personalized Guidance
                                          │
                                          ▼
                                         USER
```

The Manager Agent remains responsible for the final user-facing response
while specialist agents handle bounded career, job, or business
subtasks.

## 🏗️ Architecture

### AI / Agent Layer

-   Python
-   OpenAI Agents SDK
-   Manager Agent
-   Career Specialist Agent
-   Job Specialist Agent
-   Business Specialist Agent
-   Function tools
-   Agent-as-tool orchestration
-   Web research
-   Input/output guardrails
-   Sessions
-   Tracing and evaluation support

### Backend

-   FastAPI
-   Uvicorn
-   REST API
-   Rate limiting
-   Error handling
-   Server-side API key management

### Data Layer

-   Supabase
-   PostgreSQL
-   Persistent user profiles
-   Persistent conversation sessions
-   Multi-user data separation

### Frontend

-   HTML
-   CSS
-   JavaScript
-   Browser Local Storage for a user identifier

### Deployment

-   GitHub
-   Render
-   Supabase

## 🔎 Research Flow

``` text
User Question
     │
     ▼
Does the question require fresh information?
     │
   ┌─┴─┐
   │   │
  No  Yes
   │   │
   │   ▼
   │  Web Research
   │   │
   │   ▼
   │  Gather Sources
   │   │
   │   ▼
   │  Compare / Reason
   │   │
   └───┼──────────────┐
       ▼              │
  Personalize        │
       │              │
       └──────┬───────┘
              ▼
       Actionable Answer
```

## 👥 Multi-Agent Design

``` text
                 Manager Agent
                       │
          ┌────────────┼────────────┐
          ▼            ▼            ▼
   Career Specialist  Job       Business
                     Specialist  Specialist
```

The Manager Agent stays in control of the final conversation and can
call specialists as tools.

## 🛡️ Reliability & Guardrails

-   Input guardrails
-   Output guardrails
-   API rate limiting
-   Error handling
-   Model fallback handling
-   Environment-based secret management
-   Instant local responses for common commands
-   Persistent cloud storage
-   Production deployment

## 💾 User Data & Sessions

Each browser receives a persistent user identifier stored in browser
Local Storage.

The backend uses that identifier to associate the correct user profile
and conversation session in Supabase.

## 📁 Project Structure

``` text
AI-Career-Agent/
│
├── .venv/
├── .env
├── .gitignore
├── main.py
├── app.py
├── database.py
├── requirements.txt
│
├── Frontend/
│   ├── index.html
│   ├── script.js
│   └── style.css
│
└── data/
```

## ⚙️ Local Setup

### 1. Clone

``` bash
git clone git@github.com:hasnain1522/AI-Career-Agent.git
cd AI-Career-Agent
```

### 2. Virtual environment

``` bash
python -m venv .venv
```

Windows PowerShell:

``` powershell
.venv\Scriptsctivate
```

### 3. Install dependencies

``` bash
pip install -r requirements.txt
```

### 4. Environment variables

Create `.env`:

``` env
OPENAI_API_KEY=your_openai_api_key
OPENROUTER_API_KEY=your_openrouter_api_key
SUPABASE_URL=your_supabase_url
SUPABASE_KEY=your_supabase_key
```

**Never commit `.env` or API keys.**

### 5. Run

``` bash
uvicorn app:app --reload
```

Open:

``` text
http://127.0.0.1:8000
```

## 🧪 Validation

``` powershell
python -m py_compile main.py app.py
```

``` powershell
python -c "from app import app; print('Production app loaded successfully.')"
```

## 🔐 Security Notes

-   API keys remain server-side.
-   Secrets are provided through environment variables.
-   `.env` should remain ignored by Git.
-   Provider keys are not exposed to the frontend.

## 📊 Production Status

  Component                        Status
  -------------------------------- ------------
  Web frontend                     ✅ Live
  FastAPI backend                  ✅ Live
  Supabase persistence             ✅ Enabled
  AI agent system                  ✅ Enabled
  Web research                     ✅ Enabled
  Specialist agents                ✅ Enabled
  Guardrails                       ✅ Enabled
  Model fallback                   ✅ Enabled
  Instant greeting/exit handling   ✅ Enabled
  Render deployment                ✅ Live

## 🧰 Technology Stack

  Category          Technologies
  ----------------- ------------------------------
  Language          Python
  AI Agents         OpenAI Agents SDK
  AI Models         OpenAI + OpenRouter fallback
  Research          Web search integration
  Backend           FastAPI, Uvicorn
  Database          Supabase, PostgreSQL
  Frontend          HTML, CSS, JavaScript
  Deployment        Render
  Version Control   Git, GitHub

## 🎯 Engineering Goals

CareerGuide AI was built to demonstrate practical AI engineering beyond
a basic chatbot:

1.  Agent orchestration
2.  Tool calling
3.  Web research
4.  Personalization
5.  Persistent sessions
6.  Multi-user architecture
7.  Guardrails
8.  Reliability and fallback handling
9.  API development
10. Cloud deployment

## 🔮 Future Improvements

-   Authentication and account management
-   Resume analysis
-   Interview simulation
-   Project recommendations
-   Job application tracking
-   Richer career/job data sources
-   Automated evaluation datasets
-   Monitoring and analytics
-   Additional specialist agents
-   Stronger production database security policies
-   Improved mobile UI

## 👨‍💻 Author

**Mohammed Hasnain**

CSE AI / ML Student and AI Engineering Enthusiast

GitHub: https://github.com/hasnain1522

## 📄 License

This project is currently maintained as a portfolio project.
