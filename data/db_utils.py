import sqlite3

class Database:
    
    def __init__(self) -> None:
        self.db = sqlite3.connect('bot.db')
        self.cursor = self.db.cursor()
    
    
    def create_table(self):
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
        
    