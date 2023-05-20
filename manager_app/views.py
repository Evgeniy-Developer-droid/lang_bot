import json
from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.conf import settings
from liqpay.liqpay3 import LiqPay
from manager_app.models import SubNow, TemporalyToken
import os


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
        if response['status'] == 'success':
            token = TemporalyToken.objects.get(key=response['order_id'])
            sub = SubNow.objects.get(pk=int(token.value))
            SubNow.objects.filter(user=sub.user, active=True).update(active=False)
            sub.active = True
            sub.save()
        elif response['status'] == '3ds_verify':
            return redirect(response['redirect_to'])

        return HttpResponse("OK")
    