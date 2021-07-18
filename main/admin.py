from django.contrib import admin
from . import models
# Register your models here.

@admin.register(models.Questions)
class QuestionAdminModel(admin.ModelAdmin):
    list_filter = ('package',)
    list_display = ('package', 'question_name')
    list_display_links = ["package"]
    class Meta:
        model = models.Questions

@admin.register(models.Answers)
class AnswersModelAdmin(admin.ModelAdmin):
    list_filter = ["question"]
    list_display = ["question", "text", "is_answer"]

admin.site.register(models.Category)
admin.site.register(models.QuestionPackage)
admin.site.register(models.CustomerCreatedQuiz)
admin.site.register(models.Rank)