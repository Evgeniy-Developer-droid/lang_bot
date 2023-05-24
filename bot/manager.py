import django
import os
from django.conf import settings
from django.utils import timezone
from datetime import datetime, timedelta
from bot.payment import pay_link_generate
import logging

logger = logging.getLogger(__name__)

if bool(int(os.environ.get("DEBUG", "1"))):
    try:
        os.environ.setdefault("DJANGO_SETTINGS_MODULE", "server.settings")
        django.setup()
    except:
        pass

from manager_app.models import PromoCode, Subscription, User, History, SubNow, TemporalyToken
from dictionary_app.models import Word

def add_word_to_dict(word, translate, chat_id):
    user = User.objects.get(user_id=str(chat_id))
    Word.objects.create(
        user=user,
        word=word,
        translate=translate,
        published=False
    )

def get_temp_subscription(user):
    instances = SubNow.objects.filter(user=user, active=False).order_by('-created')
    if instances.exists():
        return instances.first()
    return False

def create_payment(sub_id):
    token = TemporalyToken.objects.create(name="payment", value=str(sub_id))
    sub = SubNow.objects.get(pk=sub_id)
    link = pay_link_generate(
        sub.price, 
        description="Сплата підписки",
        token=token.key,
        order_id=token.pk
    )
    return link

def use_promocode(promo_code, user_id):
    user = User.objects.get(user_id=str(user_id))
    promo = PromoCode.objects.filter(code=promo_code)
    if promo.exists():
        promo = promo.first()
        sub_now = get_temp_subscription(user)
        if promo.active and sub_now:
            sub_now.price = sub_now.sub.price - (sub_now.sub.price * promo.discont_value / 100)
            sub_now.promo_code = promo_code
            sub_now.save()
            if promo.for_target == 'single':
                promo.active = False
                promo.save()
            return create_payment(sub_now.pk)
    return False

def set_subscription(chat_id, sub_id):
    user = User.objects.get(user_id=str(chat_id))
    sub = Subscription.objects.get(pk=sub_id)

    end = timezone.now()

    if sub.period == 'day':
        end = end + timedelta(days=sub.period_value)
    elif sub.period == 'week':
        end = end + timedelta(weeks=sub.period_value)
    else:
        end = end + timedelta(days=sub.period_value * 30)

    inst = SubNow.objects.create(
        user=user,
        sub=sub,
        end=end,
        price=sub.price
    )
    return inst.pk


def get_subscriptions():
    instances = Subscription.objects.all()
    result = [
        {
            "id": item.id,
            "name": item.name,
            "price": item.price,
            "period": item.period,
            "period_value": item.period_value
        } for item in instances
    ]
    return result

def get_or_create_user(user):
    try:
        return User.objects.get(user_id=str(user.id))
    except User.DoesNotExist:
        return User.objects.create(
            user_id=str(user.id),
            language_code=user.language_code or "en",
            is_premium=user.is_premium or False,
            first_name=user.first_name or "",
            last_name=user.last_name or "",
            username=user.username or "",
        )

def get_now_subscription(user):
    instances = SubNow.objects.filter(user=user, active=True).order_by('-created')
    if instances.exists():
        instance = instances.first()
        return {"name": instance.sub.name, "start": instance.created, "end": instance.end}
    return False