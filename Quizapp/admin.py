from django.contrib import admin
from . models import (Class,Quiz,Subject,Topic,Mcqs,CorrectAnswer,Questions,Theory,AnswerChoice,School)
# Register your models here.

admin.site.register(Class)
admin.site.register(Subject)
admin.site.register(Topic)
admin.site.register(Quiz)
admin.site.register(Questions)
admin.site.register(Mcqs)
admin.site.register(Theory)
admin.site.register(AnswerChoice)
admin.site.register(CorrectAnswer)
admin.site.register(School)







