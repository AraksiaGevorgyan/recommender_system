from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from data_loader import load_users, load_projects, load_user_skills, load_project_skills

def compute_similarity(user_skills, projects_skills):
    """Compute cosine similarity between user skills and multiple project skills."""
    if not user_skills or not projects_skills:
        return []

    # Convert skills lists into space-separated strings
    user_str = " ".join(user_skills)  
    projects_str = [" ".join(skills) for skills in projects_skills]

    corpus = [user_str] + projects_str
    vectorizer = TfidfVectorizer()

    try:
        tfidf_matrix = vectorizer.fit_transform(corpus)
    except Exception as e:
        print(f"Error in TF-IDF computation: {e}")
        return []
    
    user_vector = tfidf_matrix[0].reshape(1, -1)  # Convert to 2D
    projects_vectors = tfidf_matrix[1:]

    similarities = cosine_similarity(user_vector, projects_vectors)
    return similarities.flatten()

"""Recommends projects based on user's skills."""
def recommend_projects(user_id):
    user_skills = load_user_skills()
    user_skill_names = user_skills.get(user_id, [])

    if not user_skill_names:
        print(f"No skills found for user {user_id}.")
        return []

    project_skills = load_project_skills()

    # Compute similarity scores
    project_ids = list(project_skills.keys())
    project_skills_list = list(project_skills.values())
    
    similarity_scores = compute_similarity(user_skill_names, project_skills_list)

    # Load project details
    projects = {p["id"]: {"id": p["id"], "title": p["title"], "skills": project_skills.get(p["id"], [])} for p in load_projects()}
    
    recommended_projects = sorted(zip(project_ids, similarity_scores), key=lambda x: x[1], reverse=True)

    return [(projects[pid], score) for pid, score in recommended_projects if pid in projects]

"""Recommends users based on project's skills."""
def recommend_users(project_id):
    project_skills = load_project_skills()
    project_skill_names = project_skills.get(project_id, [])

    if not project_skill_names:
        print(f"No skills found for project {project_id}.")
        return []

    user_skills = load_user_skills()

    # Compute similarity scores
    user_ids = list(user_skills.keys())
    user_skills_list = list(user_skills.values())
    
    similarity_scores = compute_similarity(project_skill_names, user_skills_list)

    # Load user details
    users = {u["id"]: {"id": u["id"], "name": u["name"], "skills": user_skills.get(u["id"], [])} for u in load_users()}

    recommended_users = sorted(zip(user_ids, similarity_scores), key=lambda x: x[1], reverse=True)

    return [(users[uid], score) for uid, score in recommended_users if uid in users]
