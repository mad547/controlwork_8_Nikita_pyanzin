from django.contrib import admin

import threads
from threads.models import Thread, Answer


# Register your models here.
class AnswerInline(admin.TabularInline):
    model = Answer
    extra = 1


class ThreadAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'created_at', 'answers_count']
    search_fields = ['title', 'content']
    inlines = [AnswerInline]


class AnswerAdmin(admin.ModelAdmin):
    list_display = ['author','thread', 'created_at']
    search_fields = ['content']


admin.site.register(Thread, ThreadAdmin)
admin.site.register(Answer, AnswerAdmin)