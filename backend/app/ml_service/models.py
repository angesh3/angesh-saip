import os
import pickle
import numpy as np
import pandas as pd
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from datetime import datetime, timedelta
from typing import List, Dict, Any

class AnomalyDetector:
    """
    Model for detecting anomalies in access logs.
    """
    def __init__(self, model_path: str):
        self.model_path = model_path
        self.model_file = os.path.join(model_path, "anomaly_detector.pkl")
        self.scaler_file = os.path.join(model_path, "anomaly_scaler.pkl")
        
        # Initialize model and scaler
        self.model = None
        self.scaler = None
        
        # Load model if it exists
        if os.path.exists(self.model_file) and os.path.exists(self.scaler_file):
            with open(self.model_file, "rb") as f:
                self.model = pickle.load(f)
            with open(self.scaler_file, "rb") as f:
                self.scaler = pickle.load(f)
        else:
            # Create new model
            self.model = IsolationForest(
                n_estimators=100,
                max_samples="auto",
                contamination=0.1,
                random_state=42
            )
            self.scaler = StandardScaler()
    
    def _preprocess_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Preprocess the data for anomaly detection.
        """
        # Extract features
        features = pd.DataFrame()
        
        # Time-based features
        df["hour"] = df["timestamp"].dt.hour
        df["day_of_week"] = df["timestamp"].dt.dayofweek
        
        # Categorical features
        features["resource_type_encoded"] = pd.Categorical(df["resource_type"]).codes
        features["action_encoded"] = pd.Categorical(df["action"]).codes
        features["location_encoded"] = pd.Categorical(df["location"]).codes
        
        # Numeric features
        features["hour"] = df["hour"]
        features["day_of_week"] = df["day_of_week"]
        
        # Scale features
        if self.scaler is None:
            self.scaler = StandardScaler()
            features_scaled = self.scaler.fit_transform(features)
        else:
            features_scaled = self.scaler.transform(features)
        
        return pd.DataFrame(features_scaled, columns=features.columns)
    
    def train(self, df: pd.DataFrame) -> None:
        """
        Train the anomaly detection model.
        """
        # Preprocess data
        features = self._preprocess_data(df)
        
        # Train model
        self.model.fit(features)
        
        # Save model and scaler
        os.makedirs(self.model_path, exist_ok=True)
        with open(self.model_file, "wb") as f:
            pickle.dump(self.model, f)
        with open(self.scaler_file, "wb") as f:
            pickle.dump(self.scaler, f)
    
    def detect(self, df: pd.DataFrame) -> List[Dict[str, Any]]:
        """
        Detect anomalies in the access logs.
        """
        # Preprocess data
        features = self._preprocess_data(df)
        
        # Predict anomalies
        predictions = self.model.predict(features)
        scores = self.model.score_samples(features)
        
        # Convert to list of anomalies
        anomalies = []
        for i, (pred, score) in enumerate(zip(predictions, scores)):
            if pred == -1:  # Anomaly
                anomalies.append({
                    "log_id": i,
                    "user_id": df.iloc[i]["user_id"],
                    "timestamp": df.iloc[i]["timestamp"].isoformat(),
                    "resource_type": df.iloc[i]["resource_type"],
                    "action": df.iloc[i]["action"],
                    "ip_address": df.iloc[i]["ip_address"],
                    "location": df.iloc[i]["location"],
                    "anomaly_score": float(score)
                })
        
        return anomalies


class AccessPatternAnalyzer:
    """
    Model for analyzing access patterns.
    """
    def __init__(self, model_path: str):
        self.model_path = model_path
        self.model_file = os.path.join(model_path, "pattern_analyzer.pkl")
        self.scaler_file = os.path.join(model_path, "pattern_scaler.pkl")
        
        # Initialize model and scaler
        self.model = None
        self.scaler = None
        
        # Load model if it exists
        if os.path.exists(self.model_file) and os.path.exists(self.scaler_file):
            with open(self.model_file, "rb") as f:
                self.model = pickle.load(f)
            with open(self.scaler_file, "rb") as f:
                self.scaler = pickle.load(f)
        else:
            # Create new model
            self.model = KMeans(n_clusters=5, random_state=42)
            self.scaler = StandardScaler()
    
    def _preprocess_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Preprocess the data for pattern analysis.
        """
        # Extract features
        features = pd.DataFrame()
        
        # Time-based features
        df["hour"] = df["timestamp"].dt.hour
        df["day_of_week"] = df["timestamp"].dt.dayofweek
        
        # Categorical features
        features["resource_type_encoded"] = pd.Categorical(df["resource_type"]).codes
        features["action_encoded"] = pd.Categorical(df["action"]).codes
        features["location_encoded"] = pd.Categorical(df["location"]).codes
        
        # Numeric features
        features["hour"] = df["hour"]
        features["day_of_week"] = df["day_of_week"]
        
        # Scale features
        if self.scaler is None:
            self.scaler = StandardScaler()
            features_scaled = self.scaler.fit_transform(features)
        else:
            features_scaled = self.scaler.transform(features)
        
        return pd.DataFrame(features_scaled, columns=features.columns)
    
    def train(self, df: pd.DataFrame) -> None:
        """
        Train the pattern analysis model.
        """
        # Preprocess data
        features = self._preprocess_data(df)
        
        # Train model
        self.model.fit(features)
        
        # Save model and scaler
        os.makedirs(self.model_path, exist_ok=True)
        with open(self.model_file, "wb") as f:
            pickle.dump(self.model, f)
        with open(self.scaler_file, "wb") as f:
            pickle.dump(self.scaler, f)
    
    def analyze(self, df: pd.DataFrame) -> List[Dict[str, Any]]:
        """
        Analyze access patterns in the logs.
        """
        # Preprocess data
        features = self._preprocess_data(df)
        
        # Predict clusters
        clusters = self.model.predict(features)
        
        # Calculate cluster centers
        centers = self.model.cluster_centers_
        
        # Convert to list of patterns
        patterns = []
        for i, cluster in enumerate(clusters):
            patterns.append({
                "log_id": i,
                "user_id": df.iloc[i]["user_id"],
                "timestamp": df.iloc[i]["timestamp"].isoformat(),
                "resource_type": df.iloc[i]["resource_type"],
                "action": df.iloc[i]["action"],
                "ip_address": df.iloc[i]["ip_address"],
                "location": df.iloc[i]["location"],
                "pattern_cluster": int(cluster),
                "pattern_center": centers[cluster].tolist()
            })
        
        return patterns 