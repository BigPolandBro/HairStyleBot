from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def create_inline_keyboard(items, callback_prefix):
    # Create a list to hold all rows
    inline_keyboard = []

    # Assuming you want four buttons per row
    row_width = 4
    for i in range(0, len(items), row_width):
        # Create each row
        row = [
            InlineKeyboardButton(text=item, callback_data=f"{callback_prefix}_{item}")
            for item in items[i:i + row_width]
        ]
        # Add the row to the inline keyboard
        inline_keyboard.append(row)

    # Create and return the InlineKeyboardMarkup
    return InlineKeyboardMarkup(inline_keyboard=inline_keyboard)

