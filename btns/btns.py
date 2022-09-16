from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

# ================================== [Confirm / Cancel timer btn] ================================== #
confirm_timer = InlineKeyboardButton(text="Set the timer", callback_data="confirm_timer")
cancel_timer = InlineKeyboardButton(text="Cancel the timer", callback_data="cancel_timer")
timer_btn = InlineKeyboardMarkup().add(confirm_timer, cancel_timer)