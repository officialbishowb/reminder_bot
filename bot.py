import logging
import os, time
from dotenv import load_dotenv
load_dotenv()
from datetime import datetime

from aiogram import Bot, Dispatcher, executor, types


from model  import functions as func
from data import *
## Bot Initialization
bot = Bot(token=os.getenv("BOT_TOKEN"),parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot)
# Configure logging
logging.basicConfig(level=logging.INFO)



@dp.message_handler(commands=['start', 'help'])
async def start(message: types.Message):
    if message.text.startswith("/start"):
        await message.answer("Hello, I'm a timer bot! I can help you to set a timer for you. \nSend /help to see more info and the commands.")
    elif message.text.startswith("/help"):
        await message.answer( """
Send me a message like this: <code>/timer 10m Homework</code>, and I will remind you in <b>10 minutes</b> for your <b>Homework</b>.
 
You can also use <b>h</b> for hours,  <b>d</b> for days or even a time (eg: 12:19). For example: <code>/timer 1d 2h 3m</code> - alert in 1 day, 2 hours and 3 minutes.

Commands:
/start - Start the bot
/help - Show this message

/timer - Set a timer
/get - Get all the timers
/cancel - <code>id</code> Cancel the timer""")
        
#================================== [Timer message handler] ==================================#
@dp.message_handler(commands=['timer', 'get', 'cancel'])
def timer(message: types.Message):
    
    # Command to set a timer
    if message.text.startswith("/timer"):
        timer_info = message.text[6:].split(" ")
        if len(timer_info) < 2:
            message.reply("<b>Please enter a valid time and message.</b>")
            return
        get_datetime = func.get_datetime(timer_info[0])
        if not get_datetime:
            message.reply("<b>Please enter a valid time.</b>")
            return
        
            
        
    
    # Command to get all the timers
    elif message.text.startswith("/get"):
        return "get"
    
    # Command to cancel a timer
    elif message.text.startswith("/cancel"):
        return "cancel"
        
if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)