import mysql.connector
from mysql.connector import pooling
import os
from dotenv import load_dotenv

load_dotenv()
DB_CONFIG = {
    "host": os.getenv("DB_HOST"),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD"),
    "database": os.getenv("DB_NAME"),
}

connection_pool = pooling.MySQLConnectionPool(pool_name="mypool", pool_size=10, **DB_CONFIG)

def connect_db():
    try:
        return connection_pool.get_connection()
    except mysql.connector.Error as e:
        print(f"Error: unable to connect to the database - {e}")
        return None

def load_users():
    conn = connect_db()
    if conn is None:
        return []
    try:   
        cursor = conn.cursor(dictionary=True)  
        cursor.execute("SELECT * FROM users")
        users = cursor.fetchall()
        return users
    except mysql.connector.Error as e:
        print("Error fetching users: ", e)
        return []
    finally:
        if conn.is_connected():
            conn.close()

def load_projects():
    conn = connect_db()
    if conn is None:
        return []
    try:
        cursor = conn.cursor(dictionary=True)  
        cursor.execute("SELECT * FROM projects")  
        projects = cursor.fetchall()
        return projects  
    except mysql.connector.Error as e:
        print("Error fetching projects: ", e)
        return []
    finally:
        if conn:
            conn.close()

def load_user_skills():
    conn = connect_db()
    if conn is None:
        return {}
    try:
        with conn.cursor(dictionary=True) as cursor:
            cursor.execute("""
                SELECT u.id AS user_id, IFNULL(GROUP_CONCAT(s.name SEPARATOR ', '), '') AS skills
                FROM user_skills us
                RIGHT JOIN users u ON us.user_id = u.id
                LEFT JOIN skills s ON us.skill_id = s.id
                GROUP BY u.id 
            """)
            user_skills = {
                row["user_id"]: row["skills"].split(", ") if row["skills"] else [] 
                for row in cursor.fetchall()
            }
        return user_skills
    except mysql.connector.Error as e:
        print("Error fetching user skills: ", e)
        return {}
    finally:
        if conn:
            conn.close()

def load_project_skills():
    conn = connect_db()
    if conn is None:
        return {}
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""
            SELECT p.id AS project_id, IFNULL(GROUP_CONCAT(s.name SEPARATOR ', '), '') AS skills
            FROM project_skills ps
            JOIN projects p ON ps.project_id = p.id
            JOIN skills s ON ps.skill_id = s.id
            GROUP BY p.id
        """)
        project_skills = {row["project_id"]: row["skills"].split(", ") if row ["skills"] else [] for row in cursor.fetchall()}
        return project_skills
    except mysql.connector.Error as e:
        print("Error fetching project skills: ", e)
        return {}
    finally:
        if conn:
            conn.close()
