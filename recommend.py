from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from data_loader import load_users, load_projects, load_user_skills, load_project_skills
import numpy as np

def normalize_scores(scores: np.ndarray) -> np.ndarray:
    if scores.size == 0:
        return scores
    min_val, max_val = scores.min(), scores.max()
    if max_val > min_val:
        return (scores - min_val) / (max_val - min_val)
    else:
        return scores
def compute_tfidf(corpus:list[str]) -> np.ndarray:
    vectorizer = TfidfVectorizer()
    return vectorizer.fit_transform(corpus)

def compute_similarity(user_skills, projects_skills):
    if not user_skills:
        print("Warning: No skills provided for user.")
        return np.array([])
    if not projects_skills:
        print("Warning: No skills provided for projects.")
        return np.array([])

    corpus = [" ".join(user_skills)] + [" ".join(skills) for skills in projects_skills]
    projects_str = [" ".join(skills) for skills in projects_skills]

    try:
        tfidf_matrix = compute_tfidf(corpus)
    except Exception as e:
        print(f"Error in TF-IDF computation: {e}")
        return np.array([])
    
    user_vector = tfidf_matrix[0].reshape(1, -1)  
    projects_vectors = tfidf_matrix[1:]

    similarities = cosine_similarity(user_vector, projects_vectors).flatten()
    return normalize_scores(similarities)

def recommend_projects(user_id):
    user_skills = load_user_skills().get(user_id, [])

    if not user_skills:
        print(f"No skills found for user {user_id}.")
        return []

    project_skills = load_project_skills()
    project_ids = list(project_skills.keys())
    project_skills_list = list(project_skills.values())
    
    similarity_scores = compute_similarity(user_skills, project_skills_list)

    # Load project details
    projects = {p["id"]: p for p in load_projects()}
    recommended_projects = sorted(zip(project_ids, similarity_scores), key=lambda x: x[1], reverse=True)

    return [(projects[pid], score) for pid, score in recommended_projects if pid in projects]

def recommend_users(project_id):
    project_skills = load_project_skills().get(project_id, [])

    if not project_skills:
        print(f"No skills found for project {project_id}.")
        return []

    user_skills = load_user_skills()
    user_ids = list(user_skills.keys())
    user_skills_list = list(user_skills.values())
    
    similarity_scores = compute_similarity(project_skills, user_skills_list)

    users = {u["id"]: u for u in load_users()}
    recommended_users = sorted(zip(user_ids, similarity_scores), key=lambda x: x[1], reverse=True)

    return [(users[uid], score) for uid, score in recommended_users if uid in users]
