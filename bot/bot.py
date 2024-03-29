
from bot.manager import (
    add_word_to_dict,
    create_payment,
    get_or_create_user,
    get_now_subscription,
    use_promocode,
    get_subscriptions,
    set_subscription
)
import redis
import os
import telebot
from django.http import HttpResponse
from django.core.exceptions import PermissionDenied
from django.views.decorators.csrf import csrf_exempt
from manager_tools import setKey, deleteKey, getKey


bot = telebot.TeleBot(os.environ.get("BOT_KEY"))
# r = redis.Redis(host="redis", port=6379, decode_responses=True)


@csrf_exempt
def bot_webhook(request):
    if request.META['CONTENT_TYPE'] == 'application/json':
        json_data = request.body.decode('utf-8')
        update = telebot.types.Update.de_json(json_data)
        bot.process_new_updates([update])
        return HttpResponse("")
    else:
        raise PermissionDenied

# @bot.message_handler(commands=['add_word'])
# def add_word_hand(message):
#     user = message.from_user
#     user_instance = get_or_create_user(user)
#     subscription = get_now_subscription(user_instance)
#     markup = telebot.types.InlineKeyboardMarkup()
#     markup.row_width = 1
#     if subscription:
#         msg = bot.send_message(message.chat.id, f"""Укажіть нове слово або словосполучення і його переклад у форматі Англійська/Українська. \nНаприклад Dog/Пес або I like cars/Мені подобаються автомобілі""")
#         bot.register_next_step_handler(msg, input_add_word)
#     else:
#         markup.add(
#             telebot.types.InlineKeyboardButton("\U0001F4DC Вибрати підписку", callback_data="sb_new")
#         )
#         bot.send_message(message.chat.id, f"У вас не має жодної активної підписки! \U0001F614", reply_markup=markup)

# def input_add_word(message):
#     data = message.text.split("/")
#     if len(data) != 2:
#         msg = bot.send_message(message.chat.id, f"\U0000274C Помилка. Не правильний формат!")
#         bot.register_next_step_handler(msg, input_add_word)
#     else:
#         # add to db
#         add_word_to_dict(word=data[0], translate=data[1], chat_id=message.chat.id)
#         bot.send_message(message.chat.id, f"Вітаю! \U0001F389 Ви успішно додали новий запис до словника.")

@bot.message_handler(commands=['subscription'])
def subscription_hand(message):
    user = message.from_user
    user_instance = get_or_create_user(user)
    subscription = get_now_subscription(user_instance)
    markup = telebot.types.InlineKeyboardMarkup()
    if subscription:
        markup.row_width = 1
        markup.add(
            telebot.types.InlineKeyboardButton("Змінити підписку", callback_data="sb_new")
        )
        bot.send_message(message.chat.id, f"""{subscription['name']} \nСтарт підписки - {subscription['start'].strftime("%d/%m/%Y")} \nКінець підписки - {subscription['end'].strftime("%d/%m/%Y")} """, reply_markup=markup)
    else:
        markup.row_width = 1
        markup.add(
            telebot.types.InlineKeyboardButton("\U0001F4DC Вибрати підписку", callback_data="sb_new")
        )
        bot.send_message(message.chat.id, f"У вас не має жодної активної підписки!\U0001F614", reply_markup=markup)

@bot.message_handler(commands=['help'])
def help_handler(message):
    user = message.from_user
    user_instance = get_or_create_user(user)
    msg = "Після обрання рівня підписки, кожного ранку я бути присилати тобі список слів. Впродовж дня я буду перевіряти тебе згідно цих слів. Бажаю тобі успіху!"
    bot.send_message(message.chat.id, msg)

@bot.message_handler(commands=['info'])
def info_hand(message):
    msg = f"Якщо у вас виникли проблеми, додаткові запитання можете написати мені.\n"
    msg += f"Linkedin: https://www.linkedin.com/in/evgeny-grinchak/ \n"
    msg += f"Facebook: https://www.facebook.com/profile.php?id=100068917465287 \n"
    msg += f"Instagram: https://www.instagram.com/evgen_grnk/ \n"
    bot.send_message(message.chat.id, msg)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    user = message.from_user
    user_instance = get_or_create_user(user)
    bot.set_my_commands(
        commands=[
            telebot.types.BotCommand('/subscription', 'Підписки'),
            telebot.types.BotCommand('/info', 'Контакти розробника'),
            # telebot.types.BotCommand('/add_word', 'Додати в словник'),
            telebot.types.BotCommand('/help', 'Допомога'),
        ],
        scope=telebot.types.BotCommandScopeChat(message.chat.id)
    )
    msg = f"Привіт {user.first_name or ''} \U0001F600!\n"
    msg += "Я бот який допоможе тобі з вивченням англійської мови \U0001F1EC.\nПісля обрання рівня підписки, кожного ранку я бути присилати тобі список слів. Впродовж дня я буду перевіряти тебе згідно цих слів. Бажаю тобі успіху!"
    bot.send_message(message.chat.id, msg)

@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    markup = telebot.types.InlineKeyboardMarkup()
    markup.row_width = 1
    if call.data == "sb_new":
        msg_answer = f"Виберіть рівень підписки.\n"
        for sub_instance in get_subscriptions():
            markup.add(
                telebot.types.InlineKeyboardButton(
                    f"""\U00002B50 {sub_instance['name']} {sub_instance['price']} грн""",
                    callback_data=f"sb_select|id:{sub_instance['id']}|{sub_instance['desc']}"
                )
            )
            msg_answer += "\n"
            msg_answer += f"{sub_instance['name']}\n"
            msg_answer += f"Ціна: {sub_instance['price']} грн.\n"
            msg_answer += f"Період: 30 днів.\n"
            msg_answer += f"Слів: {sub_instance['max_words']}.\n"
            msg_answer += f"Словосполучень: {sub_instance['max_phrases']}.\n"
        bot.send_message(call.message.chat.id, msg_answer, reply_markup=markup)
    
    if call.data.startswith("sb_select"):
        sub_selected_id = int(call.data.split("|")[1].split(":")[1])
        desc = call.data.split("|")[2]
        chat_id = call.message.chat.id
        if "free" in desc:
            set_subscription(chat_id, sub_selected_id)
            bot.send_message(call.message.chat.id, f"Дякую, що обрали безкоштовну підписку! Кожного ранку я бути присилати тобі список слів. Впродовж дня я буду перевіряти тебе згідно цих слів. Бажаю тобі успіху!")
            return None
        markup.add(
            telebot.types.InlineKeyboardButton("\U0001F4B3 Банківська картка", callback_data=f"sb_payment|id:{sub_selected_id}|liqpay"),
        )
        bot.send_message(call.message.chat.id, f"Виберіть спосіб оплати.", reply_markup=markup)

    if call.data.startswith("sb_payment"):
        sub_selected_id = int(call.data.split("|")[1].split(":")[1])
        payment_method = call.data.split("|")[2]
        chat_id = call.message.chat.id

        # set subscription without pay
        sub_now_id = set_subscription(chat_id, sub_selected_id)
        markup.add(
            telebot.types.InlineKeyboardButton("\U000026AA Використати Промо код", callback_data=f"sb_promocode|sub_now_id:{sub_now_id}|{payment_method}"),
        )
        link = create_payment(sub_now_id)
        bot.send_message(call.message.chat.id, f"Перейдіть за посиланням і сплатіть або використайте промокод. {link}", reply_markup=markup)
    
    if call.data.startswith("sb_promocode"):
        msg = bot.send_message(call.message.chat.id, f"Укажіть промокод, або напишіть # щоб відмінити.")
        bot.register_next_step_handler(msg, enter_promo_code)
    
    if call.data.startswith("answer"):
        right_answer = call.data.split('|')[2]
        setKey(str(call.message.chat.id)+'_answer', right_answer)
        msg = bot.send_message(call.message.chat.id, f"Напишіть вашу відповідь:")
        bot.register_next_step_handler(msg, challenge_answer)

def challenge_answer(message):
    bot.send_message(message.chat.id, f"Ваша відповідь - {message.text}\nВірна відповідь - {getKey(str(message.chat.id)+'_answer')}")
    deleteKey(str(message.chat.id)+'_answer')

def enter_promo_code(message):
    if message.text == "#":
        return None
    promo = use_promocode(message.text, message.chat.id)
    if not promo:
        msg = bot.send_message(message.chat.id, f"Промокод не знайдено, спробуйте знову, або напишіть # щоб відмінити.")
        bot.register_next_step_handler(msg, enter_promo_code)
    else:
        bot.send_message(message.chat.id, f"Перейдіть за посиланням і сплатіть. {promo}")


def main():
    bot.infinity_polling()
