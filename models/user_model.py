from utils.db import get_db_connection

class UserModel:
    @staticmethod
    def get_user_by_username(username):
        conn = get_db_connection()
        if not conn:
            return None
        try:
            with conn.cursor() as cursor:
                cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
                return cursor.fetchone()
        finally:
            conn.close()

    @staticmethod
    def create_user(username, password_hash):
        conn = get_db_connection()
        if not conn:
            return False
        try:
            with conn.cursor() as cursor:
                cursor.execute("INSERT INTO users (username, password_hash) VALUES (%s, %s)", (username, password_hash))
            conn.commit()
            return True
        except Exception:
            return False
        finally:
            conn.close()
