import json
from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.conf import settings
from liqpay.liqpay3 import LiqPay
from manager_app.models import SubNow, TemporalyToken, Transaction
import os
import telebot


def create_transaction(response, sub):
    Transaction.objects.create(
        user=sub.user,
        amount=response.get('amount'),
        currency=response.get('currency'),
        paytype=response.get('paytype'),
        status=response.get('status'),
        order_id=response.get('order_id'),
        liqpay_order_id=response.get('liqpay_order_id'),
        payment_id=response.get('payment_id'),
        ip=response.get('ip'),
        description=response.get('description')
    )


@method_decorator(csrf_exempt, name='dispatch')
class PayCallbackView(View):
    def post(self, request, *args, **kwargs):
        liqpay = LiqPay(os.environ.get("LIQPAY_PUBLIC", ""), os.environ.get("LIQPAY_SECRET", ""))
        data = request.POST.get('data', None)
        signature = request.POST.get('signature', None)
        sign = liqpay.str_to_sign(os.environ.get("LIQPAY_SECRET", "") + data + os.environ.get("LIQPAY_SECRET", ""))
        if sign == signature:
            print('callback is valid')
        response = liqpay.decode_data_from_str(data)
        print('callback data', response)

        if response['status'] == '3ds_verify':
            return redirect(response['redirect_to'])
        
        token = TemporalyToken.objects.get(key=response['order_id'])
        sub = SubNow.objects.get(pk=int(token.value))
        if response['status'] == 'success':
            SubNow.objects.filter(user=sub.user, active=True).update(active=False)
            sub.active = True
            sub.save()
            bot = telebot.TeleBot(os.environ.get("BOT_KEY"))
            message = f"Успішна сплата підписки.\n Order id - {response['order_id']}"
            bot.send_message(str(sub.user.user_id), message)

        create_transaction(response, sub)

        return HttpResponse("OK")
    