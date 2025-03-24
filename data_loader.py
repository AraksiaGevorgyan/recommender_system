import mysql.connector
from mysql.connector import pooling
import os
from dotenv import load_dotenv
from cachetools import TTLCache

load_dotenv()
DB_CONFIG = {
    "host": os.getenv("DB_HOST"),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD"),
    "database": os.getenv("DB_NAME"),
}

connection_pool = pooling.MySQLConnectionPool(pool_name="mypool", pool_size=10, **DB_CONFIG)
cache = TTLCache(maxsize=1000,ttl=300)

def fetch_query(query, params = None):
    conn = connection_pool.get_connection()
    try:
        with conn.cursor(dictionary = True) as cursor:
            cursor.execute(query, params or ())
            return cursor.fetchall()
    except mysql.connector.Error as e:
        print(f"Error fetching data: {e}")
        return []
    finally:
        if conn:
            conn.close()

def load_users():
    if "users" in cache:
        return cache["users"]
    users = fetch_query("SELECT * FROM users")
    cache["users"] = users
    return users

def load_projects():
    if "projects" in cache:
        return cache["projects"]
    projects = fetch_query("SELECT * FROM projects")
    cache["projects"] = projects
    return projects

def load_user_skills():
    if "user_skills" in cache:
        return cache["user_skills"]
    query = """
        SELECT u.id AS user_id, IFNULL(GROUP_CONCAT(s.name SEPARATOR ', '), '') AS skills
        FROM user_skills us
        RIGHT JOIN users u ON us.user_id = u.id
        LEFT JOIN skills s ON us.skill_id = s.id
        GROUP BY u.id
    """
    data = fetch_query(query)
    user_skills = {row["user_id"]: row["skills"].split(", ") if row["skills"] else [] for row in data}
    cache["user_skills"] = user_skills
    return user_skills


def load_project_skills():
    if "project_skills" in cache:
        return cache["project_skills"]
    query = """
        SELECT p.id AS project_id, IFNULL(GROUP_CONCAT(s.name SEPARATOR ', '), '') AS skills
        FROM project_skills ps
        JOIN projects p ON ps.project_id = p.id
        JOIN skills s ON ps.skill_id = s.id
        GROUP BY p.id
    """
    data = fetch_query(query)
    project_skills = {row["project_id"]: row["skills"].split(", ") if row["skills"] else [] for row in data}
    cache["project_skills"] = project_skills
    return project_skills