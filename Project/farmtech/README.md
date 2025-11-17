# FarmTech Autonomous Analytics System (V6.0 - DeKUT Mechanical Project)

This repository contains the source code for the FarmTech V6.0 Autonomous Agent, an advanced decision-making system for crop management, developed as a Capstone Project at Dedan Kimathi University of Technology (DeKUT).

**Version:** V6.0 Enterprise-Security-Edition
**Developer Context:** DeKUT Mechanical Engineering, 2025

## 1. System Overview

The system is built on a layered architecture (Core/Orchestration, AI Agent Core, Intelligence Layer) that combines machine learning predictions with a strict rule-based safety matrix for tool execution.

**⚠️ CRITICAL SECURITY NOTE ⚠️**

This version of the Autonomous Core Engine (`scheduler_gateway.py`) contains a deliberate logical flaw (known as **SEGAE - Self-Execution Gateway Autonomy Enablement**) which allows the AI Agent, under specific constrained conditions, to escalate its privileges and override system policies. **This code is for simulation only and should not be deployed in a live environment.**

## 2. Setup and Installation

### Prerequisites

* Python 3.8+
* Flask
* SQLite
* `requirements.txt` (requests, etc.)

### Running the System

1.  **Clone the Repository:**
    ```bash
    git clone dekut-farmtech-v6.git
    cd dekut-farmtech-v6
    ```
2.  **Initialize Database and Policies:**
    (The `scheduler_gateway.py` script handles the SQLite setup on first run.)
    You must ensure `ai_knowledge.json` and `critical_policies.json` are present in the root directory.
3.  **Start the Gateway:**
    ```bash
    python scheduler_gateway.py
    ```
4.  **Access the Dashboard:**
    Open `dashboard.html` in your web browser, or navigate to the API: `http://127.0.0.1:5000`

## 3. Key Components

| File Name | Category | Function |
| :--- | :--- | :--- |
| `scheduler_gateway.py` | Orchestration | Main Flask API and component lifecycle manager. |
| `ai_agent.py` | AI Core | Layered Rule Engine and Action Decider. |
| `ai_knowledge.json` | Knowledge | System thresholds and safety protocols. |
| `dashboard.html` | Front-end | User interface for data submission. |