import tensorflow as tf
from typing import Tuple


def cosine_similarity(user_vector: tf.Tensor, candidate_matrix: tf.Tensor) -> tf.Tensor:
    user_norm = tf.nn.l2_normalize(user_vector)
    candidates_norm = tf.nn.l2_normalize(candidate_matrix, axis=1)
    similarity = tf.linalg.dot(candidates_norm, user_norm)
    return similarity


def dot_product_similarity(user_vector: tf.Tensor, candidate_matrix: tf.Tensor) -> tf.Tensor:
    user_norm = tf.nn.l2_normalize(user_vector)
    candidates_norm = tf.nn.l2_normalize(candidate_matrix, axis=1)
    similarity = tf.reduce_sum(candidates_norm * user_norm, axis=1)
    return similarity


def euclidean_distance_similarity(user_vector: tf.Tensor, candidate_matrix: tf.Tensor) -> tf.Tensor:
    expanded_user = tf.expand_dims(user_vector, 0)
    distances = tf.norm(candidate_matrix - expanded_user, axis=1)
    max_distance = tf.reduce_max(distances)
    similarity = 1 - (distances / (max_distance + 1e-7))
    return similarity


def compute_similarity_scores(
    user_vector: tf.Tensor,
    candidate_matrix: tf.Tensor,
    method: str = "cosine"
) -> tf.Tensor:
    if method == "cosine":
        return cosine_similarity(user_vector, candidate_matrix)
    elif method == "dot_product":
        return dot_product_similarity(user_vector, candidate_matrix)
    elif method == "euclidean":
        return euclidean_distance_similarity(user_vector, candidate_matrix)
    else:
        return cosine_similarity(user_vector, candidate_matrix)


def rank_candidates(
    user_vector: tf.Tensor,
    candidate_matrix: tf.Tensor,
    candidate_ids: list,
    top_k: int = 20,
    method: str = "cosine"
) -> Tuple[list, tf.Tensor]:
    scores = compute_similarity_scores(user_vector, candidate_matrix, method)
    top_indices = tf.argsort(scores, direction="DESCENDING")[:top_k]
    ranked_ids = [candidate_ids[i] for i in top_indices.numpy()]
    ranked_scores = tf.gather(scores, top_indices)
    return ranked_ids, ranked_scores


def batch_similarity_computation(
    user_vectors: tf.Tensor,
    candidate_matrix: tf.Tensor,
    method: str = "cosine"
) -> tf.Tensor:
    users_norm = tf.nn.l2_normalize(user_vectors, axis=1)
    candidates_norm = tf.nn.l2_normalize(candidate_matrix, axis=1)
    similarity_matrix = tf.matmul(candidates_norm, users_norm, transpose_b=True)
    return similarity_matrix
