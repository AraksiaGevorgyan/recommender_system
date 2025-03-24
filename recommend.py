from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from data_loader import load_users, load_projects, load_user_skills, load_project_skills
import numpy as np
from joblib import Parallel, delayed

vectorizer = TfidfVectorizer()
def compute_tfidf(corpus):
    return vectorizer.fit_transform(corpus)

def normalize_scores(scores):
    if scores.size == 0:
        return scores
    min_val, max_val = scores.min(), scores.max()
    return (scores - min_val) / (max_val - min_val) if max_val > min_val else scores
    
def compute_similarity(user_skills, projects_skills):
    if not user_skills or not projects_skills:
        return np.array([])
    corpus = [" ".join(user_skills)] + [" ".join(skills) for skills in projects_skills]
    try:
        tfidf_matrix = compute_tfidf(corpus)
    except Exception as e:
        print(f"Error in TF-IDF computation: {e}")
        return []
    
    similarities = cosine_similarity(tfidf_matrix[0],tfidf_matrix[1:]).flatten()
    return normalize_scores(similarities)

def recommend_projects(user_id):
    user_skills = load_user_skills().get(user_id, [])
    if not user_skills:
        return []
    project_skills = load_project_skills()
    project_ids, project_skills_list = list(project_skills.keys()), list(project_skills.values())
    similarity_scores = compute_similarity(user_skills, project_skills_list)
    projects = {p["id"]: p for p in load_projects()}
    return {
        "recommendations": [
            {"id": projects[pid]["id"], "id": projects[pid]["id"], "score": float(score)}
            for pid, score in sorted(zip(project_ids, similarity_scores), key=lambda x: x[1], reverse=True)
        ]
    }
def recommend_users(project_id):
    project_skills = load_project_skills().get(project_id, [])
    if not project_skills:
        print(f"No skills found for project {project_id}.")
        return []
    
    user_skills = load_user_skills()
    user_skills_list, user_ids = list(user_skills.values()), list(user_skills.keys())
    similarity_scores = compute_similarity(project_skills, user_skills_list)

    users = {u["id"]: u for u in load_users()}
    return {
    "recommendations": [
        {"id": users[uid]["id"], "name": users[uid]["name"], "score": float(score)}
        for uid, score in sorted(zip(user_ids, similarity_scores), key=lambda x: x[1], reverse=True)
        ]
    }
