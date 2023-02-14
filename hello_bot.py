
import telebot
import datetime
from telebot.types import ReplyKeyboardMarkup, KeyboardButton

bot = telebot.TeleBot('6168613359:AAGBE0EBuTHcA57OSK3Y3VOVQBzsdZ0Mh6s')

@bot.message_handler(commands=['start'])
def send_welcome(message):
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = KeyboardButton("Приветствие")
    item2 = KeyboardButton("День недели")
    item3 = KeyboardButton("Когда?")
    markup.add(item1, item2, item3)
    bot.reply_to(message, "Привет! Я телеграм-бот.", reply_markup=markup)

# Обработчик события нажатия на кнопку "Приветствие"
@bot.message_handler(func=lambda message: message.text == "Приветствие")
def handle_greeting(message):
    bot.send_message(message.chat.id, "Привет! Как дела?")
@bot.message_handler(func=lambda message: message.text == "Когда?")
def handle_additional(message):
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = KeyboardButton("Девопс")
    item2 = KeyboardButton("Альбом")
    item3 = KeyboardButton("Пить")
    markup.add(item1, item2, item3)
    bot.send_message(message.chat.id, "Что когда?", reply_markup=markup)

# Обработчик события нажатия на кнопку "Девопс"
@bot.message_handler(func=lambda message: message.text == "Девопс")
def handle_devops(message):
    bot.send_message(message.chat.id, "Скоро!")

# Обработчик события нажатия на кнопку "Альбом"
@bot.message_handler(func=lambda message: message.text == "Альбом")
def handle_album(message):
    bot.send_message(message.chat.id, "Иди нахуй")

# Обработчик события нажатия на кнопку "Пить"
@bot.message_handler(func=lambda message: message.text == "Пить")
def handle_drink(message):
    bot.send_message(message.chat.id, "Позови, пойдём!")

# Обработчик события нажатия на кнопку "День недели"
@bot.message_handler(func=lambda message: message.text == "День недели")
def handle_day_of_week(message):
    # здесь можно добавить ваш код для получения дня недели
    now = datetime.datetime.now()  # Получаем текущее время
    day = now.strftime("%A")  # Получаем текущий день недели
    date = now.strftime("%d.%m.%Y")  # Получаем текущую дату
    time = now.strftime("%H:%M:%S")  # Получаем текущее время
    reply = f"Сегодня {day}, {date}, {time} по Москве."
    bot.send_message(message.chat.id, reply)

bot.polling(none_stop=True)