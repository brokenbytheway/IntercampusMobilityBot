from atexit import register
import re
import site
import telebot
import gspread
from telebot import types

bot = telebot.TeleBot('7162103985:AAEimCQMejkVTqVvcyLul-nZTHVn8wWfOyA')

credentials = gspread.service_account(filename='credentials.json') 
sheet = credentials.open_by_key('1BCzJ14uwHL9cCjReBrcIggh1rYhsZIYlm8R8CUe6o5Q')
worksheet = sheet.sheet1

# Массив для хранения данных анкеты
form_data = []

@bot.message_handler(commands=['start', 'back']) #главное меню
def start(message):
    # Приветственное сообщение и создание кнопки для заполнения анкеты
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    btn1 = types.KeyboardButton('Заполнить анкету')
    btn2 = types.KeyboardButton('Помощь')
    markup.add(btn1).add(btn2)
    if message.text == '/start':
        bot.send_message(message.chat.id, 'Привет! Я бот для заполнения анкеты на межкампусную мобильность.', reply_markup=markup)
        bot.send_message(message.chat.id, 'Перед заполнением анкеты рекомендуется прочитать полезную информацию по кнопке "Помощь"')
    elif message.text == 'Назад':
        bot.send_message(message.chat.id, 'Готовы заполнить анкету? Тогда вперёд!', reply_markup=markup)
    elif message.text.lower() == 'да':
        bot.send_message(message.chat.id, 'Спасибо, ваша анкета успешно заполнена!', reply_markup=markup)
    else:
        bot.send_message(message.chat.id, 'Пожалуйста, следуйте инструкциям', reply_markup=markup)
        
    bot.register_next_step_handler(message, next_command)
    
def next_command(message): #переход на следующую команду
    if message.text == 'Помощь':
        help_inf(message)
    elif message.text == 'Заполнить анкету':
        select_course(message)
    else:
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
        p2 = types.KeyboardButton('Экономика')
        p6 = types.KeyboardButton('Менеджмент')
        p3 = types.KeyboardButton('История')
        p4 = types.KeyboardButton('Юриспруденция')
        p7 = types.KeyboardButton('Дизайн')
        p5 = types.KeyboardButton('Лингвистика')
        
        
        markup_direction.row(p0,p1)
        markup_direction.row(p2,p6)
        markup_direction.row(p3,p4)
        markup_direction.row(p5,p7)
        bot.send_message(message.chat.id, 'Выберите ваше направление:', reply_markup=markup_direction)
        bot.send_message(message.chat.id, 'Важно! Направление "Разработка инофрмационных систем для бизнеса" разделено на направления "Программная инженерия" и "Бизнес информатика" вследствие разных кодов.')
        bot.send_message(message.chat.id, 'Важно! Направление "Международный бакалавриат по бизнесу и экономике" разделено на направления "Экономика" и "Менеджмент" вследствие разных кодов.')
    if message.text == '3' or message.text == '4': #направления 3 и 4 курсов
        p1 = types.InlineKeyboardButton('Программная инженерия')
        p2 = types.InlineKeyboardButton('Бизнес информатика')
        p3 = types.InlineKeyboardButton('История')
        p4 = types.InlineKeyboardButton('Юриспруденция')
        p5 = types.InlineKeyboardButton('Лингвистика')
        p6 = types.InlineKeyboardButton('Экономика')
        p8 = types.InlineKeyboardButton('Дизайн')
        markup_direction.row(p1,p2)
        markup_direction.row(p6,p8)
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
        worksheet.append_row([form_data[0], form_data[1], form_data[2], form_data[3], form_data[4]])
        mobility(message)
    elif message.text.lower() == 'нет':
        # Данные неверны
        bot.send_message(message.chat.id, 'Пожалуйста, введите данные заново.')
        form_data.clear()
        select_course(message)
        
@bot.message_handler(commands=['help']) #помощь
def help_inf(message):
    help_info = 'Я бот для заполнения анкеты на межкампусную мобильность. Через меня ты сможешь подать заявку для участия в межкампусной мобильности. Для этого просто начни заполнять анкету. Когда ты выберешь свой курс и направление, я сам предложу тебе варианты, в какой город и на какое направление ты сможешь отправиться. Помни, ты должен честно заполнять все данные! Особенно рейтинг! Иначе на мобильность не возьмём. :)'
    feedback = 'Возникли проблемы? Свяжись с разработчиками! \nhttps://t.me/brokenbytheway \nhttps://t.me/Miron12315 \nhttps://t.me/dedbezpasportaideneg'
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    btn1 = types.KeyboardButton('Назад')
    markup.add(btn1)
    if message.text == 'Помощь':
        bot.send_message(message.chat.id, help_info, reply_markup=markup)
        bot.send_message(message.chat.id, feedback)
    else:
        bot.send_message(message.chat.id, 'Пожалуйста, следуйте инструкциям', reply_markup=markup)
    bot.register_next_step_handler(message, next_command2)
    
def next_command2(message): #переход на следующую команду
    if message.text == 'Назад':
        start(message)
    else:
        help_inf(message)
 
@bot.message_handler(commands=['mobility']) #выбор мобильности (если придумаете, как сжать этот громадный кусок кода, то сообщите, буду безмерно благодарен)
def mobility(message):
    def site(my_url): #функция по созданию кнопки, отсылающей на сайт, чтоб хоть как-то код сократить
        return types.InlineKeyboardButton('Ознакомиться с программой', url = my_url)
    bot.send_message(message.chat.id, "Исходя из вашего направления, мы можем предложить вам следующие варианты межкампусной мобильности:", reply_markup=types.ReplyKeyboardRemove())
    markupMoscow = types.InlineKeyboardMarkup() #области кнопок для каждого города
    markupMoscow2 = types.InlineKeyboardMarkup() #их может 2 и более, так как программ с одним кодом в одном городе может быть несколько
    markupNovgorod = types.InlineKeyboardMarkup()
    markupNovgorod2 = types.InlineKeyboardMarkup()
    markupPetersburg = types.InlineKeyboardMarkup()
    if form_data[1] == 'Программная инженерия':
        siteMoscow = site('https://www.hse.ru/ba/se/') #эта кнопка ведёт на сайт
        siteNovgorod = site('https://nnov.hse.ru/bipm/se/')
        siteNovgorod2 = site('https://nnov.hse.ru/ba/cst/')
        registerMoscow = types.InlineKeyboardButton('Записаться', callback_data= 'pi_msk') #эта кнопка по идее должна обеспечивать запись
        registerNovgorod = types.InlineKeyboardButton('Записаться', callback_data='pi_nn1')
        registerNovgorod2 = types.InlineKeyboardButton('Записаться', callback_data='pi_nn2')
        markupMoscow.row(siteMoscow,registerMoscow)
        markupNovgorod.row(siteNovgorod,registerNovgorod)
        markupNovgorod2.row(siteNovgorod2,registerNovgorod2)
        bot.send_message(message.chat.id, 'Програмная инженерия \nМосква', reply_markup=markupMoscow)
        bot.send_message(message.chat.id, 'Программная инженерия (очно-заочное обучение) \nНижний Новгород', reply_markup=markupNovgorod)
        bot.send_message(message.chat.id, 'Компьютерные науки и технологии \nНижний Новгород', reply_markup=markupNovgorod2)
    elif form_data[1] == 'Бизнес информатика': #пока без кнопок "записаться", всё равно не знаю, как её активировать
        siteMoscow = site('https://www.hse.ru/ba/bi/')
        siteMoscow2 = site('https://www.hse.ru/ba/digital/')
        siteNovgorod = site('https://nnov.hse.ru/ba/cst/')
        sitePetersburg = site('https://spb.hse.ru/ba/bi/')
        markupMoscow.row(siteMoscow)
        markupMoscow2.row(siteMoscow2)
        markupNovgorod.row(siteNovgorod)
        markupPetersburg.row(sitePetersburg)
        bot.send_message(message.chat.id, 'Бизнес информатика \nМосква', reply_markup=markupMoscow)
        bot.send_message(message.chat.id, 'Управление цифровым продуктом \nМосква', reply_markup=markupMoscow2)
        bot.send_message(message.chat.id, 'Компьютерные науки и технологии \nНижний Новгород', reply_markup=markupNovgorod)
        bot.send_message(message.chat.id, 'Бизнес-информатика \nСанкт-Петербург', reply_markup=markupPetersburg)
    elif form_data[1] == 'Экономика':
        pass
    elif form_data[1] == 'Менеджмент':
        pass
    elif form_data[1] == 'История':
        siteMoscow = site('https://www.hse.ru/ba/hist/') #эта кнопка ведёт на сайт
        siteMoscow2 = site('https://www.hse.ru/ba/antiq/')
        sitePetersburg = site('https://spb.hse.ru/ba/hist/')
        registerMoscow = types.InlineKeyboardButton('Записаться', callback_data= 'pi_msk') #эта кнопка по идее должна обеспечивать запись
        registerMoscow2 = types.InlineKeyboardButton('Записаться', callback_data='pi_nn1')
        registerPetersburg = types.InlineKeyboardButton('Записаться', callback_data='pi_nn2')
        markupMoscow.row(siteMoscow,registerMoscow)
        markupMoscow2.row(siteMoscow2,registerMoscow2)
        markupPetersburg.row(sitePetersburg,registerPetersburg)
        bot.send_message(message.chat.id, 'История \nМосква', reply_markup=markupMoscow)
        bot.send_message(message.chat.id, 'Античность \nМосква', reply_markup=markupMoscow2)
        bot.send_message(message.chat.id, 'История \nСанкт-Петербург', reply_markup=markupPetersburg)
    elif form_data[1] == 'Юриспруденция':
        pass
    elif form_data[1] == 'Лингвистика':
        siteMoscow = site('https://www.hse.ru/ba/lang/')
        siteNovgorod = site('https://nnov.hse.ru/ba/ibc/')
        markupMoscow.add(siteMoscow)
        markupNovgorod.add(siteNovgorod)
        bot.send_message(message.chat.id, 'Иностранные языки и межкультурная коммуникация \nМосква', reply_markup=markupMoscow)
        bot.send_message(message.chat.id, 'Иностранные языки и межкультурная бизнес-коммуникация \nНижний Новгород', reply_markup=markupNovgorod)
        
    elif form_data[1] == 'Дизайн':
        pass

@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call): #осуществление записи на мобильность, здесь нужно реализовать добавление данных о мобильности в таблицу
    for i in range(-4,0):
        bot.delete_message(call.chatid,call.messageid-1)
    try:
        if call.message:
            if call.data == "pi_msk":
                bot.send_message(call.message.chat.id, 'Вы успешно записались на обрзовательную программу "Програмная инженерия" в городе Москва!')
            if call.data == "pi_nn":
                bot.send_message(call.message.chat.id, 'Вы успешно записались на обрзовательную программу "Программная инженерия (очно-заочное обучение)" в городе Нижний Новгород!')
    except Exception as e:
        print(repr(e))
    bot.send_message(call.message.chat.id, 'Или нет...')
bot.infinity_polling()
