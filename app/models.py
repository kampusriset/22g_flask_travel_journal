import MySQLdb
from werkzeug.security import generate_password_hash, check_password_hash

class Database:
    def __init__(self):
        self.connection = MySQLdb.connect(
            host='localhost',
            user='root',
            password='',
            database='travel_journal'
        )
        self.cursor = self.connection.cursor()

    def close(self):
        self.cursor.close()
        self.connection.close()

class Travel:
    def __init__(self, place_name, description, travel_date, cost, rating=3, username=None):
        self.place_name = place_name
        self.description = description
        self.travel_date = travel_date
        self.cost = cost
        self.rating = rating
        self.username = username

    @staticmethod
    def get_all_travels(search=None, page=1, per_page=6, count_all=False):
        db = Database()
        
        try:
            if count_all:  
                if search:
                    db.cursor.execute("""
                        SELECT * FROM travels 
                        WHERE place_name LIKE %s OR description LIKE %s
                    """, (f'%{search}%', f'%{search}%'))
                else:
                    db.cursor.execute("SELECT * FROM travels")
                travels = db.cursor.fetchall()
                return travels, 1, len(travels)
            
            offset = (page - 1) * per_page
            if search:
                db.cursor.execute("""
                    SELECT COUNT(*) FROM travels 
                    WHERE place_name LIKE %s OR description LIKE %s
                """, (f'%{search}%', f'%{search}%'))
                total = db.cursor.fetchone()[0]
                
                db.cursor.execute("""
                    SELECT id, place_name, description, travel_date, cost, rating 
                    FROM travels 
                    WHERE place_name LIKE %s OR description LIKE %s
                    ORDER BY travel_date DESC
                    LIMIT %s OFFSET %s
                """, (f'%{search}%', f'%{search}%', per_page, offset))
            else:
                db.cursor.execute("SELECT COUNT(*) FROM travels")
                total = db.cursor.fetchone()[0]
                
                db.cursor.execute("""
                    SELECT id, place_name, description, travel_date, cost, rating 
                    FROM travels 
                    ORDER BY travel_date DESC
                    LIMIT %s OFFSET %s
                """, (per_page, offset))
            
            travels = db.cursor.fetchall()
            total_pages = (total + per_page - 1) // per_page
            
            return travels, total_pages, total
        
        finally:
            db.close()

    @staticmethod
    def get_travel(travel_id):
        db = Database()
        db.cursor.execute("""
            SELECT id, place_name, description, travel_date, cost, rating 
            FROM travels 
            WHERE id = %s
        """, (travel_id,))
        travel = db.cursor.fetchone()
        db.close()
        return travel

    @staticmethod
    def create_travel(travel):
        db = Database()
        db.cursor.execute(
            """INSERT INTO travels (place_name, description, travel_date, cost, rating) 
            VALUES (%s, %s, %s, %s, %s)""",
            (travel.place_name, travel.description, travel.travel_date, 
             travel.cost, travel.rating)
        )
        db.connection.commit()
        db.close()

    @staticmethod
    def update_travel(travel_id, travel):
        db = Database()
        db.cursor.execute(
            """UPDATE travels SET place_name = %s, description = %s,
            travel_date = %s, cost = %s, rating = %s WHERE id = %s""",
            (travel.place_name, travel.description, travel.travel_date,
             travel.cost, travel.rating, travel_id)
        )
        db.connection.commit()
        db.close()

    @staticmethod
    def delete_travel(travel_id):
        db = Database()
        db.cursor.execute("DELETE FROM travels WHERE id = %s", (travel_id,))
        db.connection.commit()
        db.close()

class User:
    def __init__(self, username, password):
        self.username = username
        self.password = password

    @staticmethod
    def create_user(username, password):
        db = Database()
        hashed_password = generate_password_hash(password)
        db.cursor.execute(
            "INSERT INTO users (username, password) VALUES (%s, %s)",
            (username, hashed_password)
        )
        db.connection.commit()
        db.close()

    @staticmethod
    def check_user(username, password):
        db = Database()
        db.cursor.execute(
            "SELECT password FROM users WHERE username = %s",
            (username,)
        )
        result = db.cursor.fetchone()
        db.close()
        if result and check_password_hash(result[0], password):
            return True
        return False

    @staticmethod
    def reset_password(username, new_password):
        db = Database()
        hashed_password = generate_password_hash(new_password)
        db.cursor.execute(
            "UPDATE users SET password = %s WHERE username = %s",
            (hashed_password, username)
        )
        db.connection.commit()
        db.close()