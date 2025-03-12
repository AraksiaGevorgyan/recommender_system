from data_loader import load_users, load_projects, load_user_skills, load_project_skills

# Test loading users
users = load_users()
print("Users:", users)

# Test loading projects
projects = load_projects()
print("Projects:", projects)

# Test loading user skills
user_skills = load_user_skills()
print("User Skills:", user_skills)

# Test loading project skills
project_skills = load_project_skills()
print("Project Skills:", project_skills)
