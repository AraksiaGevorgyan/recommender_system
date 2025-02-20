from fastapi import FastAPI, HTTPException
from recommend import recommend_projects, recommend_users

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Recommender API is running"}

@app.get("/recommend_projects/{user_id}")
def get_project_recommendations(user_id: int):
    try:
        recommendations = recommend_projects(user_id)
        return recommendations
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    
@app.get("/recommend_users/{project_id}")
def get_user_recommendations(project_id: int):
    try:
        recommendations = recommend_users(project_id)
        return recommendations
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
