import tensorflow as tf
from typing import List, Tuple, Optional
from app.models.schemas import Track
from app.ml.feature_engineering import (
    extract_features,
    build_user_vector,
    apply_mood_profile,
    FEATURE_KEYS
)
from app.ml.similarity_model import rank_candidates


class RecommendationEngine:
    def __init__(self, similarity_method: str = "cosine"):
        self.similarity_method = similarity_method
    
    def generate_recommendations(
        self,
        user_tracks: List[Track],
        candidate_tracks: List[Track],
        limit: int = 20,
        mood: Optional[str] = None
    ) -> Tuple[List[Track], List[float], str]:
        user_track_vectors = []
        valid_user_tracks = []
        
        for track in user_tracks:
            if track.audio_features:
                vector = extract_features(track.audio_features)
                if vector is not None:
                    user_track_vectors.append(vector)
                    valid_user_tracks.append(track)
        
        if not user_track_vectors:
            return [], [], "No valid audio features found for user tracks"
        
        user_vector = build_user_vector(user_track_vectors)
        
        if mood:
            user_vector = apply_mood_profile(user_vector, mood)
        
        candidate_vectors = []
        valid_candidates = []
        
        for track in candidate_tracks:
            if track.audio_features:
                vector = extract_features(track.audio_features)
                if vector is not None:
                    candidate_vectors.append(vector)
                    valid_candidates.append(track)
        
        if not candidate_vectors:
            return [], user_vector.numpy().tolist(), "No valid candidate tracks"
        
        candidate_matrix = tf.stack(candidate_vectors)
        
        ranked_ids, ranked_scores = rank_candidates(
            user_vector=user_vector,
            candidate_matrix=candidate_matrix,
            candidate_ids=[t.id for t in valid_candidates],
            top_k=limit,
            method=self.similarity_method
        )
        
        id_to_track = {t.id: t for t in valid_candidates}
        recommended_tracks = [id_to_track[track_id] for track_id in ranked_ids if track_id in id_to_track]
        
        explanation = self._generate_explanation(
            user_tracks=valid_user_tracks,
            recommended_tracks=recommended_tracks,
            mood=mood,
            avg_score=float(tf.reduce_mean(ranked_scores))
        )
        
        return recommended_tracks, user_vector.numpy().tolist(), explanation
    
    def _generate_explanation(
        self,
        user_tracks: List[Track],
        recommended_tracks: List[Track],
        mood: Optional[str],
        avg_score: float
    ) -> str:
        explanation_parts = []
        
        explanation_parts.append(
            f"Based on your top {len(user_tracks)} tracks"
        )
        
        if mood:
            mood_descriptions = {
                "happy": "upbeat and positive vibes",
                "chill": "relaxed and mellow atmosphere",
                "workout": "high-energy beats",
                "sad": "emotional and introspective tones",
                "energetic": "dynamic and powerful rhythms"
            }
            if mood in mood_descriptions:
                explanation_parts.append(
                    f"with a focus on {mood_descriptions[mood]}"
                )
        
        explanation_parts.append(
            f"(match score: {avg_score:.2f})"
        )
        
        return " ".join(explanation_parts)
    
    def get_feature_importance(self, user_vector: tf.Tensor) -> dict:
        feature_names = FEATURE_KEYS
        importance = {}
        
        vector_np = user_vector.numpy()
        max_val = max(abs(vector_np)) + 1e-7
        
        for i, name in enumerate(feature_names):
            importance[name] = float(abs(vector_np[i]) / max_val)
        
        sorted_importance = sorted(importance.items(), key=lambda x: x[1], reverse=True)
        
        return dict(sorted_importance)
