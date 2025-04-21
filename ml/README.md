# SAIP ML Service

This is the Machine Learning service component of the Secure Access Insights Platform (SAIP). It provides anomaly detection capabilities for access logs using various ML algorithms.

## Features

- Anomaly detection using Isolation Forest and Autoencoder models
- Data preprocessing and feature engineering
- REST API for model training and inference
- Feature importance analysis
- Model persistence and loading

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Set up environment variables:
```bash
cp .env.example .env
# Edit .env with your configuration
```

3. Run the service:
```bash
python main.py
```

## API Endpoints

### Train Model
```http
POST /train
Content-Type: application/json

{
    "data": [...],
    "model_type": "isolation_forest",
    "contamination": 0.1
}
```

### Detect Anomalies
```http
POST /detect
Content-Type: application/json

{
    "data": [...],
    "threshold": 0.7
}
```

### Get Feature Importance
```http
GET /feature-importance
```

### Health Check
```http
GET /health
```

## Model Types

1. **Isolation Forest**
   - Fast and efficient for high-dimensional data
   - Good for detecting point anomalies
   - Less sensitive to outliers

2. **Autoencoder**
   - Better at detecting complex patterns
   - Can capture temporal dependencies
   - More computationally intensive

## Data Format

The service expects access log data in the following format:
```json
{
    "timestamp": "2024-01-01T00:00:00Z",
    "user_id": 1,
    "resource_type": "file",
    "resource_id": "doc123",
    "action": "read",
    "source_ip": "192.168.1.1",
    "location": {
        "country": "US",
        "city": "New York"
    }
}
```

## Development

1. Install development dependencies:
```bash
pip install -r requirements-dev.txt
```

2. Run tests:
```bash
pytest
```

3. Format code:
```bash
black .
```

## Docker

Build and run the service using Docker:

```bash
docker build -t saip-ml .
docker run -p 8001:8001 saip-ml
``` 