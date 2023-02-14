import telebot
import datetime

# создаем объект бота
bot = telebot.TeleBot('6168613359:AAGBE0EBuTHcA57OSK3Y3VOVQBzsdZ0Mh6s')

# первое меню с тремя кнопками
main_menu_markup = telebot.types.ReplyKeyboardMarkup(row_width=1)
hello_button = telebot.types.KeyboardButton('Приветствие')
weekday_button = telebot.types.KeyboardButton('День недели')
when_button = telebot.types.KeyboardButton('Когда?')
main_menu_markup.add(hello_button, weekday_button, when_button)

# второе меню с тремя кнопками и кнопкой "назад"
second_menu_markup = telebot.types.ReplyKeyboardMarkup(row_width=1)
devops_button = telebot.types.KeyboardButton('Девопс')
album_button = telebot.types.KeyboardButton('Альбом')
drink_button = telebot.types.KeyboardButton('Пить')
back_button = telebot.types.KeyboardButton('Назад')
second_menu_markup.add(devops_button, album_button, drink_button, back_button)

# обработчик команды /start
@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, 'Привет! Это тестовый бот. Нажми на одну из кнопок, чтобы продолжить.', reply_markup=main_menu_markup)

# обработчик кнопки "приветствие"
@bot.message_handler(func=lambda message: message.text == 'Приветствие')
def hello_message(message):
    bot.send_message(message.chat.id, 'Привет, я тестовый бот!', reply_markup=main_menu_markup)

# обработчик кнопки "день недели"
@bot.message_handler(func=lambda message: message.text == 'День недели')
def weekday_message(message):
    weekday = datetime.datetime.today().strftime('%A')
    bot.send_message(message.chat.id, f'Сегодня {weekday}.', reply_markup=main_menu_markup)

# обработчик кнопки "когда?"
@bot.message_handler(func=lambda message: message.text == 'Когда?')
def when_message(message):
    bot.send_message(message.chat.id, 'Что когда?', reply_markup=second_menu_markup)

# обработчик кнопки "девопс"
@bot.message_handler(func=lambda message: message.text == 'Девопс')
def devops_message(message):
    bot.send_message(message.chat.id, 'Скоро...', reply_markup=second_menu_markup)

# обработчик кнопки "альбом"
@bot.message_handler(func=lambda message: message.text == 'Альбом')
def album_message(message):
    bot.send_message(message.chat.id, 'Скоро...', reply_markup=second_menu_markup)

# обработчик кнопки "пить"
@bot.message_handler(func=lambda message: message.text == 'Пить')
def drink_message(message):
    bot.send_message(message.chat.id, 'Скоро...', reply_markup=second_menu_markup)

# обработчик кнопки "назад"
@bot.message_handler(func=lambda message: message.text == 'Назад')
def back_message(message):
    bot.send_message(message.chat.id, 'Выбери, что ты хочешь сделать.', reply_markup=main_menu_markup)