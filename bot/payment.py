from liqpay.liqpay3 import LiqPay
import os

def pay_link_generate(amount, description, token, order_id):
    liqpay = LiqPay(os.environ.get("LIQPAY_PUBLIC", ""), os.environ.get("LIQPAY_SECRET", ""))
    params = {
        'action': 'pay',
        'currency': 'UAH',
        'order_id': token,
        'version': '3',
        'amount': amount,
        'description': description,
        'sandbox': int(os.environ.get("LIQPAY_SANDBOX", 0)), # sandbox mode, set to 1 to enable it
        'server_url':  f'{os.environ.get("SERVER_URL", "http://localhost:8000")}/manager/liqpay-callback'
    }
    signature = liqpay.cnb_signature(params)
    data = liqpay.cnb_data(params)
    link = f"https://www.liqpay.ua/api/3/checkout?data={data}&signature={signature}"
    return link