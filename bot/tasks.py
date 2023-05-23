
import os
import random
import telebot
from server.celery import app
from datetime import datetime, timedelta
from manager_app.models import *
from dictionary_app.models import *
from django.utils import timezone


bot = telebot.TeleBot(os.environ.get("BOT_KEY"))


@app.task
def morning_word_list_task():
    active_subs = SubNow.objects.filter(active=True)
    for sub in active_subs:
        if sub.end < timezone.now():
            sub.active = False
            sub.save()
            continue
        challenge_time_period = 12 * 60 * 60  # 12 hours
        deadline_time = 1 * 60 * 60 # 1 hour

        id_list = Word.objects.filter(published=True).values_list('id', flat=True)
        random_id_list = random.sample(list(id_list), sub.sub.max_words)
        queryset = Word.objects.filter(id__in=random_id_list)

        id_list_p = Phrase.objects.filter(published=True).values_list('id', flat=True)
        random_id_list_p = random.sample(list(id_list_p), sub.sub.max_phrases)
        queryset_p = Phrase.objects.filter(id__in=random_id_list_p)

        count_challenge_time = 0
        for item in queryset:
            next_part_time = int(challenge_time_period / (sub.sub.max_words + sub.sub.max_phrases)) - 10
            count_challenge_time += next_part_time
            Challenge.objects.create(
                user=sub.user,
                word=item,
                date_send=timezone.now()+timedelta(seconds=count_challenge_time),
                deadline_send=timezone.now()+timedelta(seconds=count_challenge_time+deadline_time),
            )
        for item in queryset_p:
            next_part_time = int(challenge_time_period / (sub.sub.max_words + sub.sub.max_phrases)) - 10
            count_challenge_time += next_part_time
            Challenge.objects.create(
                user=sub.user,
                phrase=item,
                date_send=timezone.now()+timedelta(seconds=count_challenge_time),
                deadline_send=timezone.now()+timedelta(seconds=count_challenge_time+deadline_time),
            )
        message = "Доброго ранку\! Сьогодні маємо такий список слів для практики:\n"
        message += "||"
        for item in queryset:
            message += f"{item.word} \- {item.translate}\n"
        message += "\n"
        for item in queryset_p:
            message += f"{item.phrase} \- {item.translate}\n"
        message += "||"
        bot.send_message(str(sub.user.user_id), message, parse_mode='MarkdownV2')

@app.task
def challenge_task():
    challenges = Challenge.objects.all()
    for challenge in challenges:
        if timezone.now() > challenge.deadline_send:
            challenge.delete()
        elif challenge.date_send < timezone.now() < challenge.deadline_send:
            markup = telebot.types.InlineKeyboardMarkup()
            markup.row_width = 1
            ch = random.choice(['e', 'u'])
            if ch == 'e':
                if challenge.word:
                    markup.add(
                        telebot.types.InlineKeyboardButton("Перевести", callback_data=f"answer|e|{challenge.word.word}")
                    )
                    bot.send_message(str(challenge.user.user_id),
                                    f"Завдання. Переведіть на англійську: {challenge.word.translate}", 
                                    reply_markup=markup)
                else:
                    markup.add(
                        telebot.types.InlineKeyboardButton("Перевести", callback_data=f"answer|e|{challenge.phrase.phrase}")
                    )
                    bot.send_message(str(challenge.user.user_id),
                                    f"Завдання. Переведіть на англійську: {challenge.phrase.translate}", 
                                    reply_markup=markup)
            else:
                if challenge.word:
                    markup.add(
                        telebot.types.InlineKeyboardButton("Перевести", callback_data=f"answer|u|{challenge.word.translate}")
                    )
                    bot.send_message(str(challenge.user.user_id),
                                    f"Завдання. Переведіть на українську: {challenge.word.word}", 
                                    reply_markup=markup)
                else:
                    markup.add(
                        telebot.types.InlineKeyboardButton("Перевести", callback_data=f"answer|u|{challenge.phrase.translate}")
                    )
                    bot.send_message(str(challenge.user.user_id),
                                    f"Завдання. Переведіть на українську: {challenge.phrase.phrase}", 
                                    reply_markup=markup)
            challenge.delete()
