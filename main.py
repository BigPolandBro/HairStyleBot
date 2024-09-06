import asyncio
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.types import ContentType
from aiogram.fsm.state import StatesGroup, State
from keyboard import create_inline_keyboard
import os
import requests
import time
from io import BytesIO

API_KEY = 's6l0K1wSbI2rSY0ntFlPEsRqbXdB7TXYvyCLxZi4jhMEkgrV6zNHezm9ULGJcn3O'
haircut_list = [
    "BuzzCut",
    "UnderCut",
    "Pompadour",
    "SlickBack",
    "CurlyShag",
    "WavyShag",
    "FauxHawk",
    "Spiky",
    "CombOver",
    "HighTightFade",
    "ManBun",
    "Afro"
]
color_list = [
    "blonde",
    "platinumBlonde",
    "brown",
    "lightBrown",
    "blue",
    "lightBlue",
    "purple",
    "lightPurple",
    "pink",
    "black",
]

class CurrentFunction(StatesGroup):
    wait_photo = State()
    choose_color = State()
    choose_haircut = State()
    generating_photo = State()


async def query_picture_model_(image_url: str, hair_style: str, color: str) -> str:
    try:
        return change_hairstyle(image_url, hair_style, color)
    except Exception as e:
        return f"Error querying picture model: {e}"

def change_hairstyle(image_url, hair_style='Pompadour', color='black'):
    # Скачиваем изображение по URL
    response = requests.get(image_url)
    if response.status_code != 200:
        raise ValueError(f"Не удалось скачать изображение: {response.status_code}")

    print("before downloading pic in func")

    image = BytesIO(response.content)
    image.name = 'image.jpeg'  # задаем имя файла для файла в памяти

    # Первичный URL для запроса изменения прически
    url = "https://www.ailabapi.com/api/portrait/effects/hairstyle-editor-pro"

    payload = {
        'task_type': 'async',
        'hair_style': hair_style,
        'color': color
    }

    files = [
        ('image', ('file', image, 'application/octet-stream'))
    ]

    headers = {
        'ailabapi-api-key': API_KEY
    }

    # Отправка POST-запроса для начала обработки
    response = requests.request("POST", url, headers=headers, data=payload, files=files)
    if response.status_code == 200:
        task_id = response.json().get("task_id")

        if task_id:
            # URL для проверки статуса задачи
            status_url = f"https://www.ailabapi.com/api/common/query-async-task-result?task_id={task_id}"

            # Проверка статуса задачи каждые 5 секунд
            is_complete = False
            while not is_complete:
                status_response = requests.get(status_url, headers=headers)
                if status_response.status_code == 200:
                    status_data = status_response.json()
                    if status_data.get("error_code") == 0 and status_data.get("data"):
                        # Ссылка на изображение с измененной прической
                        image_url = status_data["data"]["images"][0].replace('\\/', '/')
                        return image_url
                    else:
                        print("Задача не завершена, повторное ожидание...")
                        time.sleep(5)
                else:
                    print(f"Ошибка при проверке статуса: {status_response.status_code}")
                    break
        else:
            print("Не удалось получить task_id")
    else:
        print(f"Ошибка {response.status_code}: {response.text}")



bot_token = "7326983853:AAFui30SgU-23KWQLHpfsxYv1WDdw9artas"
replicate_token = "r8_H8O6KTTCLuhocwkOhvJRC7joiu4AvSs41RiwD"
model_version = "cjwbw/night-enhancement:4328e402cfedafa70ad7cec04412e86ab61832204deccd94108ae5222c9b1ae1"

bot = Bot(bot_token)
dp = Dispatcher()


@dp.message(Command("start"))
async def start(message: types.Message, state) -> None:
    await message.reply('Привет! Я могу изменить тебе прическу, присылай фото)')
    await state.set_state(CurrentFunction.wait_photo)



@dp.message(CurrentFunction.wait_photo)
async def handle_message(message: types.Message, state) -> None:
    if message.content_type == ContentType.PHOTO:
        photo = message.photo[-1]
        file_info = await bot.get_file(photo.file_id)
        file_url = f"https://api.telegram.org/file/bot{bot_token}/{file_info.file_path}"
        await state.update_data(file_url=file_url)
        await state.set_state(CurrentFunction.choose_haircut)
        await choosing_haircut(message, state)
    else:
        await message.reply('Присылай фото')

async def choosing_haircut(message, state):
    await message.reply("Выбери прическу", reply_markup=create_inline_keyboard(haircut_list, "haircut"))
    await state.set_state(CurrentFunction.choose_color)

# @dp.callback_query()
# async def test_callback(callback):
#     print(callback.data)

@dp.callback_query(F.data.startswith("haircut"))
async def set_haircut(callback, state):
    await state.update_data(haircut=callback.data.split('_')[1])
    print(callback.message.text)
    await choosing_color(callback.message, state)

@dp.callback_query(F.data.startswith("color"))
async def set_color(callback, state):
    await state.update_data(color=callback.data.split('_')[1])
    await state.set_state(CurrentFunction.generating_photo)
    await generate_photo(callback.message, state)


async def choosing_color(message, state):
    await message.reply("Выбери цвет", reply_markup=create_inline_keyboard(color_list, "color"))


async def generate_photo(message, state):
    user_dict = await state.get_data()
    file_url = user_dict["file_url"]
    print("before query")
    response = await query_picture_model_(file_url, user_dict["haircut"], user_dict["color"])
    print("after query")
    print(file_url)
    print(response)
    if response.startswith("Error"):
        await message.reply(response)
    else:
        await message.reply_photo(response)
    await state.set_state(CurrentFunction.wait_photo)

async def main():
    await dp.start_polling(bot)


if __name__ == '__main__':
    print("Before main call")
    asyncio.run(main())