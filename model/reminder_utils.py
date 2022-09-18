from datetime import   datetime, timedelta
from data import db_utils as db


class Reminder:
    
    def __init__(self) -> None:
        self.reminder_id = ""
        self.user_id = ""
        self.reminder = ""
        self.reminder_message = ""
        self.target_id = ""
        self.db = db.Database()
        
        
    def _reminder_init(self, reminder, user_id, reminder_id, reminder_message, target_id):
        self.reminder_id = reminder_id
        self.user_id = user_id
        self.reminder = reminder
        self.reminder_message = reminder_message
        self.target_id = target_id
        
        
    def get_datetime(self,raw_time):
        """Get the datetime from the raw time (h, m, d and hh:mm)

        Args:
            raw_time (str): the raw time eg: 1h 2m 3d 12:19

        Returns:
            tuple/bool: tuple with final_date and output_msg if the time is valid, bool if the time is invalid
        """
        
        current_datetime = datetime.now()
        output_msg = ""
        if "d" in raw_time:
            time = raw_time.replace("d", "")
            final_date = current_datetime + timedelta(days=float(time))
            output_msg = f"Set the reminder for <b>{time} days</b>?"
        elif "h" in raw_time:
            time = raw_time.replace("h", "")
            final_date = current_datetime + timedelta(hours=float(time))
            output_msg = f"Set the reminder for <b>{time} hours</b>?"
        elif "m" in raw_time:
            time = raw_time.replace("m", "")
            final_date = current_datetime + timedelta(minutes=float(time))
            output_msg = "Set the reminder for <b>{time} minutes</b>?"
        elif ":" in raw_time:
            print("here")
            print(raw_time)
            time = raw_time.split(":")
            if int(time[0]) <= datetime.now().hour & int(time[1]) < datetime.now().minute:
                final_date = current_datetime.replace(days=1,hour=int(time[0]), minute=int(time[1]), second=0, microsecond=0)
                output_msg = f"Set the reminder for tommorrow at <b>{time[0]}hour and {time[1]}minute</b>?"
            else:
                final_date = current_datetime.replace(hour=int(time[0]), minute=int(time[1]), second=0, microsecond=0)
                output_msg = f"Set the reminder for today at <b>{time[0]} hour and {time[1]} minutes</b>?"
        else:
            return False
        return final_date, output_msg
    
    

    def datetime_to_str(self,datetime):
        """Convert a datetime to a string

        Args:
            datetime (datetime): the datetime

        Returns:
            str: the string datetime
        """
        return datetime.strftime("%Y-%m-%d %H:%M:%S")
    
    def str_to_datetime(self,string_date):
        """Convert a string to a datetime

        Args:
            datetime (str): the string datetime

        Returns:
            datetime: the datetime
        """
        return datetime.strptime(string_date, "%Y-%m-%d %H:%M:%S")

    
    def add(self):
        """Add the reminder to the database
        """
        self.db.add(self.reminder_id, self.user_id, self.reminder, self.reminder_message, self.target_id)
    
    
    def gen_id(self):
        """Generate a random id with utcnow

        Returns:
            str: The id
        """
        return datetime.utcnow().strftime("%Y%m%d%H%M%S")
        