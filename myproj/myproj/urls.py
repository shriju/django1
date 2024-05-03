from django.contrib import admin
from django.urls import path, include
from score.views import LoginView, LogoutView
from rest_framework.routers import DefaultRouter
#from .views import login_view
from score.views import (
    #AnswerViewSet,
    #QuestionAPIView,
    #ScoreViewSet,
    get_score,
    QuestionView,
    AnswerView,
    QuestionCreateAPIView,
    AnswerCreateAPIView,
    RegistrationView,
    QuestionUpdateAPIView,  
    AnswerUpdateAPIView,  
    QuestionDeleteAPIView,  
    AnswerDeleteAPIView
    
)

# Create a router to handle ViewSets
router = DefaultRouter()
# router.register(r'answers', AnswerViewSet)
# router.register(r'scores', ScoreViewSet)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/score", get_score, name="score_api"),
    #path("getquestion/", QuestionAPIView.as_view(), name="get_question"),
    #path("api/", include(router.urls)),
    
    
    path('login/', LoginView.as_view(), name='login'),
    #path('login/', login_view, name='login'),  # Use the csrf-exempted view
    path('logout', LogoutView.as_view(), name='logout'),
    path('question', QuestionView.as_view(), name='question'),
    path('answer', AnswerView.as_view(), name='answer'),
    path('createquestion', QuestionCreateAPIView.as_view(), name='createquestion'),
    path('createanswer', AnswerCreateAPIView.as_view(), name='createanswer'),
    path('register/', RegistrationView.as_view(), name='register'),
    
    path('updatequestion/<int:id>/', QuestionUpdateAPIView.as_view(), name='updatequestion'),
    path('updateanswer/<int:id>/', AnswerUpdateAPIView.as_view(), name='updateanswer'),
    path('deletequestion/<int:id>/', QuestionDeleteAPIView.as_view(), name='deletequestion'),
    path('deleteanswer/<int:id>/', AnswerDeleteAPIView.as_view(), name='deleteanswer'),
]





