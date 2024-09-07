from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

# def create_inline_keyboard(options, callback_prefix):
#     # Create a list to hold all rows
#     inline_keyboard = []
#
#     # Assuming you want four buttons per row
#     row_width = 4
#     # print(options.eng_list)
#     # print(options.eng2rus)
#     for i in range(0, len(options.eng_list), row_width):
#         # Create each row
#         row = [
#             InlineKeyboardButton(text=options.translate2rus(item), callback_data=f"{callback_prefix}_{item}")
#             for item in options.eng_list[i:i + row_width]
#         ]
#         # Add the row to the inline keyboard
#         inline_keyboard.append(row)
#     #     print(row)
#     # print(inline_keyboard)
#
#     # Create and return the InlineKeyboardMarkup
#     return InlineKeyboardMarkup(inline_keyboard=inline_keyboard)

def create_inline_keyboard(options, callback_prefix, current_page=0, items_per_page=6):
    # Calculate total pages
    total_items = len(options.eng_list)
    total_pages = (total_items + items_per_page - 1) // items_per_page  # round up the total pages

    # Determine the start and end index of the items for the current page
    start_index = current_page * items_per_page
    end_index = min(start_index + items_per_page, total_items)

    # Slice the list of items
    items_to_display = options.eng_list[start_index:end_index]

    # Create a list to hold all rows
    inline_keyboard = []

    row_width = 3
    for i in range(0, len(items_to_display), row_width):
        row = [
            InlineKeyboardButton(text=options.translate2rus(item), callback_data=f"{callback_prefix}_{item}")
            for item in items_to_display[i:i + row_width]
        ]
        # Add the row to the inline keyboard
        inline_keyboard.append(row)

    # Navigation buttons
    if total_pages > 1:
        navigation_row = []
        if current_page > 0:
            navigation_row.append(
                InlineKeyboardButton(
                    text="⬅️ Назад",
                    callback_data=f"{callback_prefix}_page_{current_page - 1}"
                )
            )
        if current_page < total_pages - 1:
            navigation_row.append(
                InlineKeyboardButton(
                    text="Вперед ➡️",
                    callback_data=f"{callback_prefix}_page_{current_page + 1}"
                )
            )
        inline_keyboard.append(navigation_row)

    # Create and return the InlineKeyboardMarkup
    return InlineKeyboardMarkup(inline_keyboard=inline_keyboard)


