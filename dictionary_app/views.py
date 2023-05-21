from django.shortcuts import render
from django.http.response import HttpResponse, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
from bot.tasks import morning_word_list_task, challenge_task
from dictionary_app.models import Word
import json
import os


@csrf_exempt
def import_words(request):
    data = json.loads(request.body)
    word = data.get("word", None)
    translate = data.get("translate", None)
    token = data.get("token", None)
    if word and translate and token == os.environ.get("TOKEN_IMPORT"):
        Word.objects.create(
            word=word,
            translate=translate
        )
        return HttpResponse("OK")
    else:
        return HttpResponseBadRequest("Error")


def test(r):
    # challenge_task()
    return HttpResponse("OK")
