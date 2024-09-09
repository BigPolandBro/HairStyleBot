from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from options import callback_options


class KeyboardFactory:
    def __init__(self, callback_prefix, current_page=0, items_per_page=6):
        self.callback_prefix = callback_prefix
        self.options = callback_options[callback_prefix]
        self.current_page = current_page
        self.items_per_page = items_per_page
        print(self.callback_prefix, self.options)

    def create_keyboard(self):
        if self.callback_prefix in ["haircut", "color"]:
            return self.create_paged_keyboard()
        elif "show" in self.callback_prefix:  # для отображения фотографий с выбором
            return self.create_selection_keyboard()
        else:
            return InlineKeyboardMarkup()  # Пустая клавиатура по умолчанию

    def create_paged_keyboard(self):
        total_items = len(self.options.options_list)
        total_pages = (total_items + self.items_per_page - 1) // self.items_per_page

        start_index = self.current_page * self.items_per_page
        end_index = min(start_index + self.items_per_page, total_items)

        items_to_display = self.options.options_list[start_index:end_index]

        inline_keyboard = []

        row_width = 3  # Number of buttons per row
        for i in range(0, len(items_to_display), row_width):
            row = [
                InlineKeyboardButton(
                    text=self.options.option_to_name(item),
                    callback_data=f"{self.callback_prefix}_{item}"
                )
                for item in items_to_display[i:i + row_width]
            ]
            inline_keyboard.append(row)

        if total_pages > 1:
            navigation_row = []
            if self.current_page > 0:
                navigation_row.append(
                    InlineKeyboardButton(
                        text="⬅️ Назад",
                        callback_data=f"{self.callback_prefix}_page_{self.current_page - 1}"
                    )
                )
            if self.current_page < total_pages - 1:
                navigation_row.append(
                    InlineKeyboardButton(
                        text="Вперед ➡️",
                        callback_data=f"{self.callback_prefix}_page_{self.current_page + 1}"
                    )
                )
            inline_keyboard.append(navigation_row)

        return InlineKeyboardMarkup(inline_keyboard=inline_keyboard)

    def create_selection_keyboard(self):
        inline_keyboard = [
            [
                InlineKeyboardButton(text="Назад", callback_data=f"{self.callback_prefix}_back"),
                InlineKeyboardButton(text="Выбрать", callback_data=f"{self.callback_prefix}_select")
            ]
        ]
        return InlineKeyboardMarkup(inline_keyboard=inline_keyboard)


