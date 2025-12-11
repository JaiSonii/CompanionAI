# Companion AI: Memory & Personality Engine

This project is a modular AI backend designed to build sophisticated Companion AIs. It features a **Memory Extraction Module** that identifies user preferences and emotional patterns, and a **Personality Engine** that adapts the AI's tone (e.g., Calm Mentor, Witty Friend) while managing unique user sessions.

## 🚀 Features

* **Structured Memory Extraction**: Analyzes chat history to extract:
    * **User Preferences**: Likes, dislikes, and behavioral choices.
    * **Emotional Patterns**: Recurring moods and triggers.
    * **Core Facts**: Long-term biographical data and goals.
* **Dynamic Personality Engine**: Switches between distinct personas (e.g., *Therapist*, *Tech Bro*, *Storyteller*) while maintaining conversation context.
* **Multi-User Session Management**: Scalable architecture that isolates conversation history and context for multiple concurrent users via `user_id`.
* **Context Management**: Handles context windows and auto-summarizes older messages to maintain coherence without exceeding token limits.
* **Tech Stack**: Built with **FastAPI**, **LangChain**, and **Google Gemini (Flash 2.5)**.

## 📂 Project Structure

```text
.
├── app
│   ├── config.py                 # Configuration & Environment variables
│   ├── services
│   │   ├── base_ai.py            # Base abstract class for AI services
│   │   ├── chat_analysis         # Logic for extracting structured memory
│   │   ├── personality_engine    # Logic for persona-based chat
│   │   ├── summarizer            # Logic for summarizing conversation history
│   │   └── context.py            # Context window manager
├── main.py                       # FastAPI entry point
├── demo.py                       # Script to demonstrate capabilities
├── pyproject.toml                # Dependencies
└── README.md
````

## 🛠️ Installation & Setup

### 1\. Clone the Repository

```bash
git clone https://github.com/JaiSonii/CompanionAI
cd <repo-name>
```

### 2\. Set up Environment

Create a `.env` file in the root directory with your Google Gemini API Key.

```ini
GOOGLE_API_KEY=your_google_api_key_here
CONTEXT_WINDOW=5
CHAT_MODEL=gemini-2.5-flash
```

### 3\. Install Dependencies



```bash
pip install -r requirements.txt
# OR
pip install .
# OR simply if you have uv
uv run main.py # No need for starting the server, will start
```

## 🏃‍♂️ Usage

### Running the Server

Start the FastAPI server:

```bash
uvicorn main:app --reload
```

The API will be available at `http://localhost:8000`.

### API Endpoints

#### 1\. Chat with Persona (`POST /chat`)

Interacts with the AI. Includes `user_id` to maintain a persistent session.

**Request:**

```json
{
  "user_id": "user_123", 
  "message": "I'm feeling overwhelmed with my project.",
  "persona": "calm_mentor"
}
```

*Note: If "user\_123" sends a subsequent message with a different persona (e.g., "witty\_friend"), the AI will switch tones but remember the previous conversation context.*

**Available Personas**:
`calm_mentor`, `witty_friend`, `therapist`, `professor`, `tech_bro`, `storyteller`, `minimalist`, `motivational_coach`.

#### 2\. Analyze Memory (`POST /analyze`)

Extracts structured insights from a batch of chat messages.

**Request:**

```json
{
  "history": [
    {"role": "user", "content": "I love Python but hate Java."},
    {"role": "ai", "content": "Why is that?"},
    {"role": "user", "content": "Java is too verbose. Also, I get anxious before interviews."}
  ]
}
```

## 🔄 Scalability & Session Management

This system is designed to function as a fully capable chatbot backend, supporting **multiple concurrent user sessions**.

  * **Multi-User Architecture**: The server implements an in-memory session manager that maps unique `user_id`s to distinct instances of the `PersonalityEngine`.
  * **Isolated Contexts**: Every user maintains their own conversation history, context window, and summarization state. User A's conversation about "coding" will never bleed into User B's conversation about "cooking."
  * **Stateful Design**: By keeping the `Context` object alive within the server instance, the AI remembers short-term interactions instantly without needing expensive database queries for every turn.

## 🧪 Running the Demo

A demonstration script is included to showcase Memory Extraction and Personality comparison.

1.  Ensure the server is running (`uvicorn main:app`).
2.  Run the demo script:

<!-- end list -->

```bash
python demo.py
```