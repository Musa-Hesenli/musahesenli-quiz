from django.http import HttpResponse
from django.http import response
from django.http.response import Http404
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework import status
from .serializer import Categories, QuestionPackage, Options, Question, Users, CustomerCreatedQuizSerializer
from rest_framework import permissions, authentication
from . import models
from django.contrib.auth.models import User
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

def home(request):
    return HttpResponse("Hello world")

class CategoryList(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    def get(self, request, format = None):
        category_list = models.Category.objects.all().order_by("name")
        serializer = Categories(category_list, many = True)
        return Response(serializer.data)

    def post(self, request, format = None):
        serializer = Categories(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)    



class PackagesList(APIView):
    def get(self, request, format = None):
        packages = models.QuestionPackage.objects.filter(show_in_page = True)
        serializer = QuestionPackage(packages, many = True)
        context = dict()
        items = []
        for i in serializer.data:
            field  = {}
            response = dict(i)
            creator_id = dict(i)["creator"]
            field["id"] = response["id"]
            field["name"] = response["name"]
            field["description"] = response["description"]
            field["played"] = response["played"]
            field["image"] = response["image"]
            # Get category info according to category id begin

            category_id = response["category"]
            user = models.Category.objects.get(id = category_id)
            serializer = Categories(user)
            field["category"] = serializer.data

            # Get category info according to category id end

            #Get user info according to the creator id begin

            user_info = User.objects.get(id = creator_id)
            serializer = Users(user_info)
            field["creator"] = serializer.data

            #Get user info according to the creator id end

            items.append(field)
        context["message"] = "ok"
        context["packages"] = items
        return Response(context)

    def post(self, request, format = None):
        serializer = QuestionPackage(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status = status.HTTP_201_CREATED)
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)    


class PackageDetails(APIView):
    options = []
    def get_object(self, pk):
        try:
            return models.QuestionPackage.objects.get(pk = pk)
        except models.QuestionPackage.DoesNotExist:
            raise Http404

    def get_questions(self, pk):
        return models.Questions.objects.filter(package = str(pk))

    def json_to_queryset(self, queryset):
        data = []
        for i in queryset:
            pair = {}
            pair["id"] = i.id
            pair["package_id"] = i.package_id
            pair["question"] = i.question_name
            options = self.get_options(i.id)
            options = self.convert_options_to_json(options)
            pair["options"] = options
            data.append(pair)
        return data    

    def convert_options_to_json(self, options):
        json_data = []
        for item in options:
            field = {}
            field["question"] = item.question.id
            field["title"] = item.text
            field["is_answer"] = item.is_answer
            json_data.append(field)
        return json_data


    def get_options(self, pk):
        query_set = models.Answers.objects.filter(question = pk)
        return query_set

    def get(self, request, pk, format = None):
        package_info = self.get_object(pk)
        serializer = QuestionPackage(package_info)
        package_id = serializer.data["id"]
        context = {}
        context["packageInfo"] = serializer.data
        questions = self.get_questions(package_id)
        context["questions"] = self.json_to_queryset(questions)
        return Response(context)


    def put(self, request, pk):
        snippet = self.get_object(pk)
        serializer = QuestionPackage(snippet, data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)    

     

class UsersList(APIView):
    def get(self, request):
        user_list = User.objects.all()
        serializer = Users(user_list, many = True)
        return Response(serializer.data)

    def post(self, request):
        serializer = Users(data = request.data)
        if serializer.is_valid():
            is_email_exists = User.objects.filter(email = request.data["email"]).exists()
            if is_email_exists:
                return Response([{"detail" : "This username is already taken"}], status = status.HTTP_400_BAD_REQUEST)
            instance = serializer.save()
            instance.set_password(request.data["password"])
            instance.save()
            return Response(serializer.data, status = status.HTTP_201_CREATED)
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)    

class UserInfo(APIView):
    def get_object(self, pk):
        try:
            return User.objects.get(pk = pk)
        except User.DoesNotExist:
            raise Http404    

    def get(self, request, pk, format = None):
        user_info = self.get_object(pk)
        serializer = Users(user_info)
        return Response(serializer.data)

    def put(self, request, pk, format = None):
        user_info = self.get_object(pk)
        serializer = Users(user_info, request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format = None):
        user_info = self.get_object(pk)
        user_info.delete()
        return Response(status = status.HTTP_204_NO_CONTENT)          


class Posts(APIView):
    permission_classes = (JSONWebTokenAuthentication,)

class CustomerCreatedQuizList(APIView):
    def get(self, request):
        items = models.CustomerCreatedQuiz.objects.all()
        serializer = CustomerCreatedQuizSerializer(items, many = True)
        return Response(serializer.data)
    
    def post(self, request):
        serializer = CustomerCreatedQuizSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status = status.HTTP_201_CREATED)
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)    