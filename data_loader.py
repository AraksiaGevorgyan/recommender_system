import mysql.connector

DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "050808",
    "database": "recommender_system"
}

def connect_db():
    return mysql.connector.connect(**DB_CONFIG)

def load_users():
    conn = connect_db()
    cursor = conn.cursor(dictionary=True)  
    cursor.execute("SELECT * FROM users")
    users = cursor.fetchall()
    conn.close()
    return users

def load_projects():
    conn = connect_db()
    cursor = conn.cursor(dictionary=True)  
    cursor.execute("SELECT * FROM projects")  
    projects = cursor.fetchall()
    conn.close()
    return projects

def load_user_skills():
    """Fetch user skills and return a dictionary with user_id as keys and lists of skill names as values."""
    conn = connect_db()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT u.id AS user_id, GROUP_CONCAT(s.name SEPARATOR ', ') AS skills
        FROM user_skills us
        JOIN users u ON us.user_id = u.id
        JOIN skills s ON us.skill_id = s.id
        GROUP BY u.id
    """)
    user_skills = {row["user_id"]: row["skills"].split(", ") for row in cursor.fetchall()}
    conn.close()
    return user_skills

def load_project_skills():
    """Fetch project skills and return a dictionary with project_id as keys and lists of skill names as values."""
    conn = connect_db()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT p.id AS project_id, GROUP_CONCAT(s.name SEPARATOR ', ') AS skills
        FROM project_skills ps
        JOIN projects p ON ps.project_id = p.id
        JOIN skills s ON ps.skill_id = s.id
        GROUP BY p.id
    """)
    project_skills = {row["project_id"]: row["skills"].split(", ") for row in cursor.fetchall()}
    conn.close()
    return project_skills
