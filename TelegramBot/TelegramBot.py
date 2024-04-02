import select
import telebot
import gspread
from telebot import types

bot = telebot.TeleBot('7162103985:AAEimCQMejkVTqVvcyLul-nZTHVn8wWfOyA')

credentials = gspread.service_account(filename='credentials.json') 
sheet = credentials.open_by_key('1BCzJ14uwHL9cCjReBrcIggh1rYhsZIYlm8R8CUe6o5Q')
worksheet = sheet.sheet1

# Массив для хранения данных анкеты
form_data = []

@bot.message_handler(commands=['start', 'back']) #главнок меню
def start(message):
    # Приветственное сообщение и создание кнопки для заполнения анкеты
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    btn1 = types.KeyboardButton('Заполнить анкету')
    btn2 = types.KeyboardButton('Помощь')
    markup.add(btn1).add(btn2)
    bot.send_message(message.chat.id, 'Привет! Я бот для заполнения анкеты на межкампусную мобильность.', reply_markup=markup)
    bot.register_next_step_handler(message, next_command)
    
def next_command(message): #переход на следующую команду
    if message.text == 'Помощь':
        help_inf(message)
    elif message.text == 'Заполнить анкету':
        select_course(message)
    else:
        bot.send_message(message.chat.id, 'Пожалуйста, следуйте инструкциям')
        start(message)


@bot.message_handler(commands=['form']) #заполнение анкеты
def select_course(message):
    markup_course = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    btn1= types.KeyboardButton('1')
    btn2= types.KeyboardButton('2')
    btn3= types.KeyboardButton('3')
    btn4= types.KeyboardButton('4')
    markup_course.row(btn1,btn2)
    markup_course.row(btn3,btn4)
    bot.send_message(message.chat.id, 'Выберите ваш курс:', reply_markup=markup_course)
    bot.register_next_step_handler(message, select_direction)
    
    
def select_direction(message):
    # Сохраняем выбранный пользователем курс
    form_data.append(message.text)
    
    # Создание кнопок для выбора направления
    markup_direction = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    if message.text == '1' or message.text == '2': #направления 1 и 2 курсов
        p0 = types.KeyboardButton('Программная инженерия')
        p1 = types.KeyboardButton('Бизнес информатика')
        p2 = types.KeyboardButton('Междунарожный бакалавриат')
        p3 = types.KeyboardButton('История')
        p4 = types.KeyboardButton('Юриспруденция')
        p5 = types.KeyboardButton('Иностранные языки')
        markup_direction.row(p0,p1)
        markup_direction.row(p2)
        markup_direction.row(p3,p4)
        markup_direction.row(p5)
        bot.send_message(message.chat.id, 'Выберите ваше направление (Важно! Направление "Разработка инофрмационных систем для бизнеса" разделено на направления "Программная инженерия" и "Бизнес информатика" вследствие разных кодов.):', reply_markup=markup_direction)
    if message.text == '3' or message.text == '4': #направления 3 и 4 курсов
        p1 = types.InlineKeyboardButton('Программная инженерия')
        p2 = types.InlineKeyboardButton('Бизнес информатика')
        p3 = types.InlineKeyboardButton('История')
        p4 = types.InlineKeyboardButton('Юриспруденция')
        p5 = types.InlineKeyboardButton('Иностранные языки')
        p6 = types.InlineKeyboardButton('Экономика')
        p7 = types.InlineKeyboardButton('Управление бизнесом')
        markup_direction.row(p1,p2)
        markup_direction.row(p6,p7)
        markup_direction.row(p3,p4)
        markup_direction.row(p5)
        bot.send_message(message.chat.id, 'Выберите ваше направление:', reply_markup=markup_direction)
    bot.register_next_step_handler(message, enter_lastname)

def enter_lastname(message):
    # Сохраняем выбранное пользователем направление
    form_data.append(message.text)
    
    # Запрос фамилии
    bot.send_message(message.chat.id, 'Введите вашу фамилию:', reply_markup=types.ReplyKeyboardRemove())
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
    #Проверяем, корректно ли введён рейтинг пользователем, затем сохраняем его
    try:
        if 0 < float(message.text) < 10:
            form_data.append(message.text)
        else:
            bot.send_message(message.chat.id, 'Рейтинг введён некорректно! Повторите ввод. Рейтинг должен быть в диапазоне от 0 до 10, например 7.62')
            bot.register_next_step_handler(message, confirm_data)
    except:
        bot.send_message(message.chat.id, 'Рейтинг введён некорректно! Повторите ввод. Рейтинг должен быть в диапазоне от 0 до 10, например 7.62')
        bot.register_next_step_handler(message, confirm_data)
        
    
    # Вывод анкеты для проверки
    confirmation_text = f"Ваша анкета:\n\n" \
                        f"Курс: {form_data[0]}\n" \
                        f"Направление: {form_data[1]}\n" \
                        f"Фамилия: {form_data[2]}\n" \
                        f"Имя: {form_data[3]}\n" \
                        f"Рейтинг: {form_data[4]}\n\n" \
                        f"Данные верны?"
    
    # Создание кнопок для подтверждения данных
    markup_confirmation = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    yes = types.KeyboardButton('Да')
    no = types.KeyboardButton('Нет')
    markup_confirmation.row(yes,no)
    bot.send_message(message.chat.id, confirmation_text, reply_markup=markup_confirmation)
    bot.register_next_step_handler(message, process_confirmation)

def process_confirmation(message):
    # Обработка выбора пользователя
    if message.text.lower() == 'да':
        # Данные верны
        bot.send_message(message.chat.id, 'Спасибо, ваша анкета успешно заполнена!', reply_markup=types.ReplyKeyboardRemove())
        worksheet.append_row([form_data[0], form_data[1], form_data[2], form_data[3], form_data[4]])
    elif message.text.lower() == 'нет':
        # Данные неверны
        bot.send_message(message.chat.id, 'Пожалуйста, введите данные заново.')
        form_data.clear()
        select_course(message)
        
@bot.message_handler(commands=['help']) #помощь
def help_inf(message):
    help_info = 'Я бот для заполнения анкеты на межкампусную мобильность. Через меня ты сможешь подать заявку для участия в межкампусной мобильности. Для этого просто начни заполнять анкету. Когда ты выберешь свой курс и направление, я сам предложу тебе вараинты, в какой город и на какое направление ты сможешь отправиться. Помни, ты должен честно заполнять все данные! Особенно рейтинг! Иначе на мобильность не возьмём. :)'
    feedback = 'Возникли проблемы? Свяжись с разработчиками! \nhttps://t.me/brokenbytheway \nhttps://t.me/Miron12315 \nhttps://t.me/dedbezpasportaideneg'
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    btn1 = types.KeyboardButton('Заполнить анкету')
    btn2 = types.KeyboardButton('Назад')
    markup.add(btn1).add(btn2)
    bot.send_message(message.chat.id, help_info, reply_markup=markup)
    bot.send_message(message.chat.id, feedback)
    bot.register_next_step_handler(message, next_command2)
    
def next_command2(message): #переход на следующую команду
    if message.text == 'Назад':
        start(message)
    elif message.text == 'Заполнить анкету':
        select_course(message)
    else:
        bot.send_message(message.chat.id, 'Пожалуйста, следуйте инструкциям')
        help_inf(message)
 
#@bot.message_handler(commands=['mobility']) #выбор мобильности
#def mobility(message):
    
bot.infinity_polling()
