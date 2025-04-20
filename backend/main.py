from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
import pandas as pd
import numpy as np
from sklearn.ensemble import IsolationForest
import json

app = FastAPI(title="Secure Access Insights Platform API")

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://frontend:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Models
class AccessLog(BaseModel):
    user_id: str
    timestamp: datetime
    resource: str
    action: str
    ip_address: str
    location: Optional[str]
    device_type: Optional[str]
    status: str

class AnomalyAlert(BaseModel):
    alert_id: str
    user_id: str
    timestamp: datetime
    severity: str
    description: str
    details: dict

# In-memory storage for demo
access_logs = []
anomaly_alerts = []

# Anomaly detection model
model = IsolationForest(contamination=0.1, random_state=42)

@app.get("/")
async def root():
    return {"message": "Welcome to SAIP API"}

@app.post("/logs/", response_model=AccessLog)
async def create_access_log(log: AccessLog):
    access_logs.append(log)
    # Check for anomalies
    if len(access_logs) > 10:  # Only run anomaly detection after collecting enough data
        check_for_anomalies(log)
    return log

@app.get("/logs/", response_model=List[AccessLog])
async def get_access_logs(limit: int = 100):
    return access_logs[-limit:]

@app.get("/alerts/", response_model=List[AnomalyAlert])
async def get_alerts(limit: int = 100):
    return anomaly_alerts[-limit:]

def check_for_anomalies(new_log: AccessLog):
    # Convert logs to features for anomaly detection
    features = []
    for log in access_logs[-100:]:  # Use last 100 logs for context
        features.append([
            hash(log.user_id) % 1000,  # User ID hash
            log.timestamp.hour,  # Hour of day
            hash(log.resource) % 1000,  # Resource hash
            hash(log.action) % 1000,  # Action hash
            hash(log.ip_address) % 1000,  # IP hash
        ])
    
    if len(features) > 10:
        # Fit and predict
        model.fit(features)
        predictions = model.predict(features)
        
        # If the latest log is predicted as an anomaly
        if predictions[-1] == -1:
            alert = AnomalyAlert(
                alert_id=f"alert_{len(anomaly_alerts)}",
                user_id=new_log.user_id,
                timestamp=new_log.timestamp,
                severity="high",
                description="Unusual access pattern detected",
                details={
                    "resource": new_log.resource,
                    "action": new_log.action,
                    "ip_address": new_log.ip_address,
                }
            )
            anomaly_alerts.append(alert)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 