import tensorflow as tf
from typing import List, Dict, Optional
import numpy as np


FEATURE_KEYS = [
    "danceability",
    "energy",
    "valence",
    "acousticness",
    "instrumentalness",
    "tempo"
]

TEMPO_MIN = 60.0
TEMPO_MAX = 200.0

MOOD_PROFILES = {
    "happy": {
        "valence": 0.8,
        "energy": 0.7,
        "danceability": 0.7
    },
    "chill": {
        "valence": 0.5,
        "energy": 0.3,
        "acousticness": 0.7
    },
    "workout": {
        "energy": 0.8,
        "danceability": 0.8,
        "tempo": 0.8
    },
    "sad": {
        "valence": 0.2,
        "energy": 0.3,
        "acousticness": 0.6
    },
    "energetic": {
        "energy": 0.9,
        "tempo": 0.7,
        "danceability": 0.6
    }
}


def extract_features(audio_features: dict) -> Optional[tf.Tensor]:
    if not audio_features:
        return None
    
    try:
        tempo_normalized = (audio_features.get("tempo", 120) - TEMPO_MIN) / (TEMPO_MAX - TEMPO_MIN)
        tempo_normalized = max(0.0, min(1.0, tempo_normalized))
        
        feature_vector = [
            audio_features.get("danceability", 0.5),
            audio_features.get("energy", 0.5),
            audio_features.get("valence", 0.5),
            tempo_normalized,
            audio_features.get("acousticness", 0.5),
            audio_features.get("instrumentalness", 0.5)
        ]
        
        return tf.constant(feature_vector, dtype=tf.float32)
        
    except Exception:
        return None


def build_user_vector(track_vectors: List[tf.Tensor]) -> tf.Tensor:
    if not track_vectors:
        return tf.zeros(6, dtype=tf.float32)
    
    stacked = tf.stack(track_vectors)
    user_vector = tf.reduce_mean(stacked, axis=0)
    
    return user_vector


def normalize_vector(vector: tf.Tensor) -> tf.Tensor:
    return tf.nn.l2_normalize(vector)


def apply_mood_profile(
    user_vector: tf.Tensor,
    mood: str,
    influence: float = 0.3
) -> tf.Tensor:
    if mood not in MOOD_PROFILES:
        return user_vector
    
    profile = MOOD_PROFILES[mood]
    mood_vector = tf.zeros(6, dtype=tf.float32)
    
    if "valence" in profile:
        mood_vector = mood_vector + [0, 0, profile["valence"], 0, 0, 0]
    if "energy" in profile:
        mood_vector = mood_vector + [0, profile["energy"], 0, 0, 0, 0]
    if "danceability" in profile:
        mood_vector = mood_vector + [profile["danceability"], 0, 0, 0, 0, 0]
    if "acousticness" in profile:
        mood_vector = mood_vector + [0, 0, 0, 0, profile["acousticness"], 0]
    if "tempo" in profile:
        mood_vector = mood_vector + [0, 0, 0, profile["tempo"], 0, 0]
    
    blended_vector = (1 - influence) * user_vector + influence * mood_vector
    
    return blended_vector
