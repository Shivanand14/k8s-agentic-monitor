# KubeSentry Monitor (k8s-agentic-monitor)

An AI-powered agentic monitoring tool designed to ingest real-time streaming Kubernetes logs, analyze telemetry patterns via NVIDIA NIM, and proactively catch operational infrastructure anomalies before they cause service downtime.

## Features
* **Real-time Log Ingestion**: Simulates or connects to streaming live cluster logs.
* **NVIDIA NIM Intelligence**: Employs deep telemetry processing to extract system context.
* **Proactive Out-of-Memory (OOM) Analysis**: Predicts impending `OOMKilled` pod crashes.
* **Automated Root Cause Diagnosis**: Identifies memory leaks, disk pressure, and cascading system risks.

## Tech Stack
* **Language**: Python 3.10+
* **Framework**: LangChain (Core), Pydantic
* **AI Model Engine**: NVIDIA AI Endpoints (NIM)
* **Infrastructure Interface**: Kubernetes CLI (`kubectl`)

## Installation & Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com
   cd k8s-agentic-monitor
   ```

2. **Set up a Virtual Environment:**
   ```powershell
   python -m venv venv
   .\venv\Scripts\Activate.ps1
   ```

3. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure Your API Key:**
   ```powershell
   \$env:NVIDIA_API_KEY="your-nvapi-key-here"
   ```

## 🖥️ Usage
Execute the primary workflow loop with:
```bash
python app.py
```
