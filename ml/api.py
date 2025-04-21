from fastapi import FastAPI, HTTPException, BackgroundTasks
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
import pandas as pd
from models.service import AnomalyDetectionService
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="SAIP ML Service",
    description="Machine Learning service for anomaly detection in access logs",
    version="1.0.0"
)

# Initialize the anomaly detection service
ml_service = AnomalyDetectionService()

class TrainingRequest(BaseModel):
    data: List[Dict[str, Any]]
    model_type: str = 'isolation_forest'
    contamination: float = 0.1

class DetectionRequest(BaseModel):
    data: List[Dict[str, Any]]
    threshold: float = 0.7

class ModelResponse(BaseModel):
    message: str
    model_type: str
    stats: Optional[Dict[str, Any]] = None

@app.post("/train", response_model=ModelResponse)
async def train_model(request: TrainingRequest, background_tasks: BackgroundTasks):
    """
    Train the anomaly detection model.
    """
    try:
        # Convert data to DataFrame
        df = pd.DataFrame(request.data)
        
        # Train model in background
        background_tasks.add_task(
            ml_service.train_model,
            data=df,
            model_type=request.model_type,
            contamination=request.contamination
        )
        
        return ModelResponse(
            message="Model training started",
            model_type=request.model_type
        )
    except Exception as e:
        logger.error(f"Error training model: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/detect", response_model=ModelResponse)
async def detect_anomalies(request: DetectionRequest):
    """
    Detect anomalies in the provided data.
    """
    try:
        # Convert data to DataFrame
        df = pd.DataFrame(request.data)
        
        # Detect anomalies
        result_data, stats = ml_service.detect_anomalies(
            data=df,
            threshold=request.threshold
        )
        
        return ModelResponse(
            message="Anomalies detected successfully",
            model_type=ml_service.detector.model_type if ml_service.detector else None,
            stats=stats
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Error detecting anomalies: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/feature-importance")
async def get_feature_importance():
    """
    Get feature importance scores for the trained model.
    """
    try:
        if ml_service.detector is None:
            raise HTTPException(
                status_code=400,
                detail="Model not trained. Please train the model first."
            )
        
        # Get feature importance
        importance = ml_service.get_feature_importance(pd.DataFrame())
        
        return {
            "feature_importance": importance
        }
    except Exception as e:
        logger.error(f"Error getting feature importance: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health_check():
    """
    Health check endpoint.
    """
    return {
        "status": "healthy",
        "model_loaded": ml_service.detector is not None
    } 