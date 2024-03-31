import telebot
import gspread

bot = telebot.TeleBot('7162103985:AAEimCQMejkVTqVvcyLul-nZTHVn8wWfOyA')

gc = gspread.service_account(filename='credentials.json') 
sheet = gc.open_by_key('1BCzJ14uwHL9cCjReBrcIggh1rYhsZIYlm8R8CUe6o5Q')
ws = sheet.sheet1

@bot.message_handler(commands=['start'])
def start(message): 
    bot.send_message(message.chat.id, 'Привет! Напиши мне что-нибудь, и я добавлю это в гугл таблицу.')
    
@bot.message_handler(func=lambda m: True) 
def add_link(message): 
    link = message.text 
    ws.append_row([link]) 
    bot.send_message(message.chat.id, 'Текст успешно добавлен в таблицу!') 
    
bot.infinity_polling()
