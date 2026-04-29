import numpy as np
from sentence_transformers import SentenceTransformer
from typing import List, Tuple, Optional, Dict
import logging
import time

from app.models.schemas import Track

logger = logging.getLogger(__name__)


class RecommendationEngine:
    """
    Engine responsável por:
    - Converter músicas em embeddings (vetores semânticos)
    - Criar representação do usuário
    - Calcular similaridade
    - Rankear recomendações
    """

    def __init__(self):
        # Modelo de embeddings (carregado sob demanda)
        self._model: Optional[SentenceTransformer] = None

        # Cache em memória para evitar recomputar embeddings
        # chave: track_id
        # valor: vetor numpy
        self._embedding_cache: Dict[str, np.ndarray] = {}

    # =========================================================
    # 🔹 MODEL LOADING (lazy loading)
    # =========================================================
    @property
    def model(self) -> SentenceTransformer:
        """
        Carrega o modelo apenas na primeira vez (evita custo repetido)
        """
        if self._model is None:
            logger.info("Loading embedding model: all-MiniLM-L6-v2")
            self._model = SentenceTransformer("all-MiniLM-L6-v2")
            logger.info("Model loaded successfully")
        return self._model

    # =========================================================
    # 🔹 TEXT REPRESENTATION
    # =========================================================
    def track_to_text(self, track: Track) -> str:
        """
        Converte uma música em texto descritivo.
        Esse texto será usado para gerar o embedding.

        Quanto mais contexto, melhor a qualidade do embedding.
        """

        parts = [track.name]

        # Adiciona informações do artista
        for artist in track.artists[:1]:  # usa só o principal
            if "name" in artist:
                parts.append(artist["name"])

            # Se existir gênero (depende do endpoint usado)
            if "genres" in artist:
                parts.extend(artist["genres"][:3])

        return " ".join(parts)

    # =========================================================
    # 🔹 EMBEDDING (com cache)
    # =========================================================
    def encode_tracks(self, tracks: List[Track]) -> Tuple[List[str], np.ndarray]:
        """
        Converte lista de músicas em embeddings.

        Usa cache para evitar recomputação.
        Usa batch encoding para performance.
        """

        texts = [self.track_to_text(t) for t in tracks]
        track_ids = [t.id for t in tracks]

        # Identifica quais ainda não estão no cache
        uncached_ids = []
        uncached_texts = []

        for tid, text in zip(track_ids, texts):
            if tid not in self._embedding_cache:
                uncached_ids.append(tid)
                uncached_texts.append(text)

        # Codifica apenas os novos
        if uncached_texts:
            start = time.time()

            embeddings = self.model.encode(
                uncached_texts,
                show_progress_bar=False
            )

            # Salva no cache
            for tid, emb in zip(uncached_ids, embeddings):
                self._embedding_cache[tid] = emb

            logger.info(
                f"Encoded {len(uncached_texts)} new tracks in {time.time() - start:.2f}s"
            )

        # Monta lista final na ordem correta
        all_embeddings = np.array([
            self._embedding_cache[tid] for tid in track_ids
        ])

        return track_ids, all_embeddings

    # =========================================================
    # 🔹 USER VECTOR
    # =========================================================
    def build_user_embedding(self, top_tracks: List[Track]) -> np.ndarray:
        """
        Cria vetor do usuário a partir das músicas favoritas.

        Estratégia:
        média dos embeddings das músicas
        """

        if not top_tracks:
            # vetor neutro (fallback)
            return np.zeros(384)

        _, embeddings = self.encode_tracks(top_tracks[:10])

        if embeddings.shape[0] == 0:
            return np.zeros(384)

        # Média dos embeddings
        user_embedding = np.mean(embeddings, axis=0)

        # Normalização (importante para cosine similarity)
        user_embedding = user_embedding / (
            np.linalg.norm(user_embedding) + 1e-8
        )

        return user_embedding

    # =========================================================
    # 🔹 SIMILARIDADE
    # =========================================================
    def compute_similarity(
        self,
        user_embedding: np.ndarray,
        item_embeddings: np.ndarray
    ) -> np.ndarray:
        """
        Calcula similaridade entre usuário e itens.

        Usa cosine similarity:
        - normaliza vetores
        - calcula produto escalar
        """

        item_norms = item_embeddings / (
            np.linalg.norm(item_embeddings, axis=1, keepdims=True) + 1e-8
        )

        similarities = np.dot(item_norms, user_embedding)

        return similarities

    # =========================================================
    # 🔹 MOOD BOOST (melhor que filtro)
    # =========================================================
    def apply_mood_boost(
        self,
        tracks: List[Track],
        similarities: np.ndarray,
        mood: str
    ) -> np.ndarray:
        """
        Em vez de filtrar, damos um "boost" na similaridade
        para músicas que combinam com o mood.
        """

        mood_keywords = {
            "workout": ["rock", "dance", "electronic", "hip-hop"],
            "chill": ["ambient", "jazz", "acoustic"],
            "happy": ["pop", "funk", "dance"],
            "sad": ["blues", "acoustic", "soul"],
            "energetic": ["rock", "metal", "electronic"]
        }

        keywords = mood_keywords.get(mood.lower(), [])

        if not keywords:
            return similarities

        boosted = similarities.copy()

        for i, track in enumerate(tracks):
            text = self.track_to_text(track).lower()

            if any(kw in text for kw in keywords):
                boosted[i] += 0.05  # pequeno boost

        return boosted

    # =========================================================
    # 🔹 RANKING
    # =========================================================
    def rank_tracks(
        self,
        user_tracks: List[Track],
        candidate_tracks: List[Track],
        limit: int = 20,
        mood: Optional[str] = None
    ) -> List[Track]:
        """
        Pipeline principal do recomendador.
        """

        if not candidate_tracks:
            logger.warning("No candidate tracks")
            return []

        logger.info(f"Ranking {len(candidate_tracks)} tracks")

        start = time.time()

        # 1. Vetor do usuário
        user_embedding = self.build_user_embedding(user_tracks)

        # 2. Embeddings dos candidatos
        _, item_embeddings = self.encode_tracks(candidate_tracks)

        # 3. Similaridade
        similarities = self.compute_similarity(user_embedding, item_embeddings)

        # 4. Aplicar mood (boost)
        if mood:
            similarities = self.apply_mood_boost(
                candidate_tracks,
                similarities,
                mood
            )

        # 5. Ordenar (desc)
        top_indices = np.argsort(similarities)[::-1][:limit]

        logger.info(
            f"Ranking completed in {time.time() - start:.2f}s"
        )

        # 6. Retornar tracks ordenadas
        ranked_tracks = [candidate_tracks[i] for i in top_indices]

        return ranked_tracks

    # =========================================================
    # 🔹 UTIL
    # =========================================================
    def clear_cache(self):
        """
        Limpa cache de embeddings (útil para debug)
        """
        self._embedding_cache.clear()
        logger.info("Embedding cache cleared")