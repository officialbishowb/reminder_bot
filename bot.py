import logging
import os
from dotenv import load_dotenv
from datetime import datetime
import data
load_dotenv()

from aiogram import Bot, Dispatcher, types
from aiogram.types import ChatType



from model import timer_utils as tu
from data import *
from btns import *

tu = tu.Timer()
db = Database()
## Bot Initialization
bot = Bot(token=os.getenv("BOT_TOKEN"),parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot)
# Configure logging
logging.basicConfig(level=logging.INFO)



@dp.message_handler(commands=['start', 'help'], chat_type=[ChatType.PRIVATE])
async def start(message: types.Message):
    if message.text.startswith("/start"):
        await message.answer("Hello, I'm a timer bot! I can help you to set a timer for you. \nSend /help to see more info and the commands.")
    elif message.text.startswith("/help"):
        await message.answer( """
Send me a message like this: <code>/timer 10m Homework</code>, and I will remind you in <b>10 minutes</b> for your <b>Homework</b>.
 
You can also use <b>h</b> for hours,  <b>d</b> for days or even a time (eg: 12:19) in 24hrs format. For example: <code>/timer 1d or 2h or 3m</code>.

Commands:
/start - Start the bot
/help - Show this message

/timer - Set a timer
/get - Get all the timers
/cancel - <code>id</code> Cancel the timer""")
        
#================================== [Timer message handler] ==================================#
@dp.message_handler(commands=['timer', 'get', 'cancel'], chat_type=[ChatType.PRIVATE])
async def timer(message: types.Message):
    
    # Command to set a timer
    if message.text.startswith("/timer"):
        timer_info = message.text[7:].split(" ", 1)
        if len(timer_info) < 2:
            await message.reply("<b>Please enter a valid time and message.</b>")
            return
        response = tu.get_datetime(timer_info[0])
        if type(response) != tuple:
            await message.reply("<b>Invalid time. Please make sure the time format is valid!</b>")    
            return
        
        # Timer info
        timer_to_set = tu.datetime_to_str(response[0])
        timer_message = timer_info[1]
        timer_id = tu.gen_id()
        target_id = str(message.from_user.id)
        user_id = message.from_user.id
        tu._timer_init(timer_to_set, user_id, timer_id, timer_message, target_id)
        
        final_response = response[1]
        final_response += f"\nWith the message: <code>{timer_message}</code>?"
        await message.reply(f"{final_response}",reply_markup=timer_btn)
        
    
    # Command to get all the timers
    elif message.text.startswith("/get"):
        timer_output =""
        timers = db.get(message.from_user.id)
        if timers:
            for timer in timers:
                timer_output += f"\n━━━━━━━━━━━━━\n<b>Timer ID:</b> <code>{timer[0]}</code>\n<b>Timer at:</b> <code>{timer[2]}</code>\n<b>Message:</b> <code>{timer[3]}</code>"
            await message.reply(f"{timer_output}")
            return 
        await message.reply("<b>You don't have any timers set.</b>\nType <code>/timer time message</code> to set a timer.")
    
    # Command to cancel a timer
    elif message.text.startswith("/cancel"):
        timer_id = message.text[8:]
        if timer_id == "":
            await message.reply("<b>Please enter a valid timer ID.</b>\nType /get to get all the timers.")
            return
        response = db.delete(timer_id)
        if response:
            await message.reply(f"<b>Timer has been deleted.</b>")
            return
        await message.reply(f"<b>Timer could not be deleted. Make sure that the timer ID is correct!</b>\nType /get to get all the timers.")



###================================== [Timer notifier] ==================================#
from apscheduler.schedulers.asyncio import AsyncIOScheduler
import asyncio

# ======= [Scheduler Initialization] ====== #
loop = asyncio.get_event_loop()
scheduler = AsyncIOScheduler(event_loop = loop)

async def timer_notifier():
    
    get_timers = db.get("")
    if get_timers:
        for timer in get_timers:
            alert_time = tu.str_to_datetime(timer[2])
            current_time = tu.str_to_datetime(tu.datetime_to_str(datetime.now()))
            target_id = timer[4]
            if current_time >= alert_time:
                await bot.send_message(target_id, f"⌛️ <b>Timer Alert</b> ⌛️\n\n<code>{timer[3]}</code>")
                db.delete(timer[0])

scheduler.add_job(timer_notifier, "interval", seconds=2)

#================================== [Timer callback query handler] ==================================#
@dp.callback_query_handler(text =  ["confirm_timer", "cancel_timer"])
async def timer_callback(callback_query: types.CallbackQuery):
    
    if callback_query.data == "confirm_timer":
        tu.add() # Add the timer to the database
        await bot.edit_message_text(chat_id=callback_query.message.chat.id, message_id=callback_query.message.message_id, text="<b>Timer set!</b>")
        
    elif callback_query.data == "cancel_timer":
        await bot.edit_message_text(chat_id=callback_query.message.chat.id, message_id=callback_query.message.message_id, text="<b>Timer cancelled!</b>")

# Coming soon
# #================================== [Add Time callback query handler] ==================================#
# @dp.callback_query_handler(text =  ["5_min_timer", "10_min_timer"])
# async def timer_callback(callback_query: types.CallbackQuery):
    
#     if callback_query.data == "5_min_timer":
#         tu.add() # Add the timer to the database
#         await bot.edit_message_text(chat_id=callback_query.message.chat.id, message_id=callback_query.message.message_id, text="<b>Timer set!</b>")
        
#     elif callback_query.data == "10_min_timer":
#         await bot.edit_message_text(chat_id=callback_query.message.chat.id, message_id=callback_query.message.message_id, text="<b>Timer cancelled!</b>")




if __name__ == '__main__':
    scheduler.start()
    loop.create_task(dp.start_polling())
    loop.run_forever()