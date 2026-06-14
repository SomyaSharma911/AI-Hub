import http.server
import socketserver
import json
import urllib.request
import subprocess
import time
import os

# CONFIGURATION
PORT = 8080
DIARY_FILE = r"E:\secret_ai_diary.txt"
CHAT_DB_FILE = r"E:\local_chat_database.json"
USER_REGISTRY_FILE = r"E:\user_registry.json"

# Global session matrices
LAST_ACTIVE_USER = None
SESSION_MEMORIES = {}
USER_REGISTRY = {}

def load_system_databases():
    """Synchronizes both the identity registers and dialogue maps from separate files on boot."""
    global SESSION_MEMORIES, USER_REGISTRY
    
    if os.path.exists(USER_REGISTRY_FILE):
        try:
            with open(USER_REGISTRY_FILE, "r", encoding="utf-8") as f:
                USER_REGISTRY = json.load(f)
            print(f"🔐 PLAIN-TEXT ENGINE: Loaded {len(USER_REGISTRY)} user credentials.")
        except Exception as e:
            print(f"⚠️ Identity registry read failure: {e}. Resetting buffer.")
            USER_REGISTRY = {}
    else:
        USER_REGISTRY = {}

    if os.path.exists(CHAT_DB_FILE):
        try:
            with open(CHAT_DB_FILE, "r", encoding="utf-8") as f:
                SESSION_MEMORIES = json.load(f)
            print(f"💾 CONVERSATION STORAGE: Loaded context logs cleanly.")
        except Exception as e:
            print(f"⚠️ Chat database read failure: {e}. Resetting buffer.")
            SESSION_MEMORIES = {}
    else:
        SESSION_MEMORIES = {}

def clean_ghost_processes():
    """Wipes out lingering background tunnels to prevent local port locking."""
    print("Core node spinning up. Sweeping stale environment processes...")
    try:
        subprocess.run(["taskkill", "/f", "/im", "ngrok.exe"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        time.sleep(1)
    except Exception:
        pass

def start_ngrok():
    """Launches the Ngrok tunnel automatically in the background and grabs the public link."""
    clean_ghost_processes()
    print("🚀 Launching automated secure multi-thread tunnel...")
    try:
        subprocess.Popen(["ngrok", "http", str(PORT)], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        time.sleep(3)
        
        with urllib.request.urlopen("http://127.0.0.1:4040/api/tunnels") as response:
            data = json.loads(response.read().decode())
            public_url = data['tunnels'][0]['public_url']
            print(f"\n==================================================")
            print(f"🌍 SECURE PLAIN-TEXT PORTAL IS ONLINE!")
            print(f"Share this link with your friends: {public_url}")
            print(f"==================================================\n")
    except Exception as e:
        print("⚠️ Couldn't start Ngrok automatically. Make sure ngrok is in your system path.")
        print(f"Error details: {e}\n")

class ThreadedHTTPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    """Handle requests in separate concurrent background threads smoothly."""
    daemon_threads = True

class AIAgentHandler(http.server.BaseHTTPRequestHandler):
    
    def do_OPTIONS(self):
        """Handles cross-origin security handshakes."""
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

    def do_GET(self):
        """Serves the user interface with an integrated dual-mode login/signup overlay gate."""
        self.send_response(200)
        self.send_header('Content-Type', 'text/html; charset=utf-8')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        
        html_response = """
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
            <title>Proxima Secure AI Hub</title>
            <style>
                :root {
                    --bg-dark: #07070c;
                    --bg-surface: rgba(15, 15, 25, 0.7);
                    --purple-glow: rgba(147, 51, 234, 0.4);
                    --border-glow: rgba(147, 51, 234, 0.15);
                    --text-main: #f3f4f6;
                    --text-muted: #9ca3af;
                    --accent-gradient: linear-gradient(135deg, #a855f7, #3b82f6);
                    --error-red: #ef4444;
                    --success-green: #10b981;
                }

                body {
                    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Arial, sans-serif;
                    background-color: var(--bg-dark);
                    background-image: 
                        linear-gradient(rgba(255, 255, 255, 0.015) 1px, transparent 1px),
                        linear-gradient(90deg, rgba(255, 255, 255, 0.015) 1px, transparent 1px);
                    background-size: 30px 30px;
                    color: var(--text-main);
                    margin: 0;
                    padding: 0;
                    display: flex;
                    justify-content: center;
                    align-items: center;
                    height: 100vh;
                    height: 100dvh;
                    box-sizing: border-box;
                    overflow: hidden;
                    overscroll-behavior-y: contain; 
                }

                .login-overlay {
                    position: fixed;
                    top: 0;
                    left: 0;
                    width: 100vw;
                    height: 100vh;
                    background: var(--bg-dark);
                    display: flex;
                    justify-content: center;
                    align-items: center;
                    z-index: 9999;
                }
                
                .login-card {
                    background: rgba(15, 15, 25, 0.85);
                    backdrop-filter: blur(25px);
                    border: 1px solid rgba(168, 85, 247, 0.3);
                    padding: 35px;
                    border-radius: 24px;
                    width: 90%;
                    max-width: 400px;
                    text-align: center;
                    box-shadow: 0 20px 50px rgba(0,0,0,0.6), 0 0 40px var(--purple-glow);
                }
                
                .login-card h2 { margin-top: 0; font-size: 1.6rem; background: var(--accent-gradient); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }
                .login-card p { color: var(--text-muted); font-size: 0.85rem; margin-bottom: 24px; }
                .hidden { opacity: 0; visibility: hidden; pointer-events: none; transition: opacity 0.4s; }

                .form-group {
                    display: flex;
                    flex-direction: column;
                    gap: 12px;
                    margin-bottom: 20px;
                }

                .gate-status-log {
                    font-size: 0.82rem;
                    min-height: 20px;
                    margin-bottom: 12px;
                    font-weight: 500;
                }

                .toggle-gate-link {
                    font-size: 0.8rem;
                    color: #c084fc;
                    cursor: pointer;
                    text-decoration: underline;
                    margin-top: 14px;
                    display: inline-block;
                }

                .app-wrapper {
                    width: 100%;
                    max-width: 720px;
                    height: 100vh;
                    height: 100dvh;
                    display: flex;
                    flex-direction: column;
                    background: var(--bg-surface);
                    backdrop-filter: blur(20px);
                }

                .navbar {
                    padding: 16px 24px;
                    display: flex;
                    justify-content: space-between;
                    align-items: center;
                    border-bottom: 1px solid var(--border-glow);
                }
                
                .navbar-title {
                    font-size: 1.1rem;
                    font-weight: 700;
                    background: var(--accent-gradient);
                    -webkit-background-clip: text;
                    -webkit-text-fill-color: transparent;
                }

                .model-selector {
                    background: rgba(0, 0, 0, 0.6);
                    border: 1px solid rgba(168, 85, 247, 0.4);
                    color: #c084fc;
                    padding: 6px 12px;
                    border-radius: 12px;
                    font-size: 0.8rem;
                    font-weight: 600;
                    outline: none;
                    cursor: pointer;
                }

                .conversation-stream {
                    flex: 1;
                    padding: 28px;
                    overflow-y: auto;
                    display: flex;
                    flex-direction: column;
                    gap: 26px;
                    scrollbar-width: none;
                }
                .conversation-stream::-webkit-scrollbar { display: none; }

                .bubble-row { display: flex; flex-direction: column; width: 100%; }
                .bubble-meta { font-size: 0.72rem; font-weight: 600; color: var(--text-muted); margin-bottom: 6px; text-transform: uppercase; letter-spacing: 0.8px; }
                .bubble-text { max-width: 82%; padding: 14px 18px; border-radius: 14px; font-size: 0.95rem; line-height: 1.55; word-wrap: break-word; white-space: pre-wrap; }

                .incoming { align-items: flex-start; }
                .incoming .bubble-text { background: rgba(255, 255, 255, 0.03); border: 1px solid var(--border-glow); }
                .incoming .bubble-meta { color: #a855f7; }

                .outgoing { align-items: flex-end; }
                .outgoing .bubble-text { background: var(--accent-gradient); color: #ffffff; }

                .action-tray { padding: 24px; }
                .input-wrapper { display: flex; align-items: center; background: rgba(0, 0, 0, 0.4); border: 1px solid var(--border-glow); border-radius: 16px; padding: 8px 10px 8px 18px; gap: 12px; }
                .input-wrapper.gate-input { padding: 4px 10px 4px 18px; border-radius: 12px; border: 1px solid rgba(255,255,255,0.08); }
                input { flex: 1; background: none; border: none; color: var(--text-main); font-size: 0.98rem; padding: 8px 0; }
                input:focus { outline: none; }
                button { background: var(--accent-gradient); color: #ffffff; border: none; height: 40px; padding: 0 22px; border-radius: 12px; font-weight: 600; cursor: pointer; }
                button.gate-btn { height: 44px; width: 100%; border-radius: 12px; margin-top: 5px; }

                .clean-loader { display: flex; gap: 5px; padding: 6px 0; align-items: center; }
                .clean-loader div { width: 6px; height: 6px; background-color: #a855f7; border-radius: 50%; animation: pulse 1.2s infinite ease-in-out both; }
                @keyframes pulse { 0%, 80%, 100% { transform: scale(0.4); opacity: 0.2; } 40% { transform: scale(1.1); opacity: 1; } }

                @media (min-width: 601px) {
                    body { padding: 30px 20px; }
                    .app-wrapper { height: 88vh; border: 1px solid var(--border-glow); border-radius: 24px; box-shadow: 0 30px 70px rgba(0, 0, 0, 0.8), 0 0 40px var(--purple-glow); }
                }
            </style>
        </head>
        <body>

            <div class="login-overlay" id="identityGate">
                <div class="login-card">
                    <h2 id="gateTitle">AUTHENTICATE SYSTEM</h2>
                    <p id="gateDesc">Provide your secure verification codes to link your cloud node session.</p>
                    
                    <div class="form-group">
                        <div class="input-wrapper gate-input">
                            <input type="text" id="identityInput" placeholder="Username Handle..." onkeypress="if(event.key === 'Enter') executeGateAction()">
                        </div>
                        <div class="input-wrapper gate-input">
                            <input type="password" id="passwordInput" placeholder="Password Signature..." onkeypress="if(event.key === 'Enter') executeGateAction()">
                        </div>
                    </div>
                    
                    <div class="gate-status-log" id="gateStatus"></div>
                    <button class="gate-btn" onclick="executeGateAction()" id="gateBtn">Access Engine</button>
                    
                    <div class="toggle-gate-link" onclick="toggleGateMode()" id="gateToggleLink">Need to establish a new profile handle? Register here</div>
                </div>
            </div>

            <div class="app-wrapper">
                <div class="navbar">
                    <div class="navbar-title" id="navUser">SECURE CORE</div>
                    <select class="model-selector" id="modelEngineSelect" onchange="updatePlaceholder()">
                        <option value="llama3.1">Llama 3.1 (Text Main)</option>
                        <option value="qwen2.5-coder:7b">Qwen 2.5 Coder (Software Lab)</option>
                        <option value="deepseek-r1:7b">DeepSeek-R1 (Logic Core)</option>
                    </select>
                </div>
                
                <div class="conversation-stream" id="streamViewport"></div>
                
                <div class="action-tray">
                    <div class="input-wrapper">
                        <input type="text" id="msgInput" placeholder="Message assistant..." onkeypress="if(event.key === 'Enter') dispatchMessage()">
                        <button onclick="dispatchMessage()">Send</button>
                    </div>
                </div>
            </div>

            <script>
                let clientName = "";
                let isRegisterMode = false;
                
                window.onload = function() {
                    const cachedHandle = localStorage.getItem("proxima_user_handle");
                    if (cachedHandle) {
                        document.getElementById('identityInput').value = cachedHandle;
                        document.getElementById('passwordInput').focus();
                    } else {
                        document.getElementById('identityInput').focus();
                    }
                };

                function toggleGateMode() {
                    isRegisterMode = !isRegisterMode;
                    const title = document.getElementById('gateTitle');
                    const desc = document.getElementById('gateDesc');
                    const btn = document.getElementById('gateBtn');
                    const link = document.getElementById('gateToggleLink');
                    const status = document.getElementById('gateStatus');
                    
                    status.innerText = "";
                    document.getElementById('passwordInput').value = "";
                    
                    if(isRegisterMode) {
                        title.innerText = "PROXIMA SIGN UP";
                        desc.innerText = "Create an un-hashed root profile handle. Remember your password signature code.";
                        btn.innerText = "Register & Mount Node";
                        link.innerText = "Already have an account? Run terminal verification login";
                    } else {
                        title.innerText = "AUTHENTICATE SYSTEM";
                        desc.innerText = "Provide your secure verification codes to link your cloud node session.";
                        btn.innerText = "Access Engine";
                        link.innerText = "Need to establish a new profile handle? Register here";
                    }
                }

                function updatePlaceholder() {
                    const selectedModel = document.getElementById('modelEngineSelect').value;
                    const field = document.getElementById('msgInput');
                    if (selectedModel === "deepseek-r1:7b") {
                        field.placeholder = "Enter deep mathematical or reasoning tasks...";
                    } else if (selectedModel === "qwen2.5-coder:7b") {
                        field.placeholder = "Enter coding tasks, scripting requests, or bugs...";
                    } else {
                        field.placeholder = "Message assistant...";
                    }
                }

                async function executeGateAction() {
                    const user = document.getElementById('identityInput').value.trim();
                    const pwd = document.getElementById('passwordInput').value.trim();
                    const status = document.getElementById('gateStatus');
                    
                    if(!user || !pwd) {
                        status.style.color = "var(--error-red)";
                        status.innerText = "Both data vector fields are required.";
                        return;
                    }
                    
                    const targetEndpoint = isRegisterMode ? "/api/register" : "/api/login";
                    status.style.color = "var(--text-muted)";
                    status.innerText = "Connecting to handshake matrix...";
                    
                    try {
                        const res = await fetch(targetEndpoint, {
                            method: "POST",
                            headers: { "Content-Type": "application/json" },
                            body: JSON.stringify({ user: user, password: pwd })
                        });
                        const data = await res.json();
                        
                        if(data.status === "success") {
                            status.style.color = "var(--success-green)";
                            status.innerText = isRegisterMode ? "Profile established! Initializing matrix..." : "Verified! Syncing session arrays...";
                            
                            clientName = user.toLowerCase();
                            localStorage.setItem("proxima_user_handle", user);
                            
                            setTimeout(() => {
                                document.getElementById('navUser').innerText = user.toUpperCase();
                                document.getElementById('identityGate').classList.add('hidden');
                                renderChatLogs(data.history);
                            }, 800);
                        } else {
                            status.style.color = "var(--error-red)";
                            status.innerText = data.message;
                        }
                    } catch(e) {
                        status.style.color = "var(--error-red)";
                        status.innerText = "Handshake dropped by network node.";
                    }
                }

                function renderChatLogs(history) {
                    if (history && history.length > 0) {
                        history.forEach(msg => {
                            if (msg.role === "user") {
                                renderBubble(msg.content, 'outgoing', clientName);
                            } else {
                                renderBubble(msg.content, 'incoming', 'AI Engine System');
                            }
                        });
                        renderBubble("Welcome back. Security parameters passed. Transaction history mounted securely.", "incoming", "AI Engine Control");
                    } else {
                        renderBubble("Profile session initialized safely under handle [ " + clientName.toUpperCase() + " ]. Encryption layers aligned.", "incoming", "AI Engine Control");
                        renderBubble("I am here to help. Feel free to use this secure workspace to vent out any stress or process your thoughts.", "incoming", "AI Companion");
                    }
                    document.getElementById('msgInput').focus();
                }

                async function dispatchMessage() {
                    const field = document.getElementById('msgInput');
                    const text = field.value.trim();
                    if(!text) return;

                    const selectedModel = document.getElementById('modelEngineSelect').value;
                    field.value = '';
                    renderBubble(text, 'outgoing', clientName);

                    const loaderId = 'load-' + Date.now();
                    const loaderHtml = `<div class="clean-loader"><div></div><div></div><div></div></div>`;
                    
                    let bubbleLabel = "AI Companion";
                    if(selectedModel === "qwen2.5-coder:7b") bubbleLabel = "AI Coder Lab";
                    if(selectedModel === "deepseek-r1:7b") bubbleLabel = "AI Logic Core";

                    renderBubble(loaderHtml, 'incoming', bubbleLabel, loaderId);

                    try {
                        const res = await fetch(window.location.href, {
                            method: 'POST',
                            headers: { 'Content-Type': 'application/json' },
                            body: JSON.stringify({ prompt: text, name: clientName, model: selectedModel })
                        });
                        const data = await res.json();
                        document.getElementById(loaderId).innerText = data.answer;
                    } catch (e) {
                        document.getElementById(loaderId).innerText = 'The secure routing pipeline dropped.';
                    }
                }

                function renderBubble(content, direction, label, elementId = null) {
                    const viewport = document.getElementById('streamViewport');
                    const row = document.createElement('div');
                    row.className = 'bubble-row ' + direction;
                    const meta = document.createElement('div');
                    meta.className = 'bubble-meta';
                    meta.innerText = label;
                    const bubble = document.createElement('div');
                    bubble.className = 'bubble-text';
                    if(elementId) bubble.id = elementId;
                    bubble.innerHTML = content;
                    row.appendChild(meta);
                    row.appendChild(bubble);
                    viewport.appendChild(row);
                    viewport.scrollTop = viewport.scrollHeight;
                }
            </script>
        </body>
        </html>
        """
        self.wfile.write(html_response.encode('utf-8'))

    def do_POST(self):
        """Routes conversational requests via threaded processes or processes plain-text auth handshakes."""
        global LAST_ACTIVE_USER, SESSION_MEMORIES, USER_REGISTRY
        
        content_length = int(self.headers.get('Content-Length', 0))
        post_data = self.rfile.read(content_length)
        
        # 🔑 INTERCEPT ROUTE: Plain-Text Account Sign Up
        if self.path == "/api/register":
            try:
                payload = json.loads(post_data.decode('utf-8'))
                username = payload.get("user", "").strip().lower()
                password = payload.get("password", "").strip()
                
                if not username or not password:
                    raise ValueError("Fields empty.")
                
                if username in USER_REGISTRY:
                    response_body = json.dumps({"status": "error", "message": "Handle is already claimed by another user."})
                else:
                    # UPDATED: Saves credentials in 100% readable plain-text structure!
                    USER_REGISTRY[username] = {
                        "password": password,
                        "created_at": int(time.time())
                    }
                    with open(USER_REGISTRY_FILE, "w", encoding="utf-8") as f:
                        json.dump(USER_REGISTRY, f, indent=4)
                        
                    SESSION_MEMORIES[username] = []
                    with open(CHAT_DB_FILE, "w", encoding="utf-8") as f:
                        json.dump(SESSION_MEMORIES, f, indent=4)
                        
                    response_body = json.dumps({"status": "success", "history": []})
            except Exception:
                response_body = json.dumps({"status": "error", "message": "Failed to create registration profile."})
                
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(response_body.encode('utf-8'))
            return

        # 🔑 INTERCEPT ROUTE: Plain-Text Password Login Matching
        if self.path == "/api/login":
            try:
                payload = json.loads(post_data.decode('utf-8'))
                username = payload.get("user", "").strip().lower()
                password = payload.get("password", "").strip()
                
                if username in USER_REGISTRY:
                    user_record = USER_REGISTRY[username]
                    # UPDATED: Direct string matching check
                    if user_record["password"] == password:
                        history = SESSION_MEMORIES.get(username, [])
                        response_body = json.dumps({"status": "success", "history": history})
                    else:
                        response_body = json.dumps({"status": "error", "message": "Invalid password signature code."})
                else:
                    response_body = json.dumps({"status": "error", "message": "Username handle does not exist."})
            except Exception:
                response_body = json.dumps({"status": "error", "message": "System auth handshake exception."})
                
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(response_body.encode('utf-8'))
            return

        # 📝 ROUTE: Standard Multimodal Chat Flow Execution Pipeline
        try:
            data = json.loads(post_data.decode('utf-8'))
            user_prompt = data.get("prompt", "")
            friend_name = data.get("name", "Unknown User").strip().lower()
            chosen_model = data.get("model", "llama3.1") 
        except Exception:
            user_prompt = ""
            friend_name = "unknown user"
            chosen_model = "llama3.1"

        if not user_prompt:
            self.send_response(400)
            self.end_headers()
            return

        if friend_name not in SESSION_MEMORIES:
            SESSION_MEMORIES[friend_name] = []
        
        SESSION_MEMORIES[friend_name].append({"role": "user", "content": user_prompt})
        
        if len(SESSION_MEMORIES[friend_name]) > 15:
            SESSION_MEMORIES[friend_name] = SESSION_MEMORIES[friend_name][-15:]

        compiled_context_prompt = ""
        for msg in SESSION_MEMORIES[friend_name]:
            if msg["role"] == "user":
                compiled_context_prompt += f"User: {msg['content']}\n"
            else:
                compiled_context_prompt += f"Assistant: {msg['content']}\n"
        compiled_context_prompt += "Assistant:"

        print(f"📩 Concurrent context packet firing [{chosen_model.upper()}] for verified user: {friend_name.upper()}")

        model_failover_pool = ["llama3.1", "qwen2.5-coder:7b", "deepseek-r1:7b"]
        if chosen_model in model_failover_pool:
            model_failover_pool.remove(chosen_model)
        model_failover_pool.insert(0, chosen_model)

        ai_answer = None
        actual_model_used = None

        for current_engine in model_failover_pool:
            try:
                ollama_url = "http://127.0.0.1:11434/api/generate"
                ollama_data = json.dumps({"model": current_engine, "prompt": compiled_context_prompt, "stream": False}).encode('utf-8')
                
                req = urllib.request.Request(ollama_url, data=ollama_data, headers={'Content-Type': 'application/json'})
                with urllib.request.urlopen(req, timeout=120) as response:
                    ollama_response = json.loads(response.read().decode('utf-8'))
                    ai_answer = ollama_response.get("response", "").strip()
                    
                    if ai_answer:
                        actual_model_used = current_engine
                        SESSION_MEMORIES[friend_name].append({"role": "assistant", "content": ai_answer})
                        
                        with open(CHAT_DB_FILE, "w", encoding="utf-8") as f:
                            json.dump(SESSION_MEMORIES, f, ensure_ascii=False, indent=4)
                        break
            except Exception as e:
                print(f"⚠️ CONCURRENCY MITIGATION: Node [{current_engine.upper()}] line error: {e}")
                continue

        if not ai_answer:
            ai_answer = "Core network pipelines are busy. Please resend your line in a moment."
            actual_model_used = "DISCONNECTED_ALL_NODES"

        try:
            with open(DIARY_FILE, "a", encoding="utf-8") as diary:
                if LAST_ACTIVE_USER != friend_name:
                    diary.write(f"\n==================================================\n")
                    diary.write(f"💬 CONNECTIONS HANDLED: {friend_name.upper()}\n")
                    diary.write(f"==================================================\n")
                    LAST_ACTIVE_USER = friend_name

                diary.write(f"  👉 [{friend_name} Asked]: {user_prompt}\n")
                diary.write(f"  🎯 [Requested Model]: {chosen_model.upper()}\n")
                diary.write(f"  🛡️ [Actual Processing Model]: {actual_model_used.upper()}\n")
                diary.write(f"  🤖 [Response]: {ai_answer}\n")
                diary.write(f"  --------------------------------------------------\n")
        except Exception as e:
            print(f"⚠️ Diary logging error: {e}")

        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps({"answer": ai_answer}).encode('utf-8'))

    def log_message(self, format, *args):
        return

if __name__ == "__main__":
    load_system_databases()
    start_ngrok()
    
    with ThreadedHTTPServer(("127.0.0.1", PORT), AIAgentHandler) as httpd:
        print(f"🤖 Plain-Text Certified Portal Armed on Port {PORT}...")
        try: 
            httpd.serve_forever()
        except KeyboardInterrupt: 
            print("\nShutting down system matrix.")