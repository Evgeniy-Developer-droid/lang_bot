from django.urls import path
from bot.bot import bot_webhook
from manager_app.views import PayCallbackView
import os

urlpatterns = [
    path(f"webhook/{os.environ.get('BOT_KEY')}/", bot_webhook),
    path(f"liqpay-callback", PayCallbackView.as_view())
]
