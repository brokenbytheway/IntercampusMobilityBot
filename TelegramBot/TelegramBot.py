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
        p1 = types.KeyboardButton('Бизнес-информатика')
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
        bot.send_message(message.chat.id, '<b><u>Важно!</u></b> Направление "Разработка инофрмационных систем для бизнеса" разделено на направления "Программная инженерия" и "Бизнес информатика" вследствие разных кодов.', parse_mode='html')
        bot.send_message(message.chat.id, '<b><u>Важно!</u></b> Направление "Международный бакалавриат по бизнесу и экономике" разделено на направления "Экономика" и "Менеджмент" вследствие разных кодов.', parse_mode='html')
    if message.text == '3' or message.text == '4': #направления 3 и 4 курсов
        p1 = types.InlineKeyboardButton('Программная инженерия')
        p2 = types.InlineKeyboardButton('Бизнес-информатика')
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
    
    def mobility_info(name, city, my_url, b, p, t, cbd): #функция для вывода информации об одном направлении
        markup = types.InlineKeyboardMarkup()
        site = types.InlineKeyboardButton('Ознакомиться с программой', url = my_url)
        register = types.InlineKeyboardButton('Записаться', callback_data = cbd)
        markup.row(site, register)
        text = f"*Программа: {name}\n*" \
               f"*Город: {city}\n*" \
               f"Бюджетных мест: {b}\n" \
               f"Платных мест: {p}\n" \
               f"Продолжительность обучения: {t}"
        bot.send_message(message.chat.id, text, reply_markup=markup, parse_mode='Markdown')
        
    #mobility_info(название программы, город, ссылка на сайт, кол-во бюджетных мест, кол-во платных мест, продолжительность обучения, колбэк дата)  

    bot.send_message(message.chat.id, "Исходя из вашего направления, мы можем предложить вам следующие варианты межкампусной мобильности:", reply_markup=types.ReplyKeyboardRemove())
    if form_data[1] == 'Программная инженерия':
        mobility_info('Дизайн и разработка информационных продуктов', 'Москва', 'https://www.hse.ru/ba/drip/', 0, 50, '4 года', 'drip_msk')
        mobility_info('Компьютерные науки и технологии', 'Нижний Новгород', 'https://nnov.hse.ru/ba/cst/', 50, 35, '4 года', 'cst_nn')
        mobility_info('Программная инженерия', 'Москва', 'https://www.hse.ru/ba/se/', 150, 80, '4 года', 'se_msk')
        mobility_info('Программная инженерия (очно-заочное обучение)', 'Нижний Новгород', 'https://nnov.hse.ru/bipm/se/', '???', '???', '4,5 года', 'se_nn')
        mobility_info('Технологии искусственного и дополненного интеллекта', 'Нижний Новгород', 'https://nnov.hse.ru/ba/ait/', 10, 40, '4 года', 'ait_nn')
        
    elif form_data[1] == 'Бизнес-информатика':
        mobility_info('Бизнес-информатика', 'Москва', 'https://www.hse.ru/ba/bi/', 130, 80, '4 года', 'bi_msk')
        mobility_info('Бизнес-информатика', 'Санкт-Петербург', 'https://spb.hse.ru/ba/bi/', 25, 25, '4 года', 'bi_spb')
        mobility_info('Компьютерные науки и технологии', 'Нижний Новгород', 'https://nnov.hse.ru/ba/cst/', 65, 30, '4 года', 'cst_nn')
        mobility_info('Управление цифровым продуктом', 'Москва', 'https://www.hse.ru/ba/digital/', 0, 80, '4 года', 'dig_msk')

    elif form_data[1] == 'Экономика':
        mobility_info('Аналитика в экономике', 'Санкт-Петербург', 'https://spb.hse.ru/ba/economicdata/', 60, 60, '4 года', 'ed_spb')
        mobility_info('Международная программа по экономике и финансам', 'Москва', 'https://www.hse.ru/ba/icef/', 0, 200, '4 года', 'icef_msk')
        mobility_info('Международный бакалавриат по бизнесу и экономике', 'Нижний Новгород', 'https://nnov.hse.ru/ba/interbac/', '???', '???', '4 года', 'ib_nn')
        mobility_info('Международный бакалавриат по бизнесу и экономике', 'Санкт-Петербург', 'https://spb.hse.ru/ba/interbac/', '???', '???', '4 года', 'ib_spb')
        mobility_info('Мировая экономика', 'Москва', 'https://www.hse.ru/ba/we/', 60, 90, '4 года', 'we_msk')
        mobility_info('Программа двух дипломов НИУ ВШЭ и РУТ «Экономика и инженерия транспортных систем»', 'Москва', 'https://dd.hse.ru/miit', '???', '???', '4 года', 'miit_msk')
        mobility_info('Совместная программа по экономике НИУ ВШЭ и РЭШ', 'Москва', 'https://www.hse.ru/ba/nes/', 55, 20, '4 года', 'nes_msk')
        mobility_info('Экономика', 'Москва', 'https://www.hse.ru/ba/economics/', 110, 90, '4 года', 'eco_msk')
        mobility_info('Экономика и анализ данных', 'Москва', 'https://www.hse.ru/ba/eda/', 30, 30, '4 года', 'eda_msk')
        mobility_info('Экономика и бизнес (очно-заочное обучение)', 'Нижний Новгород', 'https://nnov.hse.ru/economics/economics/', 0, 40, '4,5 года', 'eco_nn')
        mobility_info('Экономический анализ', 'Москва', 'https://www.hse.ru/ba/ea/', 0, 20, '4 года', 'ea_msk')
    
    elif form_data[1] == 'Менеджмент':
         mobility_info('Маркетинг и рыночная аналитика', 'Москва', 'https://www.hse.ru/ba/marketing/', 20, 100, '4 года', 'ma_msk')
         mobility_info('Международный бакалавриат по бизнесу и экономике', 'Санкт-Петербург', 'https://spb.hse.ru/ba/interbac/', 60, 60, '4 года', 'ib_spb')
         mobility_info('Международный бакалавриат по бизнесу и экономике', 'Нижний Новгород', 'https://nnov.hse.ru/ba/interbac/', 120, 80, '4 года', 'ib_nn')
         mobility_info('Международный бизнес', 'Москва', 'https://www.hse.ru/ba/ib/', 0, 50, '4 года', 'ib_msk')
         mobility_info('Управление бизнесом', 'Москва', 'https://www.hse.ru/ba/bba/', 30, 170, '4 года', 'bba_msk')
         mobility_info('Управление бизнесом', 'Санкт-Петербург', 'https://spb.hse.ru/ba/business/', 60, 60, '4 года', 'bu_spb')
         mobility_info('Управление цепями поставок и бизнес-аналитика', 'Москва', 'https://www.hse.ru/ba/logistics/', 30, 50, '4 года', 'log_msk')
         mobility_info('Цифровой маркетинг', 'Нижний Новгород', 'https://nnov.hse.ru/ba/dm/', 0, 45, '4 года', 'dm_nn')

    elif form_data[1] == 'История':
        mobility_info('Античность', 'Москва', 'https://www.hse.ru/ba/antiq/', 10, 5, '5 лет', 'ant_msk')
        mobility_info('История', 'Санкт-Петербург', 'https://spb.hse.ru/ba/hist/', 30, 30, '5 лет', 'his_spb')
        mobility_info('История', 'Москва', 'https://www.hse.ru/ba/hist/', 70, 15, '5 лет', 'his_msk')

    elif form_data[1] == 'Юриспруденция':
        mobility_info('Юриспруденция', 'Москва', 'https://www.hse.ru/ba/law/', 150, 90, '5 лет', 'law_msk')
        mobility_info('Юриспруденция', 'Нижний Новгород', 'https://nnov.hse.ru/ba/law/', 55, 45, '5 лет', 'law_nn')
        mobility_info('Юриспруденция', 'Санкт-Петербург', 'https://spb.hse.ru/ba/law/', 90, 90, '5 лет', 'law_spb')
        mobility_info('Юриспруденция: правовое регулирование бизнеса', 'Москва', 'https://pravo.hse.ru/doplaw/', 0, 30, '5,5 лет', 'dop_msk')
        mobility_info('Юриспруденция: цифровой юрист', 'Москва', 'https://www.hse.ru/ba/dlawyer/', 30, 30, '5 лет', 'dl_msk')

    elif form_data[1] == 'Лингвистика':
        mobility_info('Иностранные языки и межкультурная бизнес-коммуникация', 'Нижний Новгород', 'https://nnov.hse.ru/ba/ibc/', 0, 60, '4 года', 'ibc_nn')
        mobility_info('Иностранные языки и межкультурная коммуникация', 'Москва', 'https://www.hse.ru/ba/lang/', 35, 150, '4 года', 'la_msk')
        
    elif form_data[1] == 'Дизайн':
        mobility_info('Дизайн', 'Нижний Новгород', 'https://design.hse.ru/dir/design', 0, 65, '4 года', 'des_nn')
        mobility_info('Дизайн', 'Санкт-Петербург', 'https://spb.hse.ru/ba/designs/', 20, 110, '4 года', 'des_spb')
        mobility_info('Дизайн', 'Москва', 'https://design.hse.ru/ba/program/design', 65, 350, '4 года', 'des_msk')
        mobility_info('Мода', 'Москва', 'https://design.hse.ru/ba/program/fashion', 0, 80, '4 года', 'fash_msk')

@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call): #осуществление записи на мобильность, здесь нужно реализовать добавление данных о мобильности в таблицу
    for i in range(-4,0):
        bot.delete_message(call.chatid,call.messageid-1)
    try:
        if call.message:
            if call.data == "se_msk":
                bot.send_message(call.message.chat.id, 'Вы успешно записались на обрзовательную программу "Програмная инженерия" в городе Москва!')
            if call.data == "se_nn":
                bot.send_message(call.message.chat.id, 'Вы успешно записались на обрзовательную программу "Программная инженерия (очно-заочное обучение)" в городе Нижний Новгород!')
    except Exception as e:
        print(repr(e))
    bot.send_message(call.message.chat.id, 'Или нет...')
bot.infinity_polling()
