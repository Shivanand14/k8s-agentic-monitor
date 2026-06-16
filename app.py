import os
import json
import time
from typing import Annotated, TypedDict
from pydantic import BaseModel, Field
from langchain_core.messages import AnyMessage, SystemMessage, HumanMessage
from langchain_nvidia_ai_endpoints import ChatNVIDIA
from langgraph.graph import StateGraph, START, END

# Ensure API Key is available
if "NVIDIA_API_KEY" not in os.environ:
    raise ValueError("Please set your NVIDIA_API_KEY environment variable!")

# ==========================================
# 1. THE SIMULATED KUBERNETES LAYER
# ==========================================
# Since you don't have K8s locally, this file acts as your real-time cluster engine.
LOG_FILE = "simulated_k8s_logs.txt"

def generate_mock_kubernetes_logs():
    """Simulates a live Kubernetes pod slowly suffering from an Out-Of-Memory (OOM) leak."""
    logs = [
        "INFO 2026-06-14 10:00:01 pod/payment-api-7f89d - Application started successfully.",
        "INFO 2026-06-14 10:01:15 pod/payment-api-7f89d - Connection pool initialized to DB cluster.",
        "WARNING 2026-06-14 10:02:45 pod/payment-api-7f89d - Memory consumption exceeded 85% of limit.",
        "WARNING 2026-06-14 10:03:10 pod/payment-api-7f89d - Garbage Collection failed to reclaim heap memory.",
        "CRITICAL 2026-06-14 10:04:00 pod/payment-api-7f89d - High memory stress. Garbage Collection loop saturated.",
        "CRITICAL 2026-06-14 10:04:12 pod/payment-api-7f89d - System kernel warning: low memory footprint detected."
    ]
    with open(LOG_FILE, "w") as f:
        for line in logs:
            f.write(line + "\n")
    print("[Environment] Mock Kubernetes live log files generated successfully.")

# Initialize the mock cluster logs
generate_mock_kubernetes_logs()


# ==========================================
# 2. DEFINING THE AGENT'S TOOLS
# ==========================================
def read_kubernetes_logs() -> str:
    """Tool: Reads the real-time log data stream from the cluster."""
    if os.path.exists(LOG_FILE):
        with open(LOG_FILE, "r") as f:
            return f.read()
    return "Error: Unable to connect to K8s log stream data provider."

def run_simulated_kubectl_command(command: str) -> str:
    """Tool: Runs diagnostic read commands inside the cluster."""
    if "describe pod" in command.lower():
        return (
            "Pod Name: payment-api-7f89d\n"
            "Namespace: production\n"
            "Limits: Memory: 512Mi, CPU: 200m\n"
            "Requests: Memory: 256Mi, CPU: 100m\n"
            "Status: Running (Struggling Resource Allocations)"
        )
    return f"Command '{command}' executed successfully, but returned no special outputs."


# ==========================================
# 3. LANGGRAPH ARCHITECTURE & STATE
# ==========================================
class AgentState(TypedDict):
    """The memory dictionary passed between active steps in our LangGraph."""
    messages: list[AnyMessage]
    logs_content: str
    diagnostic_info: str
    requires_escalation: bool


# Initialize the ultra-fast NVIDIA NIM AI model
llm = ChatNVIDIA(model="meta/llama-3.1-70b-instruct", temperature=0.1)


# --- NODE 1: Ingest and Parse ---
def log_ingestion_node(state: AgentState) -> AgentState:
    print("\n[Node 1] Ingesting real-time streaming Kubernetes logs...")
    logs = read_kubernetes_logs()
    return {**state, "logs_content": logs}


# --- NODE 2: AI Diagnosis Brain ---
def ai_analysis_node(state: AgentState) -> AgentState:
    print("[Node 2] AI Agent analyzing log telemetry patterns via NVIDIA NIM...")
    
    system_prompt = (
        "You are an elite, proactive Site Reliability Engineer (SRE) Agent monitoring a Kubernetes cluster.\n"
        "Analyze the provided logs. Look for patterns indicating an impending system crash (e.g., memory leaks, disk pressure).\n"
        "Provide a concise summary and flag if a proactive notification is required."
    )
    
    human_prompt = f"Review these active logs:\n{state['logs_content']}"
    
    response = llm.invoke([
        SystemMessage(content=system_prompt),
        HumanMessage(content=human_prompt)
    ])
    
    # Simple algorithmic flag evaluation for the demo graph path logic
    requires_alert = "CRITICAL" in state['logs_content'] or "warning" in response.content.lower()
    
    # Store the analysis text in the state's message chain
    return {
        **state, 
        "messages": state.get("messages", []) + [response],
        "requires_escalation": requires_alert
    }


# --- NODE 3: Execute Proactive Alert Callouts ---
def notification_dispatcher_node(state: AgentState) -> AgentState:
    print("[Node 3] 🚨 CRITICAL PROACTIVE ANOMALY DETECTED! Dispatching high-priority operational alert...")
    
    # Extract the AI's analytical insight response text
    ai_insight = state["messages"][-1].content
    
    # Create a clean UI markdown payload layout that will stun the hackathon jury
    alert_payload = (
        "============ 🚨 KUBESENTRY PROACTIVE INCIDENT SUMMARY ============ \n"
        f"TARGET CLUSTER ID: prod-india-west-01\n"
        f"PREDICTED ROOT CAUSE: Impending Out-Of-Memory (OOMKilled) pod crash risk.\n"
        f"AI ANALYTICS DICTIONARY:\n{ai_insight}\n"
        "===================================================================\n"
    )
    print(alert_payload)
    return state


# ==========================================
# 4. BUILDING THE GRAPH EXECUTION WORKFLOW
# ==========================================
# Compile the workflow blueprint step mapping paths
workflow = StateGraph(AgentState)

# Add the functional code components to our processing grid nodes
workflow.add_node("IngestLogs", log_ingestion_node)
workflow.add_node("AnalyzeLogs", ai_analysis_node)
workflow.add_node("DispatchAlert", notification_dispatcher_node)

# Map relationships sequentially using clean design paths
workflow.add_edge(START, "IngestLogs")
workflow.add_edge("IngestLogs", "AnalyzeLogs")

# Conditional Router Logic: Decides whether to trigger an alert based on the AI state evaluation
def routing_condition(state: AgentState):
    if state["requires_escalation"]:
        return "DispatchAlert"
    return END

workflow.add_conditional_edges("AnalyzeLogs", routing_condition, {
    "DispatchAlert": "DispatchAlert",
    END: END
})
workflow.add_edge("DispatchAlert", END)

# Finalize compilation
app = workflow.compile()


# ==========================================
# 5. EXECUTION PIPELINE
# ==========================================
if __name__ == "__main__":
    print("Starting KubeSentry Engine demo workflow execution run loop...")
    initial_state: AgentState = {
        "messages": [],
        "logs_content": "",
        "diagnostic_info": "",
        "requires_escalation": False
    }
    
    # Run the agentic workflow pipeline instance
    app.invoke(initial_state)
