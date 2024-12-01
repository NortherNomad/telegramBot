import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'almau.settings')
django.setup()

import telebot
from almau import settings
from app.schemas import CreateProductIn
from app.models import Product

bot = telebot.TeleBot(settings.BOT_TOKEN)


@bot.message_handler(commands=['start'])
def send_welcome(message):
	bot.reply_to(message, f"Hello, {message.from_user.first_name} \nType /help to list comands")


@bot.message_handler(commands=['help'])
def help_command(message):
	bot.reply_to(message, f"Get list of products: /products \nCreate product: /create_product <quantity> <price> <name>")


@bot.message_handler(commands=['products'])
def get_products(message):
    products = Product.objects.all()
    if len(products) == 0:
          bot.send_message(message.from_user.id, "No products")
          return
    text = ""
    for product in products:
        text += f"Name: {product.name}, Quantity: {product.quantity}, Price: {product.price}\n"
    bot.send_message(message.from_user.id, text)


@bot.message_handler(commands=['create_product'])
def get_products(message: telebot.types.Message):
    text = message.text.split()
    if len(text) < 4:
        bot.send_message(message.from_user.id, "Fill all necessary data to create product")
        return
    try:
        params = CreateProductIn(quantity=text[1], price=text[2], name=" ".join(text[3:]))
    except:
        bot.send_message(message.from_user.id, "Quantity and price must be numbers")
        return

    if Product.objects.filter(quantity=params.quantity, price=params.price, name=params.name).exists():
        bot.send_message(message.from_user.id, "Product already exists")
        return

    Product.objects.create(
        quantity=params.quantity,
        price=params.price,
        name=params.name
    )
    bot.send_message(message.from_user.id, "Product was created")
    
def main():
     bot.infinity_polling()
     
if __name__ == "__main__":
     main()