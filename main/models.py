from django.db import models
from django.contrib.contenttypes.fields import GenericRelation
# Create your models here.
class Category(models.Model):
    name = models.CharField(verbose_name = "Category name", max_length = 30)
    image = models.ImageField(null = True)
    def __str__(self):
        return self.name




class QuestionPackage(models.Model):
    name = models.CharField(max_length=100, verbose_name="Question package name")
    description = models.CharField(max_length = 400, verbose_name = "Description", null = True)
    category = models.ForeignKey(Category, on_delete = models.CASCADE)
    creator = models.ForeignKey("auth.User", on_delete = models.CASCADE)
    show_in_page = models.BooleanField(default = False)
    played = models.IntegerField(default = 0)
    image = models.ImageField(null = True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["name"]  

class Questions(models.Model):
    package = models.ForeignKey(QuestionPackage, on_delete = models.CASCADE)
    question_name = models.CharField(verbose_name = "Question name", max_length=250)
    def __str__(self):
        return self.question_name

class Answers(models.Model):
    question = models.ForeignKey(Questions, on_delete = models.CASCADE)
    text = models.CharField(verbose_name = "Text", max_length = 100)
    is_answer = models.BooleanField(verbose_name = "Check if that is a answer of the question")

    def __str__(self) :
        return self.question.question_name + ": Answer: " + self.text


class CustomerCreatedQuiz(models.Model):
    text = models.TextField()
    is_looked_at = models.BooleanField()


class Rank(models.Model):
    user = models.OneToOneField("auth.User", on_delete = models.CASCADE)
    total_point = models.DecimalField(max_digits = 1000000000, decimal_places = 2)

    def __str__(self):
        return self.user.username + ": " + str(self.total_point)