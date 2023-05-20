import django
import os
from django.conf import settings

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "server.settings")
django.setup()

from bot.bot import main

if __name__ == "__main__":
    main()