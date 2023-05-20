from django.contrib import admin
from dictionary_app.models import Word, Challenge


class ChallengeAdmin(admin.ModelAdmin):
    list_display = ('word', 'user', 'date_send', 'deadline_send', 'created',)
    ordering = ('-created',)

admin.site.register(Challenge, ChallengeAdmin)


class WordAdmin(admin.ModelAdmin):
    list_display = ('word', 'translate', 'user', 'created',)
    ordering = ('-created',)
    search_fields = ('word', 'translate',)

admin.site.register(Word, WordAdmin)
