from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

#Разметка клавиатуры ответа #изменение размера клавиатуры #Кнопка клавиатуры
main_meny = ReplyKeyboardMarkup(resize_keyboard=True).add(KeyboardButton('/Фильмы'), KeyboardButton('/Топ-100'))