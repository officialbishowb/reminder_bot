from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

# ================================== [Confirm / Cancel reminder btn] ================================== #
confirm_reminder = InlineKeyboardButton(text="Set the reminder", callback_data="confirm_reminder")
cancel_reminder = InlineKeyboardButton(text="Cancel the reminder", callback_data="cancel_reminder")
reminder_btn = InlineKeyboardMarkup().add(confirm_reminder, cancel_reminder)

# # ================================== [Add time to current reminder btn] ================================== #
# five_min_reminder = InlineKeyboardButton(text="+5 minutes", callback_data="5_min_reminder")
# ten_min_reminder = InlineKeyboardButton(text="+10 minutes", callback_data="10_min_reminder")
# add_reminder_btn = InlineKeyboardMarkup().add(five_min_reminder, ten_min_reminder)