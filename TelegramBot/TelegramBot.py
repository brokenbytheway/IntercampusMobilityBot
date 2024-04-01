import telebot
import gspread
from telebot import types

bot = telebot.TeleBot('7162103985:AAEimCQMejkVTqVvcyLul-nZTHVn8wWfOyA')

credentials = gspread.service_account(filename='credentials.json') 
sheet = credentials.open_by_key('1BCzJ14uwHL9cCjReBrcIggh1rYhsZIYlm8R8CUe6o5Q')
worksheet = sheet.sheet1

# Массив для хранения данных анкеты
form_data = []

@bot.message_handler(commands=['start'])
def start(message):
    # Приветственное сообщение и создание кнопки для заполнения анкеты
    markup = types.ReplyKeyboardMarkup()
    btn1 = types.KeyboardButton('Заполнить анкету')
    markup.add(btn1)
    bot.send_message(message.chat.id, 'Привет! Я бот для заполнения анкеты на межкампусную мобильность.', reply_markup=markup)
    bot.register_next_step_handler(message, select_course)

def select_course(message):
    if message.text == 'Заполнить анкету':
        # Создание кнопок для выбора курса с 2 по 4
        markup_course = types.ReplyKeyboardMarkup()
        for course in range(2, 5):
            button = types.KeyboardButton(course)
            markup_course.add(button)
    
        bot.send_message(message.chat.id, 'Выберите ваш курс:', reply_markup=markup_course)
        bot.register_next_step_handler(message, select_direction)
    
def select_direction(message):
    # Сохраняем выбранный пользователем курс
    form_data.append(message.text)
    
    # Создание кнопок для выбора направления
    markup_direction = types.ReplyKeyboardMarkup()
    directions = ['РИС', 'МБ', 'И', 'Ю', 'ИЯ']  # Пример направлений
    for direction in directions:
        button = types.KeyboardButton(direction)
        markup_direction.add(button)
    
    bot.send_message(message.chat.id, 'Выберите ваше направление:', reply_markup=markup_direction)
    bot.register_next_step_handler(message, enter_lastname)

def enter_lastname(message):
    # Сохраняем выбранное пользователем направление
    form_data.append(message.text)
    
    # Запрос фамилии
    bot.send_message(message.chat.id, 'Введите вашу фамилию:')
    bot.register_next_step_handler(message, enter_firstname)

def enter_firstname(message):
    # Сохраняем введенную пользователем фамилию
    form_data.append(message.text)
    
    # Запрос имени
    bot.send_message(message.chat.id, 'Введите ваше имя:')
    bot.register_next_step_handler(message, enter_rating)

def enter_rating(message):
    # Сохраняем введенное пользователем имя
    form_data.append(message.text)
    
    # Запрос рейтинга
    bot.send_message(message.chat.id, 'Введите ваш рейтинг (например, 7.62):')
    bot.register_next_step_handler(message, confirm_data)

def confirm_data(message):
    # Сохраняем введенный пользователем рейтинг
    form_data.append(message.text)
    
    # Вывод анкеты для проверки
    confirmation_text = f"Ваша анкета:\n\n" \
                        f"Курс: {form_data[0]}\n" \
                        f"Направление: {form_data[1]}\n" \
                        f"Фамилия: {form_data[2]}\n" \
                        f"Имя: {form_data[3]}\n" \
                        f"Рейтинг: {form_data[4]}\n\n" \
                        f"Данные верны?"
    
    # Создание кнопок для подтверждения данных
    markup_confirmation = types.ReplyKeyboardMarkup()
    buttons = ['Да', 'Нет']
    for button in buttons:
        markup_confirmation.add(button)
    
    bot.send_message(message.chat.id, confirmation_text, reply_markup=markup_confirmation)
    bot.register_next_step_handler(message, process_confirmation)

def process_confirmation(message):
    # Обработка выбора пользователя
    if message.text.lower() == 'да':
        # Данные верны
        bot.send_message(message.chat.id, 'Спасибо, ваша анкета успешно заполнена!')
        worksheet.append_row([form_data[0], form_data[1], form_data[2], form_data[3], form_data[4]])
    elif message.text.lower() == 'нет':
        # Данные неверны
        bot.send_message(message.chat.id, 'Пожалуйста, введите данные заново.')
        form_data.clear()
        start(message)
    
bot.infinity_polling()
