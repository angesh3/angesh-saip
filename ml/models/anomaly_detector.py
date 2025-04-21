import numpy as np
import pandas as pd
from sklearn.ensemble import IsolationForest
from tensorflow.keras.models import Model, Sequential
from tensorflow.keras.layers import Dense, Input
from tensorflow.keras.optimizers import Adam
from typing import Tuple, Dict, Any
import joblib
import os

class AnomalyDetector:
    def __init__(self, model_type: str = 'isolation_forest'):
        """
        Initialize the anomaly detector.
        
        Args:
            model_type: Type of model to use ('isolation_forest' or 'autoencoder')
        """
        self.model_type = model_type
        self.model = None
        self.threshold = None
        
    def build_autoencoder(self, input_dim: int) -> Model:
        """
        Build an autoencoder model for anomaly detection.
        
        Args:
            input_dim: Dimension of input features
            
        Returns:
            Compiled autoencoder model
        """
        # Encoder
        encoder = Sequential([
            Dense(input_dim // 2, activation='relu', input_shape=(input_dim,)),
            Dense(input_dim // 4, activation='relu'),
            Dense(input_dim // 8, activation='relu')
        ])
        
        # Decoder
        decoder = Sequential([
            Dense(input_dim // 4, activation='relu', input_shape=(input_dim // 8,)),
            Dense(input_dim // 2, activation='relu'),
            Dense(input_dim, activation='sigmoid')
        ])
        
        # Autoencoder
        autoencoder = Sequential([
            Input(shape=(input_dim,)),
            encoder,
            decoder
        ])
        
        autoencoder.compile(optimizer=Adam(learning_rate=0.001), loss='mse')
        return autoencoder
    
    def fit(self, data: pd.DataFrame, contamination: float = 0.1) -> None:
        """
        Fit the anomaly detection model.
        
        Args:
            data: DataFrame containing preprocessed data
            contamination: Expected proportion of anomalies in the data
        """
        if self.model_type == 'isolation_forest':
            self.model = IsolationForest(
                n_estimators=100,
                contamination=contamination,
                random_state=42
            )
            self.model.fit(data)
        elif self.model_type == 'autoencoder':
            input_dim = data.shape[1]
            self.model = self.build_autoencoder(input_dim)
            self.model.fit(
                data, data,
                epochs=50,
                batch_size=32,
                validation_split=0.2,
                verbose=0
            )
            # Calculate reconstruction error threshold
            reconstructions = self.model.predict(data)
            mse = np.mean(np.power(data - reconstructions, 2), axis=1)
            self.threshold = np.percentile(mse, (1 - contamination) * 100)
    
    def predict(self, data: pd.DataFrame) -> Tuple[np.ndarray, np.ndarray]:
        """
        Predict anomaly scores for the data.
        
        Args:
            data: DataFrame containing preprocessed data
            
        Returns:
            Tuple of (anomaly_scores, is_anomaly)
        """
        if self.model_type == 'isolation_forest':
            # Isolation Forest returns -1 for anomalies and 1 for normal points
            scores = self.model.score_samples(data)
            # Convert to anomaly scores (0 to 1, where 1 is most anomalous)
            anomaly_scores = 1 - (scores - scores.min()) / (scores.max() - scores.min())
            is_anomaly = self.model.predict(data) == -1
        elif self.model_type == 'autoencoder':
            reconstructions = self.model.predict(data)
            mse = np.mean(np.power(data - reconstructions, 2), axis=1)
            anomaly_scores = mse / self.threshold
            is_anomaly = mse > self.threshold
        
        return anomaly_scores, is_anomaly
    
    def save_model(self, model_path: str) -> None:
        """
        Save the model to disk.
        
        Args:
            model_path: Path to save the model
        """
        os.makedirs(os.path.dirname(model_path), exist_ok=True)
        if self.model_type == 'isolation_forest':
            joblib.dump(self.model, model_path)
        elif self.model_type == 'autoencoder':
            self.model.save(model_path)
    
    def load_model(self, model_path: str) -> None:
        """
        Load the model from disk.
        
        Args:
            model_path: Path to load the model from
        """
        if self.model_type == 'isolation_forest':
            self.model = joblib.load(model_path)
        elif self.model_type == 'autoencoder':
            self.model = Model.load_model(model_path) 