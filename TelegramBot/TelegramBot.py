import telebot

bot = telebot.TeleBot('7162103985:AAEimCQMejkVTqVvcyLul-nZTHVn8wWfOyA')

@bot.message_handler(commands=['start'])

def main(message):
    bot.send_message(message.chat.id, 'Привет!')

bot.infinity_polling()
