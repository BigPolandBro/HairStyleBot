import asyncio
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.types import ContentType, FSInputFile
from aiogram.fsm.state import StatesGroup, State
from keyboard import KeyboardFactory
import os
import requests
import time
from io import BytesIO
from datetime import datetime
from APIKeyManager import APIKeyManager
from PIL import Image, ImageFilter

API_KEY = 's6l0K1wSbI2rSY0ntFlPEsRqbXdB7TXYvyCLxZi4jhMEkgrV6zNHezm9ULGJcn3O'

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
    blurred_image = image.filter(ImageFilter.GaussianBlur(40))  # Измените радиус размытия по необходимости

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


async def choosing_haircut(message, state):
    await message.reply("Выбери прическу", reply_markup=KeyboardFactory(callback_prefix="haircut").create_keyboard())
    await state.set_state(CurrentFunction.choose_color)

# @dp.callback_query()
# async def test_callback(callback):
#     print(callback.data)

@dp.callback_query(F.data.startswith("haircut"))
async def set_haircut(callback, state):
    data = callback.data
    print("ok")
    if "_page_" in data:
        current_page = int(data.split('_page_')[-1])
        await callback.message.edit_reply_markup(
            reply_markup=KeyboardFactory(callback_prefix="haircut", current_page=current_page).create_keyboard()
        )
    elif "_back" in data:
        current_page = 1  # TODO
        await callback.message.reply(
            "Выбери прическу",
            reply_markup=KeyboardFactory(callback_prefix="haircut", current_page=current_page).create_keyboard()
        )
        await callback.message.delete()
    elif "_view_" in data:
        haircut_name = data.split('_view_')[-1]
        photo_path = os.path.join("haircut_photos", f"{haircut_name}.jpg")
        if os.path.exists(photo_path):
            #with open(photo_path, 'rb') as photo:
            await callback.message.delete()  # Удаляем предыдущие сообщения
            await state.update_data(haircut=haircut_name)
            await callback.message.answer_photo(
                photo=FSInputFile(photo_path),
                caption=f"Прическа: {haircut_name}",
                reply_markup=KeyboardFactory(callback_prefix="haircut_view").create_keyboard()
            )
    elif "_choose" in data:
        # haircut_name = await state.get_data("haircut")
        # await state.update_data(haircut=haircut_name)
        print(callback.message.text)
        await choosing_color(callback.message, state)

    #TO DO bigpolandbro -
    # elif "back" -> show menu
    # elif "view" -> add await callback.message.edit_reply_markup( PHOTO
    #         #     reply_markup=KeyboardFactory(callback_prefix="haircut_show").create_keyboard()
    #         # )
    # + add _view_ to buttons in paged_keyboard
    # elif "choose" -> same as current else
    # think how to organize options[callback_prefix] ? currently options["haircut"] but I need options["haircut_view"]


@dp.callback_query(F.data.startswith("color"))
async def set_color(callback, state):
    data = callback.data
    print("GOOD")
    if "_page_" in data:
        current_page = int(data.split('_page_')[-1])
        await callback.message.edit_reply_markup(
            reply_markup=KeyboardFactory(callback_prefix="color", current_page=current_page).create_keyboard()
        )
    else:
        await state.update_data(color=data.split('_')[1])
        await state.set_state(CurrentFunction.generating_photo)
        await generate_photo(callback.message, state)


async def choosing_color(message, state):
    await message.reply("Выбери цвет", reply_markup=KeyboardFactory(callback_prefix="color").create_keyboard())
    await message.delete()


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
    await message.answer("Ваш баланс генераций на сегодня: " + str(free_credits), reply_markup=KeyboardFactory(callback_prefix="purchase").create_keyboard())

@dp.callback_query(F.data.startswith("purchase"))
async def make_purchase(callback, state):
    await callback.message.edit_text("Автоматическая оплата в разработке \n"
                            "***Для того, чтобы купить 10 генераций, "
                            "отправьте 200 рублей по номеру телефона +79174667475*** \n"
                            "После этого пришлите скриншот/чек сюда: @andreevoleg22", parse_mode="markdown")

@dp.message()
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

async def main():
    await dp.start_polling(bot)


if __name__ == '__main__':
    print("Before main call")
    asyncio.run(main())