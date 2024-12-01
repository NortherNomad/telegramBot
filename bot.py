import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'almau.settings')
django.setup()

import telebot
from almau import settings
from app.models import Product

bot = telebot.TeleBot(settings.BOT_TOKEN)


@bot.message_handler(commands=['start'])
def send_welcome(message):
	bot.reply_to(message, f"Hello, {message.from_user.first_name} \nType /help to list comands")


@bot.message_handler(commands=['help'])
def help_command(message):
	bot.reply_to(message, f"Get list of products: /products \nCreate product: /create_product")


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
def start_create_product(message: telebot.types.Message):
    msg = bot.send_message(message.from_user.id, 'type product name')
    bot.register_next_step_handler(msg, get_product_name, {})

def get_product_name(message: telebot.types.Message, product_data: dict):
    product_data['name'] = message.text
    if not product_data['name']:
        msg = bot.send_message(message.from_user.id, 'Product name can not be empty. Try again:')
        bot.register_next_step_handler(msg, get_product_name, product_data)
        return
    msg = bot.send_message(message.from_user.id, 'type product quantity')
    bot.register_next_step_handler(msg, get_product_quantity, product_data)
    
def get_product_quantity(message: telebot.types.Message, product_data: dict):
    try:
          product_data['quantity'] = int(message.text)
          if product_data['quantity'] < 0:
               raise ValueError
    except ValueError:
        msg = bot.send_message(message.from_user.id, "Invalid quantity. Please type a valid positive integer:")
        bot.register_next_step_handler(msg, get_product_quantity, product_data)
        return
    
    msg = bot.send_message(message.from_user.id, 'type product price')
    bot.register_next_step_handler(msg, get_product_price, product_data)
    

def get_product_price(message: telebot.types.Message, product_data: dict):
    try:
        product_data['price'] = float(message.text.strip())
        if product_data['price'] <= 0:
            raise ValueError
    except ValueError:
        msg = bot.send_message(message.from_user.id, "Invalid price. Please type a valid positive integer:")
        bot.register_next_step_handler(msg, get_product_price, product_data)
        return

    if Product.objects.filter(**product_data).exists():
        bot.send_message(message.from_user.id, "Product already exists")
        return

    Product.objects.create(**product_data)
    bot.send_message(message.from_user.id, 'product created')


def main():
     bot.infinity_polling()
     
if __name__ == "__main__":
     main()