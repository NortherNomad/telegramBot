import os
import threading
from django.apps import AppConfig


class AppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'app'

    def ready(self):
        from app.bot import bot

        def run_bot():
            bot.polling(non_stop=True)
        
        if os.environ.get('RUN_MAIN') == 'true':
            threading.Thread(target=run_bot, daemon=True).start()