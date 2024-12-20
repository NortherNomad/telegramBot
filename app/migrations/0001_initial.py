# Generated by Django 5.1.3 on 2024-11-29 16:53

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField(default=0, verbose_name='Количество товара')),
                ('price', models.IntegerField(verbose_name='Цена товара')),
                ('name', models.CharField(max_length=250, verbose_name='Название товара')),
            ],
        ),
    ]
