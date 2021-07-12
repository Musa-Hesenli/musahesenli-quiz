from django.contrib import admin
from . import models
# Register your models here.
admin.site.register(models.Category)
admin.site.register(models.Questions)
admin.site.register(models.Answers)
admin.site.register(models.QuestionPackage)
admin.site.register(models.CustomerCreatedQuiz)
admin.site.register(models.Rank)