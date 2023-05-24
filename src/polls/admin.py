from django.contrib import admin

from .models import Answer, Poll, Question, Response

models = [Poll, Question, Response, Answer]

admin.site.register(models)
