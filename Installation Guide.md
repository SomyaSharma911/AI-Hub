# 🚀 Proxima Core Hub: Quick CMD Installation Guide



##### Open your standard Windows Command Prompt (cmd) or PowerShell and run the following blocks step-by-step to deploy the entire ecosystem:



##### Step 1: Automated Ollama Framework Installation

Run this command to download, configure, and install the core Ollama engine directly on your Windows environment automatically:



**PowerShell**

**irm https://ollama.com/install.ps1 | iex**





##### Step 2: Force-Purge Stale Background Processes

Ensure no lingering ghost tunnels, old script instances, or blocked network ports are hanging in your laptop's memory before starting the clean server:




```cmd
**DOS**

**taskkill /f /im ngrok.exe**

**taskkill /f /im python.exe**

**taskkill /f /im ollama.exe**
```




##### Step 3: Download the Local AI Model Stack

Fire up your newly installed local inference engine and download the three specialized text brains directly to your machine. Run these one after the other:


```cmd
**DOS**

**ollama pull llama3.1**

**ollama pull qwen2.5-coder:7b**

**ollama pull deepseek-r1:7b**

**(To verify that all three downloaded safely into your local registry, run ollama list)**
```




##### Step 4: Initialize and Deploy the Server Core

Navigate directly to the drive partition and folder path where you saved your auto\_agent.py script, then execute it to launch the portal:


```cmd
**DOS**

**:: Switch to your project drive partition**

**E:**



**:: Boot up the multithreaded network handler**

**python ai_agent.py**

```



##### 📋 Post-Deployment Operational Checklist

Once you execute python auto\_agent.py, the script automatically finalizes the deployment:



**Database Generation**: It scans your storage path and automatically writes clean, empty JSON sheets (user\_registry.json and local\_chat\_database.json) if they aren't already present.



**Network Binding**: It secures the local communication ring by binding explicitly to the IPv4 loopback address at 127.0.0.1:8080.



**Tunnel Initialization**: It spins up an independent background Ngrok worker thread, grabs the secure public web tunnel, and prints the unique web URL directly onto your console screen.



Copy that live public link, send it to your friends, and your encrypted, fault-tolerant AI workspace is fully active and ready for users!

