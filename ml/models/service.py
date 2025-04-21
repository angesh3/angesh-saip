import os
import logging
import pandas as pd
from typing import Dict, Any, List, Tuple
from ..utils.preprocessor import DataPreprocessor
from .anomaly_detector import AnomalyDetector
import numpy as np

logger = logging.getLogger(__name__)

class AnomalyDetectionService:
    def __init__(self, model_dir: str = 'models'):
        """
        Initialize the anomaly detection service.
        
        Args:
            model_dir: Directory to store models
        """
        self.model_dir = model_dir
        self.preprocessor = DataPreprocessor()
        self.detector = None
        self.preprocessing_info = None
        
    def train_model(
        self,
        data: pd.DataFrame,
        model_type: str = 'isolation_forest',
        contamination: float = 0.1
    ) -> None:
        """
        Train the anomaly detection model.
        
        Args:
            data: DataFrame containing access log data
            model_type: Type of model to use
            contamination: Expected proportion of anomalies
        """
        logger.info(f"Training {model_type} model...")
        
        # Preprocess data
        processed_data, preprocessing_info = self.preprocessor.preprocess_access_logs(data)
        self.preprocessing_info = preprocessing_info
        
        # Initialize and train model
        self.detector = AnomalyDetector(model_type=model_type)
        self.detector.fit(processed_data, contamination=contamination)
        
        # Save model and preprocessing info
        model_path = os.path.join(self.model_dir, f'{model_type}_model')
        self.detector.save_model(model_path)
        
        logger.info(f"Model trained and saved to {model_path}")
    
    def detect_anomalies(
        self,
        data: pd.DataFrame,
        threshold: float = 0.7
    ) -> Tuple[pd.DataFrame, Dict[str, Any]]:
        """
        Detect anomalies in the data.
        
        Args:
            data: DataFrame containing access log data
            threshold: Threshold for anomaly scores
            
        Returns:
            Tuple of (data with anomaly scores, detection statistics)
        """
        if self.detector is None:
            raise ValueError("Model not trained. Please train the model first.")
        
        # Preprocess data
        processed_data, _ = self.preprocessor.preprocess_access_logs(data)
        
        # Detect anomalies
        anomaly_scores, is_anomaly = self.detector.predict(processed_data)
        
        # Add results to original data
        result_data = data.copy()
        result_data['anomaly_score'] = anomaly_scores
        result_data['is_anomaly'] = is_anomaly
        
        # Calculate statistics
        stats = {
            'total_samples': len(data),
            'anomalies_detected': int(is_anomaly.sum()),
            'anomaly_rate': float(is_anomaly.mean()),
            'mean_anomaly_score': float(anomaly_scores.mean()),
            'threshold_used': threshold
        }
        
        return result_data, stats
    
    def load_model(self, model_type: str = 'isolation_forest') -> None:
        """
        Load a trained model.
        
        Args:
            model_type: Type of model to load
        """
        model_path = os.path.join(self.model_dir, f'{model_type}_model')
        if not os.path.exists(model_path):
            raise FileNotFoundError(f"Model not found at {model_path}")
        
        self.detector = AnomalyDetector(model_type=model_type)
        self.detector.load_model(model_path)
        logger.info(f"Model loaded from {model_path}")
    
    def get_feature_importance(self, data: pd.DataFrame) -> Dict[str, float]:
        """
        Get feature importance scores for anomaly detection.
        
        Args:
            data: DataFrame containing access log data
            
        Returns:
            Dictionary of feature importance scores
        """
        if self.detector is None:
            raise ValueError("Model not trained. Please train the model first.")
        
        # Preprocess data
        processed_data, _ = self.preprocessor.preprocess_access_logs(data)
        
        if self.detector.model_type == 'isolation_forest':
            # For isolation forest, we can use the feature_importances_ attribute
            importances = self.detector.model.feature_importances_
        else:
            # For autoencoder, we'll use reconstruction error per feature
            reconstructions = self.detector.model.predict(processed_data)
            importances = np.mean(np.abs(processed_data - reconstructions), axis=0)
        
        # Create feature importance dictionary
        feature_importance = dict(zip(processed_data.columns, importances))
        
        return feature_importance 