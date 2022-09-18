import logging
import os
from dotenv import load_dotenv
from datetime import datetime
import data
load_dotenv()

from aiogram import Bot, Dispatcher, types
from aiogram.types import ChatType



from model import reminder_utils as tu
from data import *
from btns import *

tu = tu.reminder()
db = Database()
## Bot Initialization
bot = Bot(token=os.getenv("BOT_TOKEN"),parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot)
# Configure logging
logging.basicConfig(level=logging.INFO)



@dp.message_handler(commands=['start', 'help'], chat_type=[ChatType.PRIVATE])
async def start(message: types.Message):
    if message.text.startswith("/start"):
        await message.answer("Hello, I'm a reminder bot! I can help you to set a reminder for you. \nSend /help to see more info and the commands.")
    elif message.text.startswith("/help"):
        await message.answer( """
Send me a message like this: <code>/reminder 10m Homework</code>, and I will remind you in <b>10 minutes</b> for your <b>Homework</b>.
 
You can also use <b>h</b> for hours,  <b>d</b> for days or even a time (eg: 12:19) in 24hrs format. For example: <code>/reminder 1d or 2h or 3m</code>.

Commands:
/start - Start the bot
/help - Show this message

/reminder - Set a reminder
/get - Get all the reminders
/cancel - <code>id</code> Cancel the reminder""")
        
#================================== [reminder message handler] ==================================#
@dp.message_handler(commands=['reminder', 'get', 'cancel'], chat_type=[ChatType.PRIVATE])
async def reminder(message: types.Message):
    
    # Command to set a reminder
    if message.text.startswith("/reminder"):
        reminder_info = message.text[7:].split(" ", 1)
        if len(reminder_info) < 2:
            await message.reply("<b>Please enter a valid time and message.</b>")
            return
        response = tu.get_datetime(reminder_info[0])
        if type(response) != tuple:
            await message.reply("<b>Invalid time. Please make sure the time format is valid!</b>")    
            return
        
        # reminder info
        reminder_to_set = tu.datetime_to_str(response[0])
        reminder_message = reminder_info[1]
        reminder_id = tu.gen_id()
        target_id = str(message.from_user.id)
        user_id = message.from_user.id
        tu._reminder_init(reminder_to_set, user_id, reminder_id, reminder_message, target_id)
        
        final_response = response[1]
        final_response += f"\nWith the message: <code>{reminder_message}</code>?"
        await message.reply(f"{final_response}",reply_markup=reminder_btn)
        
    
    # Command to get all the reminders
    elif message.text.startswith("/get"):
        reminder_output =""
        reminders = db.get(message.from_user.id)
        if reminders:
            for reminder in reminders:
                reminder_output += f"\n━━━━━━━━━━━━━\n<b>Reminder ID:</b> <code>{reminder[0]}</code>\n<b>Reminder time:</b> <code>{reminder[2]}</code>\n<b>Message:</b> <code>{reminder[3]}</code>"
            await message.reply(f"{reminder_output}")
            return 
        await message.reply("<b>You don't have any reminders set.</b>\nType <code>/reminder time message</code> to set a reminder.")
    
    # Command to cancel a reminder
    elif message.text.startswith("/cancel"):
        reminder_id = message.text[8:]
        if reminder_id == "":
            await message.reply("<b>Please enter a valid reminder ID.</b>\nType /get to get all the reminders.")
            return
        response = db.delete(reminder_id)
        if response:
            await message.reply(f"<b>Reminder has been deleted.</b>")
            return
        await message.reply(f"<b>Reminder could not be deleted. Make sure that the reminder ID is correct!</b>\nType /get to get all the reminders.")



###================================== [reminder notifier] ==================================#
from apscheduler.schedulers.asyncio import AsyncIOScheduler
import asyncio

# ======= [Scheduler Initialization] ====== #
loop = asyncio.get_event_loop()
scheduler = AsyncIOScheduler(event_loop = loop)

async def reminder_notifier():
    
    get_reminders = db.get("")
    if get_reminders:
        for reminder in get_reminders:
            alert_time = tu.str_to_datetime(reminder[2])
            current_time = tu.str_to_datetime(tu.datetime_to_str(datetime.now()))
            target_id = reminder[4]
            if current_time >= alert_time:
                await bot.send_message(target_id, f"⌛️ <b>Reminder Alert</b> ⌛️\n\n<code>{reminder[3]}</code>")
                db.delete(reminder[0])

scheduler.add_job(reminder_notifier, "interval", seconds=2)

#================================== [reminder callback query handler] ==================================#
@dp.callback_query_handler(text =  ["confirm_reminder", "cancel_reminder"])
async def reminder_callback(callback_query: types.CallbackQuery):
    
    if callback_query.data == "confirm_reminder":
        tu.add() # Add the reminder to the database
        await bot.edit_message_text(chat_id=callback_query.message.chat.id, message_id=callback_query.message.message_id, text="<b>Reminder set!</b>")
        
    elif callback_query.data == "cancel_reminder":
        await bot.edit_message_text(chat_id=callback_query.message.chat.id, message_id=callback_query.message.message_id, text="<b>Reminder cancelled!</b>")

# Coming soon
# #================================== [Add Time callback query handler] ==================================#
# @dp.callback_query_handler(text =  ["5_min_reminder", "10_min_reminder"])
# async def reminder_callback(callback_query: types.CallbackQuery):
    
#     if callback_query.data == "5_min_reminder":
#         tu.add() # Add the reminder to the database
#         await bot.edit_message_text(chat_id=callback_query.message.chat.id, message_id=callback_query.message.message_id, text="<b>reminder set!</b>")
        
#     elif callback_query.data == "10_min_reminder":
#         await bot.edit_message_text(chat_id=callback_query.message.chat.id, message_id=callback_query.message.message_id, text="<b>reminder cancelled!</b>")




if __name__ == '__main__':
    scheduler.start()
    loop.create_task(dp.start_polling())
    loop.run_forever()