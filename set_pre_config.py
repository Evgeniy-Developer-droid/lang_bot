import requests
import sys, os

sys.stdout.flush()


res = requests.get(f"https://api.telegram.org/bot{os.environ.get('BOT_KEY')}/setWebhook")
print("Delete all webhooks", res.content, flush=True)
res = requests.get(f"https://api.telegram.org/bot{os.environ.get('BOT_KEY')}/setWebhook?url={os.environ.get('SERVER_URL')}/manager/webhook/{os.environ.get('BOT_KEY')}/")

print(f"Set webhook {os.environ.get('SERVER_URL')}/manager/webhook/{os.environ.get('BOT_KEY')}/", res.content, flush=True)