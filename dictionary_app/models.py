from django.db import models
from manager_app.models import User


class Word(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name="words")
    word = models.CharField(max_length=500)
    translate = models.CharField(max_length=500)

    def __str__(self) -> str:
        return f"{self.word} - {self.translate}"


class Challenge(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_chellenges")
    word = models.ForeignKey(Word, on_delete=models.CASCADE, related_name="word_chellenges")
    date_send = models.DateTimeField()
    deadline_send = models.DateTimeField()

    def __str__(self) -> str:
        return f"{self.user} - {self.date_send}"