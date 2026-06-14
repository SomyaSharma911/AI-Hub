# Proxima Secure AI Hub: A Multithreaded Local Model Portal

Proxima Secure AI Hub is a lightweight, production-grade local AI dashboard designed to distribute local LLM endpoints securely over the public internet. Built entirely on top of Python's native networking stack, it features a custom cyberpunk web interface that allows authenticated users to seamlessly swap between various specialized open-source models running locally on a host machine via Ollama.

---

## 🚀 Key Architectural Features

### 1. High-Concurrency Threaded Core
Standard Python HTTP servers process requests on a single isolated thread, which means long model processing execution blocks freeze the port loop for everyone else. Proxima resolves this by leveraging a `ThreadingTCPServer` pipeline. Every incoming user prompt spawns an independent, sandboxed background thread, enabling multiple friends to query the models simultaneously without connection bottlenecks.

### 2. Autonomous Failover Pipeline (Error-Proofing)
To ensure 100% web application uptime, the backend acts as a proxy with built-in graceful degradation loops. If a specialized model encounters an Out-Of-Memory (OOM) exception or a hardware VRAM lockup on the host machine, the backend catches the failure instantly and routes the user's prompt to a secondary backup model (e.g., Llama 3.1) within milliseconds. The front-end interface labels remain unchanged, shielding the user from the system fallback entirely.

### 3. Stateful Context Memory & Local Storage Sync
By default, standard model APIs are stateless. Proxima introduces long-term conversation tracking by appending rolling dialogue structures (up to the last 15 exchanges) directly into an automated JSON database. Upon successful login, the interface triggers a hardware browser `localStorage` hook to map context variables, rebuilding past user conversation timelines instantly even after page reloads or device crashes.

### 4. Divided Data Management Layout
System metrics and footprints are split across two separate tracking files for clear monitoring transparency:
* `user_registry.json`: Stores user profile database tables containing unique handles and password credentials.
* `local_chat_database.json`: Stores explicit chat history transcripts mapped directly to user handle keys.

---

## 🛠️ System Workflow

1. **The Authorization Gate:** The user arrives at the dark cyberpunk overlay loop and registers or logs into a profile handle.
2. **Network Handshake:** The backend validates credentials against `user_registry.json`. On success, it reads `local_chat_database.json` to restore their session state.
3. **The Traffic Loop:** The user enters a prompt and picks an engine. The multi-threaded server passes the stitched context straight to the host machine's Ollama loop layout (`http://127.0.0.1:11434`).
4. **Log Sync:** The prompt and delivery outputs are logged cleanly into the internal files and a secondary `secret_ai_diary.txt` for audit transparency.

---

## 📦 Prerequisites & Setup Instructions

### 1. Clone the Architecture
Download this repository folder structure onto your local storage array (e.g., your `E:` drive partition).

### 2. Download Host AI Engines
Ensure you have [Ollama](https://ollama.com/) installed on the host machine. Open a terminal panel and pull down the required model configurations:
```cmd
ollama pull llama3.1
ollama pull qwen2.5-coder:7b
ollama pull deepseek-r1:7b
