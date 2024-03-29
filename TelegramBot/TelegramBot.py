import telebot

bot = telebot.TeleBot('7162103985:AAEimCQMejkVTqVvcyLul-nZTHVn8wWfOyA')

@bot.message_handler(commands=['start'])

def main(message):
    bot.send_message(message.chat.id, '���� ����!')
    bot.send_message('до встречи!')
    bot.send_message('До скорой встречи!')

bot.infinity_polling()
