from django.shortcuts import render
from django.http.response import HttpResponse, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
from bot.tasks import morning_word_list_task, challenge_task
from dictionary_app.models import Word
import json
import os
# import logging

# logger = logging.getLogger(__name__)


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
    # logger.warning("test")
    # logger.critical("critical")
    # logger.error("error")
    # logger.info("info")
    return HttpResponse("OK")

def get_logs(request):
    data = []
    # with open('logs.log', 'r') as f:
    #     for line in f.readlines():
    #         if line.startswith("WARNING"):
    #             data.append({'type': "warning", "data": line})
    #         elif line.startswith("CRITICAL"):
    #             data.append({'type': "critical", "data": line})
    #         elif line.startswith("ERROR"):
    #             data.append({'type': "error", "data": line})
    #         else:
    #             data.append({'type': "info", "data": line})
    return render(request, 'logs.html', {'data': data})