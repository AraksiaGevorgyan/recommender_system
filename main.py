from fastapi import FastAPI, HTTPException, BackgroundTasks
from recommend import recommend_projects, recommend_users
from data_loader import cache, load_users, load_projects, load_user_skills, load_project_skills
app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Recommender API is running!"}

@app.get("/recommend_projects/{user_id}")
def get_project_recommendations(user_id: int):
    try:
        return recommend_projects(user_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    
@app.get("/recommend_users/{project_id}")
def get_user_recommendations(project_id: int):
    try:
        return recommend_users(project_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    
@app.get("/refresh_cache")
def refresh_cache(bg_tasks: BackgroundTasks):
    bg_tasks.add_task(load_users)
    bg_tasks.add_task(load_projects)
    bg_tasks.add_task(load_user_skills)
    bg_tasks.add_task(load_project_skills)
    return {"message": "Cache refresh started in background."}
