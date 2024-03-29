import telebot

bot = telebot.TeleBot('7162103985:AAEimCQMejkVTqVvcyLul-nZTHVn8wWfOyA')

@bot.message_handler(commands=['start'])

def main(message):
    bot.send_message(message.chat.id, 'до свидания 3 модуль')
    bot.send_message(message.chat.id, 'до встречи!')
    bot.send_message(message.chat.id, 'До скорой встречи!')
    

bot.infinity_polling()
