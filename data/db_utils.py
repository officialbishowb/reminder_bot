import sqlite3

class Database:
    
    def __init__(self) -> None:
        self.db = sqlite3.connect('bot.db')
        self.cursor = self.db.cursor()
    
    
    def create_table(self):
        """ Create the table if it doesn't exist 
        """
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS timers(
            id INTEGER PRIMARY KEY,
            user_id INTEGER,
            alert_time TEXT,
            alert_message TEXT,
            target_id TEXT
        )
        """)
        self.db.commit()
    
    def add(self, user_id, alert_time, alert_message, target_id):
        """ Add a timer to the database
        """
        self.cursor.execute("""
        INSERT INTO timers(user_id, alert_time, alert_message, target_id) VALUES(?,?,?,?)
        """, (user_id, alert_time, alert_message, target_id))
        self.db.commit()
    
    
    def delete(self, id):
        """ Delete a timer from the database with the given id
        """
        self.cursor.execute("""
        DELETE FROM timers WHERE id=?
        """, (id,))
        self.db.commit()
    
    
    def update(self, id, column, value):
        """ Update a timer from the database with the given id
        """
        self.cursor.execute(f"""
        UPDATE timers SET {column}=? WHERE id=?
        """, (value, id))
        self.db.commit()
    
    