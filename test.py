import telebot

bot = telebot.TeleBot("7586259913:AAGS3QxQLEJBSjMzZjZaggfOiyIRA9lnw8c", parse_mode=None)

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
	bot.reply_to(message, "Howdy, how are you doing?")

@bot.message_handler(func=lambda m: True)
def echo_all(message: telebot.types.Message):
	bot.send_message(message.from_user.id, f"Hello, {message.from_user.first_name}")

bot.infinity_polling()
