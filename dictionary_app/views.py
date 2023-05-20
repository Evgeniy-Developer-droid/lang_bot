from django.shortcuts import render
from django.http.response import HttpResponse

from bot.tasks import morning_word_list_task, challenge_task

def test(r):
    challenge_task()
    return HttpResponse("OK")
