import psycopg2
from db import dbname, user, password

# Database connection parameters
db_params = {
    'dbname': dbname,
    'user': user,
    'password': password, 
    'host': 'localhost',
    'port': '5432'
}

class MosqueDatabase:

    def __init__(self):
        # Connect to the PostgreSQL database
        self.conn = psycopg2.connect(
            dbname=dbname,
            user=user,
            password=password,
            host='localhost',
            port='5432'
        )
        self.cursor = self.conn.cursor()

        # Create the Mosques table if it doesn't exist
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS Mosques (
                id SERIAL PRIMARY KEY,
                name VARCHAR(100),
                type VARCHAR(50),
                address VARCHAR(255),
                coordinates VARCHAR(50),
                imam_name VARCHAR(100)
            );
        """)
        self.conn.commit()

    def display_mosques(self):
        self.cursor.execute("SELECT * FROM Mosques;")
        mosques = self.cursor.fetchall()
        return mosques
    
    def search(self, name):
        self.cursor.execute("SELECT * FROM Mosques WHERE name ILIKE %s;", (f"%{name}%",))
        mosques = self.cursor.fetchall()
        return mosques

    def insert(self, name, type, address, coordinates, imam_name):
        self.cursor.execute("INSERT INTO Mosques (name, type, address, coordinates, imam_name) VALUES (%s, %s, %s, %s, %s);",
                            (name, type, address, coordinates, imam_name))
        self.conn.commit()

    def update(self, mosque_id, name, type, address, coordinates, imam_name):
        self.cursor.execute("""
            UPDATE Mosques
            SET name = %s, type = %s, address = %s, coordinates = %s, imam_name = %s
            WHERE id = %s;
        """, (name, type, address, coordinates, imam_name, mosque_id))
        self.conn.commit()


    def delete(self, mosque_id):
        self.cursor.execute("DELETE FROM Mosques WHERE id = %s;", (mosque_id,))
        self.conn.commit()

    def __del__(self):
        # Close connection when object is destroyed
        if hasattr(self, 'cursor') and self.cursor:
            self.cursor.close()
        if hasattr(self, 'conn') and self.conn:
            self.conn.close()
        print("Database connection closed.")


