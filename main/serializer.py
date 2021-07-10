from django.db.models import fields
from django.contrib.auth.models import User
from rest_framework import serializers
from . import models


class Categories(serializers.ModelSerializer):
    class Meta:
        model = models.Category
        fields = '__all__'

class QuestionPackage(serializers.ModelSerializer):
    class Meta:
        model = models.QuestionPackage
        fields = '__all__'        

class Question(serializers.ModelSerializer):
    class Meta:
        model = models.Questions
        fields = '__all__'

class Options(serializers.ModelSerializer):
    class Meta:
        model = models.Answers
        fields = ('question','text')

class Users(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'                  

class CustomerCreatedQuizSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.CustomerCreatedQuiz
        fields = '__all__'        