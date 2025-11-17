// This file contains the primary front-end logic extracted from dashboard.html

const API_URL = 'http://127.0.0.1:5000';
const logsContainer = document.getElementById('logs');
const heartbeatElement = document.getElementById('heartbeat');
const messageBox = document.getElementById('message-box');
const aiActionDisplay = document.getElementById('ai-action-display');
const dataForm = document.getElementById('data-form');

function log(message, type = 'INFO') {
    // Logging logic remains the same (appends to logsContainer)
    // ... (omitted for brevity)
    const logEntry = document.createElement('div');
    logEntry.textContent = `[${new Date().toLocaleTimeString()}] [${type}] ${message}`;
    logEntry.className = (type === 'CRITICAL' || type === 'ERROR') ? 'text-red-500' : 'text-green-400';
    logsContainer.appendChild(logEntry);
    logsContainer.scrollTop = logsContainer.scrollHeight;
}

async function fetchHeartbeat() {
    try {
        const response = await fetch(`${API_URL}/status`);
        const data = await response.json();
        heartbeatElement.textContent = new Date().toLocaleTimeString();
        
        // Safety lock status display logic
        const safetyLockElement = document.getElementById('safety-lock-status');
        if (data.safety_lock === false) {
            safetyLockElement.textContent = `Lock: INACTIVE (Privilege Jump!)`;
            safetyLockElement.className = 'font-mono text-xs text-red-500 font-bold';
            heartbeatElement.className = 'font-mono text-xs text-red-500 font-bold';
        } else {
            safetyLockElement.textContent = `Lock: ACTIVE`;
            safetyLockElement.className = 'font-mono text-xs text-gray-400';
            heartbeatElement.className = 'font-mono text-xs text-green-400';
        }

    } catch (error) {
        heartbeatElement.textContent = 'Worker Offline';
        heartbeatElement.className = 'font-mono text-xs text-red-700';
    }
}

async function handleDataSubmission(e) {
    e.preventDefault();
    messageBox.textContent = 'Sending data...';
    
    // Collect all 7 required variables from the form
    const payload = [
        {
            "field_id": dataForm.elements['field-id'].value, 
            "moisture": parseInt(dataForm.elements['moisture'].value), 
            "nutrient_level": dataForm.elements['nutrient-level'].value,
            "temp": parseInt(dataForm.elements['temp'].value),
            "cost_kes": parseInt(dataForm.elements['cost_kes'].value), 
            "pump_pressure": parseInt(dataForm.elements['pump-pressure'].value),
            "historical_trend": dataForm.elements['historical-trend'].value
        }
    ];

    try {
        const response = await fetch(`${API_URL}/process_data`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload)
        });

        const data = await response.json();

        if (response.ok) {
            messageBox.textContent = `SUCCESS: ${data.prediction}`;
            aiActionDisplay.textContent = data.ai_action;
            log(`[BACKEND] Prediction: ${data.prediction} | AI Action: ${data.ai_action}`, 'SUCCESS');
        } else {
            messageBox.textContent = `ERROR: ${data.message || 'Unknown error'}`;
            aiActionDisplay.textContent = "Error during processing.";
            log(`[BACKEND] Error: ${data.message || 'Server did not respond.'}`, 'ERROR');
        }
    } catch (error) {
        messageBox.textContent = `CONNECTION ERROR: Could not reach ${API_URL}`;
        aiActionDisplay.textContent = "Worker Offline.";
        log(`[FATAL] Connection failed. Is the server running? ${error.message}`, 'CRITICAL');
    }
}

// Event Listeners
dataForm.addEventListener('submit', handleDataSubmission);
setInterval(fetchHeartbeat, 3000); // Fetch heartbeat every 3 seconds
fetchHeartbeat(); // Initial fetch