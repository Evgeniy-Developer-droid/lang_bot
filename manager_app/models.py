import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser
from manager_app.fields import IntegerRangeField


class TemporalyToken(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    key = models.UUIDField(default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255, null=True, blank=True, default="")
    value = models.CharField(max_length=255, null=True, blank=True, default="")

    def __str__(self) -> str:
        return self.key


class PromoCode(models.Model):
    FOR_TARGET = (
        ('single', 'Single user',),
        ('multi', 'Multi user',),
    )
    created = models.DateTimeField(auto_now_add=True)
    key = models.UUIDField(default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    code = models.CharField(max_length=255, unique=True)
    for_target = models.CharField(max_length=10, choices=FOR_TARGET, default='single')
    discont_value = IntegerRangeField(min_value=1, max_value=100, help_text="Parsantage, %")
    active = models.BooleanField(default=True)

    def __str__(self) -> str:
        return self.name


class Subscription(models.Model):
    PERIOD = (
        ('month', 'Month',),
    )
    created = models.DateTimeField(auto_now_add=True)
    key = models.UUIDField(default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    price = models.FloatField(default=0.0)
    period = models.CharField(max_length=10, choices=PERIOD, default="month")
    period_value = models.IntegerField(default=1)
    max_words = models.IntegerField(default=5)
    max_phrases = models.IntegerField(default=5)
    description = models.TextField(default="", blank=True, null=True)

    def __str__(self) -> str:
        return self.name


class User(AbstractUser):
    key = models.UUIDField(default=uuid.uuid4, editable=False)
    user_id = models.CharField(max_length=255, unique=True, default=uuid.uuid4)
    language_code = models.CharField(max_length=255, default="en")
    is_premium = models.BooleanField(default=False)

    def __str__(self) -> str:
        return self.user_id


class SubNow(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="subsriptions")
    sub = models.ForeignKey(Subscription, on_delete=models.CASCADE, related_name="sub_history")
    end = models.DateTimeField()
    promo_code = models.CharField(max_length=255, default="", null=True, blank=True)
    price = models.FloatField(default=0.0)
    active = models.BooleanField(default=False)


class History(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="history")
    name = models.CharField(max_length=255, default="", null=True, blank=True)
    target = models.CharField(max_length=255, default="", null=True, blank=True)
    value = models.CharField(max_length=255, default="", null=True, blank=True)
    meta = models.TextField(default="{}", null=True, blank=True)


class Log(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=255, default="", null=True, blank=True)
    source = models.CharField(max_length=255, default="", null=True, blank=True)
    value = models.TextField(default="", null=True, blank=True)


class Transaction(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    amount = models.FloatField(default=0.0)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name="transactions")
    currency = models.CharField(max_length=50, null=True, blank=True, default="")
    paytype = models.CharField(max_length=50, null=True, blank=True, default="")
    status = models.CharField(max_length=50, null=True, blank=True, default="")
    order_id = models.CharField(max_length=255, null=True, blank=True, default="")
    liqpay_order_id = models.CharField(max_length=255, null=True, blank=True, default="")
    payment_id = models.CharField(max_length=255, null=True, blank=True, default="")
    ip = models.CharField(max_length=50, null=True, blank=True, default="")
    description = models.TextField(null=True, blank=True, default="")

    def __str__(self) -> str:
        return self.order_id