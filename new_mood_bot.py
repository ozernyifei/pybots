import pyodbc
import telebot
import datetime
from telebot import types


server_name = 'localhost'  # Имя вашего сервера
database_name = 'MoodBotDB'  # Название вашей базы данных
username = 'botbotname'  # Ваше имя пользователя для доступа к базе данных
password = 'password'  # Ваш пароль для доступа к базе данных

# Строка подключения
connection_string = f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server_name};DATABASE={database_name};UID={username};PWD={password}'

# Создаем соединение
cnxn = pyodbc.connect(connection_string)

cursor = cnxn.cursor()

# Создание бота
bot = telebot.TeleBot('6290464531:AAHyfuLMg5eMZMe348O8TxkVXQ7vhEdE1vA')

# Обработка команды /start
@bot.message_handler(commands=['start'])
def start_handler(message):
    chat_id = message.chat.id
    user_id = message.from_user.id
    username = message.from_user.username

    # Проверяем, есть ли пользователь в базе данных
    cursor.execute("SELECT id FROM users WHERE id=?", user_id)
    row = cursor.fetchone()

    if not row:
        # Добавляем пользователя в базу данных
        cursor.execute("INSERT INTO users (id, username) VALUES (?, ?)", user_id, username)
        cnxn.commit()

        bot.reply_to(message, "Привет! Я буду записывать твои настроения. Используй кнопки, чтобы отправить свое текущее настроение.", reply_markup=mood_keyboard)

    else:
        bot.reply_to(message, "С возвращением! Используй кнопки, чтобы отправить свое текущее настроение.", reply_markup=start_keyboard)
# Определяем стартовую клавиатуру
start_keyboard = types.ReplyKeyboardMarkup(resize_keyboard= True)
share_mood_button = types.KeyboardButton(text="Share my mood")
send_weekly_report_button = types.KeyboardButton(text="Weekly report")
start_keyboard.add(share_mood_button, send_weekly_report_button)

@bot.message_handler(func=lambda message: message.text == 'Share my mood')
def handle_share_button(message):
    bot.reply_to(message, "Отправь своё текущее настроение из трех возможных вариантов: ", reply_markup= mood_keyboard)
    
@bot.message_handler(func=lambda message: message.text == 'Weekly report')
def handle_weekly_report(message):
    bot.reply_to(message, "Пока что я не могу отправить еженедельный отчёт! Ходят слухи, что в этом виноват ленивый разработчик... На данный момент, можешь начать отправлять мне своё настроение!", reply_markup= start_keyboard)

# Определяем клавиатуру с настроениеями
mood_keyboard = types.ReplyKeyboardMarkup(resize_keyboard= True)
good_button = types.KeyboardButton(text="Good")
okay_button = types.KeyboardButton(text="Okay")
bad_button = types.KeyboardButton(text="Bad")
mood_keyboard.add(good_button, okay_button, bad_button)

# Отправляем сообщение с кнопками пользователю
# Отвечаем на настроение юзера
@bot.message_handler(func=lambda message: message.text in ['Good', 'Okay', 'Bad'])
def handle_query(message):
    user_id = message.chat.id


    # Получаем время последнего добавления настроения пользователя
    last_mood_time = get_last_mood_time(user_id)

    # Если пользователь пытается добавить настроение раньше, чем через 24 часа, выдаем сообщение
    if last_mood_time and datetime.datetime.now() - last_mood_time < datetime.timedelta(days=1):
        bot.send_message(user_id, "Вы уже добавляли настроение сегодня. Попробуйте еще раз завтра!",reply_markup=start_keyboard)
        return

    # Добавляем настроение пользователя в базу данных
    add_mood_to_db(user_id, message.text)

    # Отправляем сообщение об успешном добавлении настроения
    bot.send_message(user_id, "Ваше настроение успешно добавлено!", reply_markup=start_keyboard)

# Define message handler
@bot.message_handler(commands=['mood'])
def send_mood(message):
    user_id = message.chat.id
    last_mood_time = get_last_mood_time(user_id)
    if not last_mood_time:
        bot.send_message(user_id, "You haven't submitted your mood yet.")
    else:
        mood_data = get_mood_data(user_id)
        if not mood_data:
            bot.send_message(user_id, "You haven't submitted your mood yet.")
        else:
            mood_list = [f"{data[0]}: {data[1]}" for data in mood_data]
            mood_history = '\n'.join(mood_list)
            bot.send_message(user_id, f"Your mood history for the past 7 days:\n{mood_history}")

# Add mood data to SQL database
def add_mood_to_db(user_id, mood):
    now = datetime.datetime.now()
    cursor.execute("INSERT INTO mood (user_id, mood, time) VALUES (?, ?, ?)", user_id, mood, now)
    cnxn.commit()

# Get the datetime of the last mood submission
def get_last_mood_time(user_id):
    cursor.execute("SELECT TOP 1 time FROM mood WHERE user_id = ? ORDER BY time DESC", user_id)
    row = cursor.fetchone()
    if row:
        return row[0]

# Get mood data for the past 7 days
def get_mood_data(user_id):
    conn = pyodbc.connect('Driver={SQL Server};'
                          'Server=your_server_name;'
                          'Database=your_database_name;'
                          'Trusted_Connection=yes;')
    cursor = conn.cursor()

    # Получаем данные о настроении пользователя за последние 7 дней
    end_date = datetime.datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
    start_date = end_date - datetime.timedelta(days=7)
    cursor.execute(f"SELECT CAST(time AS date), mood FROM mood WHERE user_id = ? AND time >= ? AND time <= ?", (user_id, start_date, end_date))
    rows = cursor.fetchall()

    mood_data = []
    for row in rows:
        mood_data.append({'date': row[0], 'mood': row[1]})


    return mood_data


# Запуск бота
bot.polling(none_stop= True)
