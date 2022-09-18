import sqlite3

class Database:
    
    def __init__(self) -> None:
        self.db = sqlite3.connect('bot.db')
        self.cursor = self.db.cursor()
        self.create_table()
    
    
    def create_table(self):
        """ Create the table if it doesn't exist 
        """
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS reminders(
            id INTEGER PRIMARY KEY,
            user_id INTEGER,
            alert_time TEXT,
            alert_message TEXT,
            target_id TEXT
        )
        """)
        self.db.commit()
    
    def add(self, reminder_id, user_id, alert_time, alert_message, target_id):
        """ Add a reminder to the database
        """
        self.cursor.execute("""
        INSERT INTO reminders(id, user_id, alert_time, alert_message, target_id) VALUES(?,?,?,?,?)
        """, (reminder_id, user_id, alert_time, alert_message, target_id))
        self.db.commit()
    
    
    def delete(self, id):
        """ Delete a reminder from the database with the given id
        """
        response = self.cursor.execute("""
        DELETE FROM reminders WHERE id=?
        """, (id,))
        self.db.commit()
        if response.rowcount:
            return True
        return False
    
    
    def update(self, id, column, value):
        """ Update a reminder from the database with the given id
        """
        self.cursor.execute(f"""
        UPDATE reminders SET {column}=? WHERE id=?
        """, (value, id))
        self.db.commit()
    
    
    def get(self,user_id):
        """Get all reminder from a user

        Args:
            user_id (int): the user id (optional)

        Returns:
            list: the list of reminders
        """
        if user_id != "":
            response = self.cursor.execute("""
            SELECT * FROM reminders WHERE user_id=?
            """, (user_id,))
            return self.cursor.fetchall()
        self.cursor.execute("""SELECT * FROM reminders""",)
        return self.cursor.fetchall()
            
    