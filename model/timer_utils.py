from datetime import  datetime, timedelta
from data import db_utils as db


class Timer:
    
    def __init__(self) -> None:
        self.timer = ""
        self.timer_id = ""
        self.timer_message = ""
        self.target_id = ""
        self.db = db.Database()
        
        
    def __init__(self, timer, timer_id, timer_message, target_id):
        self.timer = timer
        self.timer_id = timer_id
        self.timer_message = timer_message
        self.target_id = target_id
        
        
    def get_datetime(raw_time):
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
            output_msg = f"Set the timer for <b>{time} days</b>?"
        elif "h" in raw_time:
            time = raw_time.replace("h", "")
            final_date = current_datetime + timedelta(hours=float(time))
            output_msg = f"Set the timer for <b>{time} hours</b>?"
        elif "m" in raw_time:
            time = raw_time.replace("m", "")
            final_date = current_datetime + timedelta(minutes=float(time))
            output_msg = "Set the timer for <b>{time} minutes</b>?"
        elif ":" in raw_time:
            time = raw_time.split(":")
            final_date = current_datetime.replace(hour=int(time[0]), minute=int(time[1]), second=0, microsecond=0)
            output_msg = f"Set the timer for <b>{time[0]}hour and {time[1]}minute</b>?"
        else:
            return False
        return final_date, output_msg
    
    

    def datetime_to_str(datetime):
        """Convert a datetime to a string

        Args:
            datetime (datetime): the datetime

        Returns:
            str: the string datetime
        """
        return datetime.strftime("%Y-%m-%d %H:%M:%S")
    

    
    def add(self):
        """Add the timer to the database
        """
        self.db.add(self.timer, self.timer_id, self.timer_message, self.target_id)
    
    
    def gen_id(self):
        """Generate a random id with utcnow

        Returns:
            int: The id
        """
        return int(datetime.utcnow().strftime("%Y%m%d%H%M%S"))
        