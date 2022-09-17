from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

# ================================== [Confirm / Cancel timer btn] ================================== #
confirm_timer = InlineKeyboardButton(text="Set the timer", callback_data="confirm_timer")
cancel_timer = InlineKeyboardButton(text="Cancel the timer", callback_data="cancel_timer")
timer_btn = InlineKeyboardMarkup().add(confirm_timer, cancel_timer)

# # ================================== [Add time to current timer btn] ================================== #
# five_min_timer = InlineKeyboardButton(text="+5 minutes", callback_data="5_min_timer")
# ten_min_timer = InlineKeyboardButton(text="+10 minutes", callback_data="10_min_timer")
# add_timer_btn = InlineKeyboardMarkup().add(five_min_timer, ten_min_timer)