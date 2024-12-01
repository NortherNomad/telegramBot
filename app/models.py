from django.db import models


class Product(models.Model):
    quantity = models.IntegerField(verbose_name="Количество товара", default=0)
    price = models.IntegerField(verbose_name="Цена товара")
    name = models.CharField(max_length=250, verbose_name="Название товара")
    