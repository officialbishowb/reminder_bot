import logging
import os, time
from dotenv import load_dotenv
load_dotenv()

from aiogram import Bot, Dispatcher, executor, types


from model import timer_utils as tu
from data import *
from btns import *

tu = tu.Timer()
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
async def timer(message: types.Message):
    
    # Command to set a timer
    if message.text.startswith("/timer"):
        timer_info = message.text[7:].split(" ")
        if len(timer_info) < 2:
            await message.reply("<b>Please enter a valid time and message.</b>")
            return
        response = tu.get_datetime(timer_info[0])
        # Timer info
        timer_to_set = tu.datetime_to_srt(response[0])
        timer_message = timer_info[1]
        timer_id = tu.gen_id()
        target_id = message.from_user.id
        tu.__init__(timer_to_set, timer_id, timer_message, target_id)
        
        
        
        response[1] += f"\nWith the message: <code>{timer_message}</code>?"
        if type(response) != tuple:
            await message.reply("<b>Please enter a valid time.</b>")
            return
        await message.reply(f"{response[1]}",reply_markup=timer_btn)
        
    
    # Command to get all the timers
    elif message.text.startswith("/get"):
        return "get"
    
    # Command to cancel a timer
    elif message.text.startswith("/cancel"):
        return "cancel"







#================================== [Timer callback query handler] ==================================#
@dp.callback_query_handler(text =  ["confirm_timer", "cancel_timer"])
async def timer_callback(callback_query: types.CallbackQuery):
    
    if callback_query.data == "confirm_timer":
        tu.add() # Add the timer to the database
        await bot.edit_message_text(chat_id=callback_query.message.chat.id, message_id=callback_query.message.message_id, text="<b>Timer set!</b>")
        
    elif callback_query.data == "cancel_timer":
        await bot.edit_message_text(chat_id=callback_query.message.chat.id, message_id=callback_query.message.message_id, text="<b>Timer cancelled!</b>")



if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)