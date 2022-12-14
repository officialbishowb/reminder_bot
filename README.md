# Reminder Bot

## A simple bot that allows you to set a reminder on telegram

### Files
- `bot.py` - The main bot file
- `model/reminder_utils.py` - Functions required for the reminder
- `data/db_utils.py` - Functions required for the database
- `btns/btns.py` - Buttons for the bot


### How to use
1. Clone the repository
2. Create an .env file with the following variables:
    - `BOT_TOKEN`: Your bot token
3. Run `pip install -r requirements.txt`
4. Finally, run `python bot.py`

### Commands
- `/start`: Start the bot
- `/help`: Show the help message with all the commands and an info message
- `/reminder` - Set the reminder
- `/get` - Get all the reminders for the current user
- `/cancel` - Cancel the reminder with the given id

---
Bug report can be done at the Issues sections. If you have any ideas, feel free to open a pull request or tell me on [telegram](https://t.me/officialbishowb).