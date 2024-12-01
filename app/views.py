from django.shortcuts import render
from django.conf import settings
import telebot
from .models import Product


bot = telebot.TeleBot(settings.BOT_TOKEN)


@bot.message_handler(commands=['start'])
def send_welcome(message):
	bot.reply_to(message, f"Hello, {message.from_user.first_name} \nType /help to list comands")


@bot.message_handler(commands=['help'])
def send_welcome(message):
	bot.reply_to(message, f"Get list of products: /products \nCreate product: /create_product <quantity> <price> <name>")


@bot.message_handler(commands=['create_product'])
def send_welcome(message):
    products = Product.objects.all()
    text = ""
    for product in products:
        text += f"Name: {product.name}, Quantity: {product.quantity}, Price: {product.price}\n"
    bot.send_message(message.from_user.id, text)