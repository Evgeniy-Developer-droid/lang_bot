from django.contrib import admin
from dictionary_app.models import Word, Challenge, Phrase


class PhraseAdmin(admin.ModelAdmin):
    list_display = ('phrase', 'translate', 'user', 'level', 'published', 'created',)
    ordering = ('-created',)

admin.site.register(Phrase, PhraseAdmin)


class ChallengeAdmin(admin.ModelAdmin):
    list_display = ('word', 'phrase', 'user', 'date_send', 'deadline_send', 'created',)
    ordering = ('-created',)

admin.site.register(Challenge, ChallengeAdmin)


class WordAdmin(admin.ModelAdmin):
    list_display = ('word', 'translate', 'user', 'published', 'created',)
    ordering = ('-created',)
    search_fields = ('word', 'translate',)

admin.site.register(Word, WordAdmin)
