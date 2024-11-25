from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher import filters
from aiogram.utils import executor
import os

API_TOKEN = ''
bot = Bot(token=API_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

# Список продуктов
products = [
    ("Парацетамол", "описание 1", 100, "images/1.png", "rb"),
    ("Pharmacy", "описание 2", 200, "images/2.png", "rb"),
    ("VitaBox", "описание 3", 300, "images/3.png", "rb"),
    ("Уронорм", "описание 4", 400, "images/4.png", "rb"),
]


# Главная клавиатура с кнопкой "Купить"
@dp.message_handler(commands=['start'])
async def start_command(message: types.Message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    buy_button = types.KeyboardButton('Купить')
    keyboard.add(buy_button)
    await message.answer("Добро пожаловать! Выберите действие.", reply_markup=keyboard)


@dp.message_handler(filters.Text(equals="Купить"))
async def get_buying_list(message: types.Message):
    for product in products:
        product_info = f"Название: {product[0]} | Описание: {product[1]} | Цена: {product[2]}"
        await message.answer(product_info)

        # Отправка изображения
        photo_path = product[3]  # путь к изображению
        if os.path.exists(photo_path):
            with open(photo_path, 'rb') as photo:
                await message.answer_photo(photo=photo)
        else:
            await message.answer("Изображение не найдено.")

    inline_keyboard = types.InlineKeyboardMarkup()
    for product in products:
        button = types.InlineKeyboardButton(text=product[0], callback_data="product_buying")
        inline_keyboard.add(button)

    await message.answer("Выберите продукт для покупки:", reply_markup=inline_keyboard)


@dp.callback_query_handler(lambda call: call.data == "product_buying")
async def send_confirm_message(call: types.CallbackQuery):
    await call.answer()  # Убираем спиннер
    await call.message.answer("Вы успешно приобрели продукт!")


# Запуск бота
if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)