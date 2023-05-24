from django.urls import path
from dictionary_app.views import *

urlpatterns = [
    path('test', test),
    path('import', import_words),
    path('logs', get_logs),
]
