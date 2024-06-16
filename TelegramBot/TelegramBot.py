import telebot
import gspread
import re
from telebot import types

bot = telebot.TeleBot('7037301667:AAHAflz1Bl0vW7KDGc46FtopxFeRIdt445A')

credentials = gspread.service_account(filename='credentials.json') 
sheet = credentials.open_by_key('1BCzJ14uwHL9cCjReBrcIggh1rYhsZIYlm8R8CUe6o5Q')
worksheet = sheet.sheet1

# Словарь для хранения данных, специфичных для пользователя
user_data = {}

@bot.message_handler(commands=['start', 'back']) #главное меню
def start(message):
    # Инициализация данных, специфичных для пользователя
    user_data[message.chat.id] = []
    
    # Приветственное сообщение и создание кнопки для заполнения анкеты
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    btn1 = types.KeyboardButton('Заполнить анкету')
    btn2 = types.KeyboardButton('Помощь')
    markup.add(btn1).add(btn2)
    if message.text == '/start':
        bot.send_message(message.chat.id, 'Привет! Я бот для заполнения анкеты на межкампусную мобильность.', reply_markup=markup)
        bot.send_message(message.chat.id, 'Перед заполнением анкеты рекомендуется прочитать полезную информацию по кнопке "Помощь".')
    elif message.text == 'Назад':
        bot.send_message(message.chat.id, 'Готовы заполнить анкету? Тогда вперёд!', reply_markup=markup)
    elif message.text.lower() == 'да':
        bot.send_message(message.chat.id, 'Спасибо, ваша анкета успешно заполнена!', reply_markup=markup)
    elif message.text == '/back':
        bot.send_message(message.chat.id, 'Теперь вы можете заполнить новую анкету!', reply_markup=markup)
    else:
        bot.send_message(message.chat.id, 'Пожалуйста, следуйте инструкциям.', reply_markup=markup)
        
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
    if message.text == '1' or message.text == '2' or message.text == '3' or message.text == '4':
        # Сохранение выбранного курса пользователя
        user_data[message.chat.id].append(message.text)
    
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
        elif message.text == '3' or message.text == '4': #направления 3 и 4 курсов
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
    else:
        bot.send_message(message.chat.id, 'Пожалуйста, выберите один из представленных вариантов ответа.')
        bot.register_next_step_handler(message, select_direction)

def enter_lastname(message):
    if message.text == 'Программная инженерия' or message.text == 'Бизнес-информатика' or message.text == 'Экономика' or message.text == 'Менеджмент' or message.text == 'История' or message.text == 'Юриспруденция' or message.text == 'Дизайн' or message.text == 'Лингвистика':
        # Сохранение выбранного направления пользователя
        user_data[message.chat.id].append(message.text)
    
        # Запрос фамилии
        bot.send_message(message.chat.id, 'Введите вашу фамилию:', reply_markup=types.ReplyKeyboardRemove())
        bot.register_next_step_handler(message, enter_firstname)
    else:
        bot.send_message(message.chat.id, 'Пожалуйста, выберите один из представленных вариантов ответа.')
        bot.register_next_step_handler(message, enter_lastname)

def enter_firstname(message):
    # Сохранение фамилии пользователя
    user_data[message.chat.id].append(message.text)
    
    # Запрос имени
    bot.send_message(message.chat.id, 'Введите ваше имя:')
    bot.register_next_step_handler(message, enter_secondname)

def enter_secondname(message):
    # Сохранение имени пользователя
    user_data[message.chat.id].append(message.text)
    
    # Запрос отчества
    bot.send_message(message.chat.id, 'Введите ваше отчество:')
    bot.register_next_step_handler(message, enter_hsemail)

def enter_hsemail(message):
    # Сохранение отчества пользователя
    user_data[message.chat.id].append(message.text)
    
    # Запрос корпоративной почты
    bot.send_message(message.chat.id, 'Введите адрес вашей корпоративной почты (учтите, что адрес почты должен оканчиваться на "@edu.hse.ru"):')
    bot.register_next_step_handler(message, was_or_not)
        
def was_or_not(message):
    pattern = re.compile(r'^[a-zA-Z][a-zA-Z0-9_]*$')
    if message.text[-11:] == "@edu.hse.ru" and len(message.text) > 11 and pattern.match(message.text[:-11]): #проверка на правильность ввода корпоративной почты
        # Сохранение корпоративной почты пользователя
        user_data[message.chat.id].append(message.text)
        # Узнаём у пользователя, бывал ли он на мобильности ранее
        markup_was = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
        btn1= types.KeyboardButton('Да')
        btn2= types.KeyboardButton('Нет')
        markup_was.row(btn1,btn2)
        bot.send_message(message.chat.id, 'Принимали ли вы участие в межкампусной мобильности ранее?', reply_markup=markup_was)
        bot.register_next_step_handler(message, enter_period)
    else:
        bot.send_message(message.chat.id, 'Адрес вашей корпоративной почты введён некорректно! Повторите ввод. Адрес почты должен оканчиваться на "@edu.hse.ru".')
        bot.register_next_step_handler(message, was_or_not)

def enter_period(message):
    if message.text == 'Да' or message.text == 'Нет':
        # Сохранение ответа пользователя о предыдущем участии в мобильности
        user_data[message.chat.id].append(message.text)
        if message.text == 'Да':
            bot.send_message(message.chat.id, 'Учтите, что при отборе студентов на мобильность высшим приоритетом обладают студенты, ранее не принимавшие участие в мобильности.')
        # Узнаём у пользователя, на какой срок он собирается на мобильность
        markup_was = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
        if user_data[message.chat.id][0] == '4': 
            btn0= types.KeyboardButton('1 модуль')
            btn1= types.KeyboardButton('2 модуля')
            btn2= types.KeyboardButton('3 модуля')
            markup_was.row(btn0,btn1)
            markup_was.row(btn2)
        else:
            btn0= types.KeyboardButton('1 модуль')
            btn1= types.KeyboardButton('2 модуля')
            btn3= types.KeyboardButton('3 модуля')
            btn2= types.KeyboardButton('4 модуля')
            markup_was.row(btn0,btn1)
            markup_was.row(btn3,btn2)
        bot.send_message(message.chat.id, 'На какой срок вы собираетесь отправиться на мобильность?', reply_markup=markup_was)
        bot.register_next_step_handler(message, confirm_data)
    else:
        bot.send_message(message.chat.id, 'Пожалуйста, выберите один из представленных вариантов ответа.')
        bot.register_next_step_handler(message, enter_period)
        

def confirm_data(message):
    if message.text == '1 модуль' or message.text == '2 модуля' or message.text == '3 модуля' or message.text == '4 модуля':
        # Сохранение выбранного срока мобильности пользователя
        user_data[message.chat.id].append(message.text)
        # Вывод анкеты для проверки
        confirmation_text = f"Ваша анкета:\n\n" \
                            f"Курс: {user_data[message.chat.id][0]}\n" \
                            f"Направление: {user_data[message.chat.id][1]}\n" \
                            f"Фамилия: {user_data[message.chat.id][2]}\n" \
                            f"Имя: {user_data[message.chat.id][3]}\n" \
                            f"Отчество: {user_data[message.chat.id][4]}\n" \
                            f"Корпоративная почта: {user_data[message.chat.id][5]}\n" \
                            f"Посещал ли мобильность ранее: {user_data[message.chat.id][6]}\n" \
                            f"Срок текущей мобильности: {user_data[message.chat.id][7]}\n\n" \
                            f"Данные верны?"
    
        # Создание кнопок для подтверждения данных
        markup_confirmation = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
        yes = types.KeyboardButton('Да')
        no = types.KeyboardButton('Нет')
        markup_confirmation.row(yes,no)
        bot.send_message(message.chat.id, confirmation_text, reply_markup=markup_confirmation)
        bot.register_next_step_handler(message, form_is_correct)
    else:
        bot.send_message(message.chat.id, 'Пожалуйста, выберите один из представленных вариантов ответа.')
        bot.register_next_step_handler(message, confirm_data)
def form_is_correct(message):
    # Обработка выбора пользователя
    if message.text.lower() == 'да':
        mobility(message)
    elif message.text.lower() == 'нет':
        # Данные неверны
        bot.send_message(message.chat.id, 'Пожалуйста, введите данные заново.')
        user_data[message.chat.id].clear()
        select_course(message)
    else:
        bot.send_message(message.chat.id, 'Пожалуйста, выберите один из представленных вариантов ответа.')
        bot.register_next_step_handler(message, form_is_correct)
        
@bot.message_handler(commands=['help']) #помощь
def help_inf(message):
    help_info = 'Я бот для заполнения анкеты на межкампусную мобильность. Через меня ты сможешь подать заявку для участия в межкампусной мобильности. Для этого просто начни заполнять анкету. Когда ты выберешь свой курс и направление, я сам предложу тебе варианты, в какой город и на какое направление ты сможешь отправиться. Помни, ты должен честно заполнять все данные! Иначе на мобильность не возьмём. :)'
    feedback = 'Возникли проблемы? Свяжись с разработчиками! \nhttps://t.me/brokenbytheway \nhttps://t.me/dedbezpasportaideneg'
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    btn1 = types.KeyboardButton('Назад')
    markup.add(btn1)
    if message.text == 'Помощь':
        bot.send_message(message.chat.id, help_info, reply_markup=markup)
        bot.send_message(message.chat.id, feedback)
    else:
        bot.send_message(message.chat.id, 'Пожалуйста, следуйте инструкциям.', reply_markup=markup)
    bot.register_next_step_handler(message, next_command2)
    
def next_command2(message): #переход на следующую команду
    if message.text == 'Назад':
        start(message)
    else:
        help_inf(message)
 # ---------------------- ДАННЫЕ О НАПРАВЛЕНИЯХ ДЛЯ МОБИЛЬНОСТИ -----------------------------
drip_msk = ['Дизайн и разработка информационных продуктов', 'Москва', 'https://www.hse.ru/ba/drip/', 'drip_msk']
cst_nn = ['Компьютерные науки и технологии', 'Нижний Новгород', 'https://nnov.hse.ru/ba/cst/', 'cst_nn']
se_msk = ['Программная инженерия', 'Москва', 'https://www.hse.ru/ba/se/', 'se_msk']
ait_nn = ['Технологии искусственного и дополненного интеллекта', 'Нижний Новгород', 'https://nnov.hse.ru/ba/ait/', 'ait_nn']
bi_msk = ['Бизнес-информатика', 'Москва', 'https://www.hse.ru/ba/bi/', 'bi_msk']
bi_spb = ['Бизнес-информатика', 'Санкт-Петербург', 'https://spb.hse.ru/ba/bi/', 'bi_spb']
cst_nn = ['Компьютерные науки и технологии', 'Нижний Новгород', 'https://nnov.hse.ru/ba/cst/', 'cst_nn']
dig_msk = ['Управление цифровым продуктом', 'Москва', 'https://www.hse.ru/ba/digital/', 'dig_msk']
ed_spb = ['Аналитика в экономике', 'Санкт-Петербург', 'https://spb.hse.ru/ba/economicdata/', 'ed_spb']
icef_msk = ['Международная программа по экономике и финансам', 'Москва', 'https://www.hse.ru/ba/icef/', 'icef_msk']
ib_nn = ['Международный бакалавриат по бизнесу и экономике', 'Нижний Новгород', 'https://nnov.hse.ru/ba/interbac/', 'ib_nn']
ib_spb = ['Международный бакалавриат по бизнесу и экономике', 'Санкт-Петербург', 'https://spb.hse.ru/ba/interbac/', 'ib_spb']
we_msk = ['Мировая экономика', 'Москва', 'https://www.hse.ru/ba/we/', 'we_msk']
eco_msk = ['Экономика', 'Москва', 'https://www.hse.ru/ba/economics/', 'eco_msk']
eda_msk = ['Экономика и анализ данных', 'Москва', 'https://www.hse.ru/ba/eda/', 'eda_msk']
ea_msk = ['Экономический анализ', 'Москва', 'https://www.hse.ru/ba/ea/', 'ea_msk']
ma_msk = ['Маркетинг и рыночная аналитика', 'Москва', 'https://www.hse.ru/ba/marketing/', 'ma_msk']
ib_spb = ['Международный бакалавриат по бизнесу и экономике', 'Санкт-Петербург', 'https://spb.hse.ru/ba/interbac/', 'ib_spb']
ib_nn = ['Международный бакалавриат по бизнесу и экономике', 'Нижний Новгород', 'https://nnov.hse.ru/ba/interbac/', 'ib_nn']
ib_msk = ['Международный бизнес', 'Москва', 'https://www.hse.ru/ba/ib/', 'ib_msk']
bba_msk = ['Управление бизнесом', 'Москва', 'https://www.hse.ru/ba/bba/', 'bba_msk']
bu_spb = ['Управление бизнесом', 'Санкт-Петербург', 'https://spb.hse.ru/ba/business/', 'bu_spb']
log_msk = ['Управление цепями поставок и бизнес-аналитика', 'Москва', 'https://www.hse.ru/ba/logistics/', 'log_msk']
dm_nn = ['Цифровой маркетинг', 'Нижний Новгород', 'https://nnov.hse.ru/ba/dm/', 'dm_nn']
ant_msk = ['Античность', 'Москва', 'https://www.hse.ru/ba/antiq/', 'ant_msk']
his_spb = ['История', 'Санкт-Петербург', 'https://spb.hse.ru/ba/hist/', 'his_spb']
his_msk = ['История', 'Москва', 'https://www.hse.ru/ba/hist/', 'his_msk']
law_msk = ['Юриспруденция', 'Москва', 'https://www.hse.ru/ba/law/', 'law_msk']
law_nn = ['Юриспруденция', 'Нижний Новгород', 'https://nnov.hse.ru/ba/law/', 'law_nn']
law_spb = ['Юриспруденция', 'Санкт-Петербург', 'https://spb.hse.ru/ba/law/', 'law_spb']
dop_msk = ['Юриспруденция: правовое регулирование бизнеса', 'Москва', 'https://pravo.hse.ru/doplaw/', 'dop_msk']
dl_msk = ['Юриспруденция: цифровой юрист', 'Москва', 'https://www.hse.ru/ba/dlawyer/', 'dl_msk']
ibc_nn = ['Иностранные языки и межкультурная бизнес-коммуникация', 'Нижний Новгород', 'https://nnov.hse.ru/ba/ibc/', 'ibc_nn']
la_msk = ['Иностранные языки и межкультурная коммуникация', 'Москва', 'https://www.hse.ru/ba/lang/', 'la_msk']
des_nn = ['Дизайн', 'Нижний Новгород', 'https://design.hse.ru/dir/design', 'des_nn']
des_spb = ['Дизайн', 'Санкт-Петербург', 'https://spb.hse.ru/ba/designs/', 'des_spb']
des_msk = ['Дизайн', 'Москва', 'https://design.hse.ru/ba/program/design', 'des_msk']
fash_msk = ['Мода', 'Москва', 'https://design.hse.ru/ba/program/fashion', 'fash_msk']
stat_msk = ['Экономика и статистика', 'Москва', 'https://www.hse.ru/ba/stat/', 'stat_msk']
# -------------------------------------------------------------------------------------------
@bot.message_handler(commands=['mobility']) #выбор мобильности
def mobility(message):
    
    def mobility_info(mob): #функция для вывода информации об одном направлении
        markup = types.InlineKeyboardMarkup()
        site = types.InlineKeyboardButton('Ознакомиться с программой', url = mob[2])
        register = types.InlineKeyboardButton('Записаться', callback_data = mob[3])
        markup.row(site, register)
        text = f"*Программа: {mob[0]}\n*" \
               f"*Город: {mob[1]}\n*"
        bot.send_message(message.chat.id, text, reply_markup=markup, parse_mode='Markdown')
        
    bot.send_message(message.chat.id, "Исходя из вашего направления, мы можем предложить вам следующие варианты межкампусной мобильности:", reply_markup=types.ReplyKeyboardRemove())
    if user_data[message.chat.id][1] == 'Программная инженерия':
        mobility_info(drip_msk)
        mobility_info(cst_nn)
        mobility_info(se_msk)
        mobility_info(ait_nn)
        
    elif user_data[message.chat.id][1] == 'Бизнес-информатика':
        mobility_info(bi_msk)
        mobility_info(bi_spb)
        mobility_info(cst_nn)
        mobility_info(dig_msk)

    elif user_data[message.chat.id][1] == 'Экономика':
        mobility_info(ed_spb)
        mobility_info(icef_msk)
        mobility_info(ib_nn)
        mobility_info(ib_spb)
        mobility_info(we_msk)
        mobility_info(eco_msk)
        mobility_info(eda_msk)
        mobility_info(ea_msk)
        mobility_info(stat_msk)
    
    elif user_data[message.chat.id][1] == 'Менеджмент':
         mobility_info(ma_msk)
         mobility_info(ib_spb)
         mobility_info(ib_nn)
         mobility_info(ib_msk)
         mobility_info(bba_msk)
         mobility_info(bu_spb)
         mobility_info(log_msk)
         mobility_info(dm_nn)

    elif user_data[message.chat.id][1] == 'История':
        mobility_info(ant_msk)
        mobility_info(his_spb)
        mobility_info(his_msk)

    elif user_data[message.chat.id][1] == 'Юриспруденция':
        mobility_info(law_msk)
        mobility_info(law_nn)
        mobility_info(law_spb)
        mobility_info(dop_msk)
        mobility_info(dl_msk)

    elif user_data[message.chat.id][1] == 'Лингвистика':
        mobility_info(ibc_nn)
        mobility_info(la_msk)
        
    elif user_data[message.chat.id][1] == 'Дизайн':
        mobility_info(des_nn)
        mobility_info(des_spb)
        mobility_info(des_msk)
        mobility_info(fash_msk)
    bot.send_message(message.chat.id, 'Вы можете записаться сразу на несколько мобильностей!')

@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call): #осуществление записи на мобильность, здесь нужно реализовать добавление данных о мобильности в таблицу
    #функция для записи данных в таблицу
    def fill_table(form_data, mob):
        worksheet.append_row([user_data[call.message.chat.id][0], user_data[call.message.chat.id][1], user_data[call.message.chat.id][2], user_data[call.message.chat.id][3], user_data[call.message.chat.id][4], user_data[call.message.chat.id][5], user_data[call.message.chat.id][6],  mob[0], mob[1], user_data[call.message.chat.id][7]])
        bot.send_message(call.message.chat.id, f'Вы успешно записались на образовательную программу "{mob[0]}" в городе {mob[1]} на срок в {form_data[7]}!')
        markup_back = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
        markup_back.add(types.KeyboardButton('/back'))
        bot.send_message(call.message.chat.id, 'Вы можете записаться на ещё одну программу или вернуться в главное меню по кнопке /back', reply_markup=markup_back)
        
    #обрабатываем кнопки, записываем данные в таблицу
    if call.message:
        if call.data == "drip_msk":
            fill_table(user_data[call.message.chat.id], drip_msk)
        elif call.data == "cst_nn":
            fill_table(user_data[call.message.chat.id], cst_nn)
        elif call.data == "se_msk":
            fill_table(user_data[call.message.chat.id], se_msk)
        elif call.data == "ait_nn":
            fill_table(user_data[call.message.chat.id], ait_nn)
        elif call.data == "bi_msk":
            fill_table(user_data[call.message.chat.id], bi_msk)
        elif call.data == "bi_spb":
            fill_table(user_data[call.message.chat.id], bi_spb)
        elif call.data == "cst_nn":
            fill_table(user_data[call.message.chat.id], cst_nn)
        elif call.data == "dig_msk":
            fill_table(user_data[call.message.chat.id], dig_msk)
        elif call.data == "ed_spb":
            fill_table(user_data[call.message.chat.id], ed_spb)
        elif call.data == "icef_msk":
            fill_table(user_data[call.message.chat.id], icef_msk)
        elif call.data == "ib_nn":
            fill_table(user_data[call.message.chat.id], ib_nn)
        elif call.data == "ib_spb":
            fill_table(user_data[call.message.chat.id], ib_spb)
        elif call.data == "we_msk":
            fill_table(user_data[call.message.chat.id], we_msk)
        elif call.data == "eco_msk":
            fill_table(user_data[call.message.chat.id], eco_msk)
        elif call.data == "eda_msk":
            fill_table(user_data[call.message.chat.id], eda_msk)
        elif call.data == "ea_msk":
            fill_table(user_data[call.message.chat.id], ea_msk)
        elif call.data == "ma_msk":
            fill_table(user_data[call.message.chat.id], ma_msk)
        elif call.data == "ib_spb":
            fill_table(user_data[call.message.chat.id], ib_spb)
        elif call.data == "ib_nn":
            fill_table(user_data[call.message.chat.id], ib_nn)
        elif call.data == "ib_msk":
            fill_table(user_data[call.message.chat.id], ib_msk)
        elif call.data == "bba_msk":
            fill_table(user_data[call.message.chat.id], bba_msk)
        elif call.data == "bu_spb":
            fill_table(user_data[call.message.chat.id], bu_spb)
        elif call.data == "log_msk":
            fill_table(user_data[call.message.chat.id], log_msk)
        elif call.data == "dm_nn":
            fill_table(user_data[call.message.chat.id], dm_nn)
        elif call.data == "ant_msk":
            fill_table(user_data[call.message.chat.id], ant_msk)
        elif call.data == "his_spb":
            fill_table(user_data[call.message.chat.id], his_spb)
        elif call.data == "his_msk":
            fill_table(user_data[call.message.chat.id], his_msk)
        elif call.data == "law_msk":
            fill_table(user_data[call.message.chat.id], law_msk)
        elif call.data == "law_nn":
            fill_table(user_data[call.message.chat.id], law_nn)
        elif call.data == "law_spb":
            fill_table(user_data[call.message.chat.id], law_spb)
        elif call.data == "dop_msk":
            fill_table(user_data[call.message.chat.id], dop_msk)
        elif call.data == "dl_msk":
            fill_table(user_data[call.message.chat.id], dl_msk)
        elif call.data == "ibc_nn":
            fill_table(user_data[call.message.chat.id], ibc_nn)
        elif call.data == "la_msk":
            fill_table(user_data[call.message.chat.id], la_msk)
        elif call.data == "des_nn":
            fill_table(user_data[call.message.chat.id], des_nn)
        elif call.data == "des_spb":
            fill_table(user_data[call.message.chat.id], des_spb)
        elif call.data == "des_msk":
            fill_table(user_data[call.message.chat.id], des_msk)
        elif call.data == "fash_msk":
            fill_table(user_data[call.message.chat.id], fash_msk)
        elif call.data == "stat_msk":
            fill_table(user_data[call.message.chat.id], stat_msk)
bot.infinity_polling()
