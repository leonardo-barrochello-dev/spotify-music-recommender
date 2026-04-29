import random
from typing import List, Dict, Set, Tuple
from app.models.schemas import Track, Artist
from app.services.spotify_service import SpotifyService
import logging
from app.enums import SearchType

logger = logging.getLogger(__name__)


class CandidateGenerator:
    def __init__(self, spotify_service: SpotifyService):
        self.spotify_service = spotify_service
        self._seen_track_ids: Set[str] = set()

    async def generate(
        self, top_tracks: List[Track], top_artists: List[Artist], access_token: str
    ) -> Tuple[List[Track], Dict[str, float]]:

        all_candidates: List[Track] = []
        known_track_ids = {t.id for t in top_tracks}
        candidate_scores: Dict[str, float] = {}

        sources = {"artist_based": 0, "track_based": 0, "exploration": 0}

        # =====================================================
        # 🔹 1. BASEADO EM ARTISTAS (mais forte que antes)
        # =====================================================
        for artist in top_artists[:5]:
            try:
                # 🔥 busca mais contextual (não só "artist name track")
                query = f"{artist.name}"

                tracks = await self.spotify_service.search(
                    access_token, type=SearchType.TRACK, query=query, limit=10
                )

                for t in tracks:
                    if t.id not in known_track_ids and t.id not in self._seen_track_ids:
                        all_candidates.append(t)
                        self._seen_track_ids.add(t.id)
                        sources["artist_based"] += 1
                        candidate_scores[t.id] = candidate_scores.get(t.id, 0) + 2

            except Exception as e:
                logger.warning(f"Artist search failed for {artist.name}: {e}")

        # =====================================================
        # 🔹 2. BASEADO EM MÚSICAS (similaridade indireta)
        # =====================================================
        
        random.shuffle(top_tracks)

        sample_tracks = top_tracks[:5]

        for base_track in sample_tracks:
            try:
                # 🔥 melhora aqui: usar artista + nome da música
                artist_name = (
                    base_track.artists[0]["name"] if base_track.artists else ""
                )
                query = f"{base_track.name} {artist_name}"

                tracks = await self.spotify_service.search(
                    access_token, type=SearchType.TRACK, query=query, limit=10
                )

                for t in tracks:
                    if t.id not in known_track_ids and t.id not in self._seen_track_ids:
                        all_candidates.append(t)
                        self._seen_track_ids.add(t.id)
                        sources["track_based"] += 1
                        candidate_scores[t.id] = candidate_scores.get(t.id, 0) + 3

            except Exception as e:
                logger.warning(f"Track search failed for {base_track.name}: {e}")

        # =====================================================
        # 🔹 3. EXPLORAÇÃO INTELIGENTE (semi-personalizada)
        # =====================================================
        genre_seeds = []

        for artist in top_artists:
            if artist.genres:
                genre_seeds.extend(artist.genres[:2])

        # fallback se não tiver gênero
        if not genre_seeds:
            genre_seeds = ["rock", "pop", "electronic", "metal"]

        random.shuffle(genre_seeds)

        for genre in genre_seeds[:4]:
            try:
                tracks = await self.spotify_service.search(
                    access_token, type=SearchType.TRACK, query=genre, limit=10
                )

                for t in tracks:
                    if t.id not in known_track_ids and t.id not in self._seen_track_ids:
                        all_candidates.append(t)
                        self._seen_track_ids.add(t.id)
                        sources["exploration"] += 1
                        candidate_scores[t.id] = candidate_scores.get(t.id, 0) + 1

            except Exception as e:
                logger.warning(f"Exploration search failed for {genre}: {e}")

        # =====================================================
        # 🔹 4. DEDUPLICAÇÃO
        # =====================================================
        unique_candidates: Dict[str, Track] = {}

        for t in all_candidates:
            if t.id not in unique_candidates:
                unique_candidates[t.id] = t

        candidates = list(unique_candidates.values())

        # =====================================================
        # 🔹 5. SHUFFLE FINAL (evitar ranking enviesado)
        # =====================================================
        random.shuffle(candidates)

        logger.info(f"Candidate generation summary: {sources}")
        logger.info(f"Final candidates: {len(candidates)} tracks")

        return candidates, candidate_scores

    def clear_seen(self):
        self._seen_track_ids.clear()
