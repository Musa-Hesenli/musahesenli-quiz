from collections import UserList
from django.urls import path
from rest_framework_jwt.views import obtain_jwt_token, refresh_jwt_token
from . import views
urlpatterns = [
    path("home", views.home, name = "app_home"),
    path("quiz-categories", views.CategoryList.as_view()),
    path("users", views.UsersList.as_view()),
    path("users/<int:pk>/", views.UserInfo.as_view()),
    path("packages", views.PackagesList.as_view()),
    path("created-quizess", views.CustomerCreatedQuizList.as_view()),
    path("packages/<int:pk>", views.PackageDetails.as_view()),
    path("ranks", views.RankList.as_view()),
    path("ranks/<int:pk>", views.RankDetails.as_view()),
    path(r'auth/obtain_token/', obtain_jwt_token),
    path(r'auth/refresh_token/', refresh_jwt_token)
    
]
