
import os
import random
import telebot
from server.celery import app
from datetime import timedelta
from manager_app.models import *
from dictionary_app.models import *
from django.utils import timezone
from manager_tools import markdown_filter
import sys

sys.stdout.flush()


bot = telebot.TeleBot(os.environ.get("BOT_KEY"))


@app.task
def morning_word_list_task():
    active_subs = SubNow.objects.filter(active=True)
    for sub in active_subs:
        if sub.end < timezone.now():
            sub.active = False
            sub.save()
            try:
                message = "Термін дії вашої підписки заківчився! Оформіть підписку знову."
                bot.send_message(str(sub.user.user_id), message)
            except Exception as e:
                Log.objects.create(
                    source="bot/tasks.py/morning_word_list_task()",
                    status="info",
                    value=f"{str(e)} - user:{str(sub.user.user_id)}"
                )
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
        for item_wi in queryset:
            next_part_time = int(challenge_time_period / (sub.sub.max_words + sub.sub.max_phrases)) - 10
            count_challenge_time += next_part_time
            Challenge.objects.create(
                user=sub.user,
                word=item_wi,
                date_send=timezone.now()+timedelta(seconds=count_challenge_time),
                deadline_send=timezone.now()+timedelta(seconds=count_challenge_time+deadline_time),
            )
        for item_pi in queryset_p:
            next_part_time = int(challenge_time_period / (sub.sub.max_words + sub.sub.max_phrases)) - 10
            count_challenge_time += next_part_time
            Challenge.objects.create(
                user=sub.user,
                phrase=item_pi,
                date_send=timezone.now()+timedelta(seconds=count_challenge_time),
                deadline_send=timezone.now()+timedelta(seconds=count_challenge_time+deadline_time),
            )
        try:
            message = "Доброго ранку! Сьогодні маємо такий список для практики:"
            bot.send_message(str(sub.user.user_id), message)

            message_w = ""
            for item_w in queryset:
                message_w += f"{item_w.word} - {item_w.translate}\n"
            bot.send_message(str(sub.user.user_id), f'||{markdown_filter(message_w)}||', parse_mode='MarkdownV2')

            message_p = ""
            for item_p in queryset_p:
                message_p += f"{item_p.phrase} - {item_p.translate}\n"
            bot.send_message(str(sub.user.user_id), f'||{markdown_filter(message_p)}||', parse_mode='MarkdownV2')
        except Exception as e:
            # print("morning_word_list_task  "+str(e), flush=True)
            Log.objects.create(
                source="bot/tasks.py/morning_word_list_task()",
                status="info",
                value=f"{str(e)} - user:{str(sub.user.user_id)}"
            )

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
            try:
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
            except Exception as e:  
                Log.objects.create(
                    source="bot/tasks.py/morning_word_list_task()",
                    status="info",
                    value=f"{str(e)} - user:{str(challenge.user.user_id)}"
                )
            challenge.delete()
