import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler, LabelEncoder
from typing import Tuple, Dict, Any

class DataPreprocessor:
    def __init__(self):
        self.scaler = StandardScaler()
        self.label_encoders = {}
        
    def preprocess_access_logs(self, data: pd.DataFrame) -> Tuple[pd.DataFrame, Dict[str, Any]]:
        """
        Preprocess access log data for anomaly detection.
        
        Args:
            data: DataFrame containing access log data
            
        Returns:
            Tuple of (processed_data, preprocessing_info)
        """
        # Create a copy to avoid modifying the original data
        df = data.copy()
        
        # Convert timestamp to datetime if it's not already
        if not pd.api.types.is_datetime64_any_dtype(df['timestamp']):
            df['timestamp'] = pd.to_datetime(df['timestamp'])
        
        # Extract time-based features
        df['hour'] = df['timestamp'].dt.hour
        df['day_of_week'] = df['timestamp'].dt.dayofweek
        df['is_weekend'] = df['day_of_week'].isin([5, 6]).astype(int)
        
        # Encode categorical variables
        categorical_cols = ['resource_type', 'action', 'source_ip']
        for col in categorical_cols:
            if col in df.columns:
                le = LabelEncoder()
                df[col] = le.fit_transform(df[col].astype(str))
                self.label_encoders[col] = le
        
        # Extract location features
        if 'location' in df.columns:
            df['country_code'] = df['location'].apply(lambda x: x.get('country', 'unknown'))
            df['city'] = df['location'].apply(lambda x: x.get('city', 'unknown'))
            
            # Encode location features
            for col in ['country_code', 'city']:
                le = LabelEncoder()
                df[col] = le.fit_transform(df[col].astype(str))
                self.label_encoders[col] = le
        
        # Scale numerical features
        numerical_cols = ['hour', 'day_of_week']
        if numerical_cols:
            df[numerical_cols] = self.scaler.fit_transform(df[numerical_cols])
        
        # Store preprocessing information
        preprocessing_info = {
            'label_encoders': self.label_encoders,
            'scaler': self.scaler
        }
        
        return df, preprocessing_info
    
    def inverse_transform(self, data: pd.DataFrame, preprocessing_info: Dict[str, Any]) -> pd.DataFrame:
        """
        Inverse transform preprocessed data back to original format.
        
        Args:
            data: DataFrame containing preprocessed data
            preprocessing_info: Dictionary containing preprocessing information
            
        Returns:
            DataFrame with original format
        """
        df = data.copy()
        
        # Inverse transform label encoded columns
        for col, le in preprocessing_info['label_encoders'].items():
            if col in df.columns:
                df[col] = le.inverse_transform(df[col])
        
        # Inverse transform scaled columns
        numerical_cols = ['hour', 'day_of_week']
        if numerical_cols:
            df[numerical_cols] = preprocessing_info['scaler'].inverse_transform(df[numerical_cols])
        
        return df 