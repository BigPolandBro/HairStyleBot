import asyncio
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.types import ContentType, FSInputFile
from aiogram.fsm.state import StatesGroup, State
from keyboard import create_inline_keyboard
import os
import requests
import time
from io import BytesIO
from datetime import datetime
from APIKeyManager import APIKeyManager
from PIL import Image, ImageFilter


api_keys_list = ['XXjL90yUJYO2RsocHN0pFeS2ZGhNKLKGhq3OeEirWQ146Id5mxMlAnPVCwbEl4Jo',
                 'vjSdUng03HfgqVuMrlmJibDFA7KhVRUoeYFPP3qiBzT2wHwzWLZLGackExsYJRlf',
                 '0coH412v8qKpVoYJBAi59wesW9MdgGYO36Vrx5qRZ2SckUXIaEAsQrChZtxjOEQF',
                 'j9AyfiMkbSGWUqHgsqBVG0lY0dytSZ1pzmM6Um5bBe8v7fQLTZNw2CK4CtkJFYhr',
                 'wS8cSZKUof6JXHo2eN9U5diMXb2ggC0aYx7bOem7lauImvQDdyzVyxpVRPqT3nBw']



API_KEY = 's6l0K1wSbI2rSY0ntFlPEsRqbXdB7TXYvyCLxZi4jhMEkgrV6zNHezm9ULGJcn3O'

class Options:
    eng_list = []
    eng2rus = {}

    def __init__(self, eng_list_, eng2rus_):
        self.eng_list = eng_list_
        self.eng2rus = eng2rus_

    def translate2rus(self, item):
        return self.eng2rus.get(item, "Другое")


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

haircut_translation = {
    "BuzzCut": "Ноль",
    "UnderCut": "Андеркат",
    "Pompadour": "Помпадур",
    "SlickBack": "Зачес назад",
    "CurlyShag": "Кудри",
    "WavyShag": "Волны",
    "FauxHawk": "Ирокез",
    "Spiky": "Шипы",
    "CombOver": "Зачес",
    "HighTightFade": "Фейд",
    "ManBun": "Пучок",
    "Afro": "Афро"
}

color_translation = {
    "blonde": "Блонд",
    "platinumBlonde": "Платиновый блонд",
    "brown": "Коричневый",
    "lightBrown": "Светло-коричневый",
    "blue": "Синий",
    "lightBlue": "Светло-синий",
    "purple": "Фиолетовый",
    "lightPurple": "Светло-фиолетовый",
    "pink": "Розовый",
    "black": "Черный"
}

haircut_options = Options(haircut_list, haircut_translation)
color_options = Options(color_list, color_translation)

class CurrentFunction(StatesGroup):
    wait_photo = State()
    choose_color = State()
    choose_haircut = State()
    generating_photo = State()


async def blur_image(image_url, user_id):
    # Загружаем изображение по URL
    response = requests.get(image_url)
    if response.status_code != 200:
        raise ValueError(f"Не удалось скачать изображение: {response.status_code}")

    image = Image.open(BytesIO(response.content))

    # Применяем размытость
    blurred_image = image.filter(ImageFilter.GaussianBlur(20))  # Измените радиус размытия по необходимости

    # Сохраняем результат в BytesIO
    temp_filename = f'blurred_image_{user_id}.png'
    blurred_image.save(temp_filename, format='PNG')
    return temp_filename


async def change_hairstyle(image_url, hair_style='Pompadour', color='black'):
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
    try:
        headers = {
            'ailabapi-api-key': APIKeyManager.get_current_key()
        }
    except Exception as E:
            print(f"Ошибка {response.status_code}: {response.text}")
            return "https://avatars.mds.yandex.net/i?id=2ced998169ff1da0d4087152330c122d_l-5666582-images-thumbs&n=13"

    # Отправка POST-запроса для начала обработки
    response = requests.request("POST", url, headers=headers, data=payload, files=files)
    while response.status_code != 200:
        print(response.text)
        try:
            APIKeyManager.switch_to_next_key()
            headers = {
                'ailabapi-api-key': APIKeyManager.get_current_key()
            }
            image.seek(0)
            files = [
                ('image', ('file', image, 'application/octet-stream'))
            ]
            print("Переключаем ключ на ", headers, files, payload)
            response = requests.request("POST", url, headers=headers, data=payload, files=files)
        except Exception as E:
            print(f"Ошибка {response.status_code}: {response.text}")
            return "https://avatars.mds.yandex.net/i?id=2ced998169ff1da0d4087152330c122d_l-5666582-images-thumbs&n=13"

    task_id = response.json().get("task_id")
    print("Получен task_id")
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
                    time.sleep(5)
            else:
                print(f"Ошибка при проверке статуса: {status_response.status_code}")
                break
    else:
        print("Не удалось получить task_id")




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
    await message.reply("Выбери прическу", reply_markup=create_inline_keyboard(haircut_options, "haircut"))
    await state.set_state(CurrentFunction.choose_color)

# @dp.callback_query()
# async def test_callback(callback):
#     print(callback.data)

@dp.callback_query(F.data.startswith("haircut"))
async def set_haircut(callback, state):
    data = callback.data
    if "_page_" in data:
        current_page = int(data.split('_page_')[-1])
        await callback.message.edit_reply_markup(
            reply_markup=create_inline_keyboard(haircut_options, "haircut", current_page=current_page, items_per_page=6)
        )
    else:
        await state.update_data(haircut=data.split('_')[1])
        print(callback.message.text)
        await choosing_color(callback.message, state)


@dp.callback_query(F.data.startswith("color"))
async def set_color(callback, state):
    data = callback.data
    if "_page_" in data:
        current_page = int(data.split('_page_')[-1])
        await callback.message.edit_reply_markup(
            reply_markup=create_inline_keyboard(color_options, "color", current_page=current_page, items_per_page=6)
        )
    else:
        await state.update_data(color=data.split('_')[1])
        await state.set_state(CurrentFunction.generating_photo)
        await generate_photo(callback.message, state)


async def choosing_color(message, state):
    await message.edit_text("Выбери цвет", reply_markup=create_inline_keyboard(color_options, "color"))


async def generate_photo(message, state):
    user_dict = await state.get_data()
    print(user_dict)
    if user_dict.get("credits", 0) == 0 and user_dict.get("free_credits", None) and user_dict["free_credits"].get(datetime.now().date(), 1) < 1:
        await message.answer_photo(user_dict["blur_photo"], caption="На сегодня лимит генераций исчерпан")
    else:
        file_url = user_dict["file_url"]
        print("before query")
        sent_message = await message.edit_text("Идет генерация")
        task = asyncio.create_task(change_hairstyle(file_url, user_dict["haircut"], user_dict["color"]))
        while not task.done():
            await sent_message.edit_text("Идет генерация.")
            time.sleep(1)
            await sent_message.edit_text("Идет генерация..")
            time.sleep(1)
            await sent_message.edit_text("Идет генерация...")
            time.sleep(1)
        response = await task
        print("after query")
        print(file_url)
        print(response)
        if response.startswith("Error"):
            await message.reply(response)
        else:
            await sent_message.delete()
            if user_dict.get("credits", 0) == 0 and user_dict.get("free_credits", None) and user_dict["free_credits"].get(datetime.now().date(), 1) == 1:
                blur_photo = await blur_image(response, message.from_user.id)
                await state.update_data(blur_image=blur_photo)
                input_file = FSInputFile(blur_photo)
                await message.answer_photo(photo=input_file)
            else:
                await message.answer_photo(photo=response)
        await state.set_state(CurrentFunction.wait_photo)
        print("AFTER CHANGING state")
        print(await state.get_data())
        print(await state.get_state())
        print(user_dict)
        if user_dict.get("free_credits", None):
            if user_dict["free_credits"][datetime.now().date()] > 0:
                user_dict["free_credits"][datetime.now().date()] = user_dict["free_credits"].get(datetime.now().date(), 2) - 1
            else:
                user_dict["credits"] -= 1
        else:
            user_dict["free_credits"] = dict()
            user_dict["free_credits"][datetime.now().date()] = 2 - 1

        await state.update_data(free_credits=user_dict["free_credits"])
        if user_dict.get("credits", None):
            await state.update_data(credits=user_dict["credits"])
        await send_purchase_offer(message.reply_to_message, state)


async def send_purchase_offer(message, state):
    user_data = await state.get_data()
    credits = user_data.get("credits", 0)
    free_credits = user_data["free_credits"].get(datetime.now().date(), 1)
    print("Ваш баланс генераций на сегодня: " + str(free_credits))
    await message.answer("Ваш баланс генераций на сегодня: " + str(free_credits))
                        # reply_markup=CustomKeyboard("purchase"))

@dp.message()
async def default_reply(message: types.Message, state) -> None:
    await message.reply('Пришли мне фото')
    await state.set_state(CurrentFunction.wait_photo)


async def main():
    await dp.start_polling(bot)


if __name__ == '__main__':
    print("Before main call")
    asyncio.run(main())