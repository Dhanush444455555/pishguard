"""
PhishGuard AI — ML Predictor Service
=====================================
Loads the trained phishing detection model and provides a prediction
interface for the backend API.
"""

import os
from pathlib import Path
from typing import Optional

import joblib
import pandas as pd

# Import shared feature extraction logic
import sys
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from utils.feature_extractor import extract_features, FEATURE_NAMES


class PhishingPredictor:
    """
    Wrapper around the trained phishing detection model.
    Provides a simple predict(url) → result interface.
    """

    def __init__(self, model_dir: Optional[str] = None):
        if model_dir is None:
            model_dir = Path(__file__).resolve().parent.parent / "models"
        else:
            model_dir = Path(model_dir)

        model_path = model_dir / "phishing_model.pkl"
        meta_path = model_dir / "vectorizer.pkl"

        if not model_path.exists():
            raise FileNotFoundError(
                f"Model not found at {model_path}. "
                "Run notebooks/model_training.py first."
            )

        self.model = joblib.load(model_path)
        self.metadata = joblib.load(meta_path) if meta_path.exists() else {}
        self.feature_names = self.metadata.get("feature_names", FEATURE_NAMES)

    def predict(self, url: str) -> dict:
        """
        Predict whether a URL is phishing or legitimate.

        Returns:
            dict with keys:
              - is_phishing: bool
              - confidence: float (0-1, probability of phishing)
              - risk_score: float (0-100 scale)
              - label: str ("phishing" or "legitimate")
              - features: dict of extracted features
        """
        features = extract_features(url)
        feature_df = pd.DataFrame([features], columns=self.feature_names)

        prediction = self.model.predict(feature_df)[0]
        probabilities = self.model.predict_proba(feature_df)[0]
        phishing_prob = float(probabilities[1])

        return {
            "is_phishing": bool(prediction == 1),
            "confidence": phishing_prob,
            "risk_score": round(phishing_prob * 100, 1),
            "label": "phishing" if prediction == 1 else "legitimate",
            "features": features,
        }

    def predict_batch(self, urls: list) -> list:
        """Predict for a batch of URLs."""
        return [self.predict(url) for url in urls]

    def get_model_info(self) -> dict:
        """Return metadata about the loaded model."""
        return {
            "model_type": self.metadata.get("model_type", "unknown"),
            "accuracy": self.metadata.get("accuracy"),
            "f1_score": self.metadata.get("f1_score"),
            "roc_auc": self.metadata.get("roc_auc"),
            "training_date": self.metadata.get("training_date"),
            "num_features": len(self.feature_names),
            "feature_names": self.feature_names,
        }


# ─────────────────────────────────────────────────────────────────────
# Singleton instance for the backend
# ─────────────────────────────────────────────────────────────────────
_predictor: Optional[PhishingPredictor] = None


def get_predictor() -> PhishingPredictor:
    """Get or create the singleton predictor instance."""
    global _predictor
    if _predictor is None:
        _predictor = PhishingPredictor()
    return _predictor
