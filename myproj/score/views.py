# Initialize LanguageTool for grammar checking
import language_tool_python
tool = language_tool_python.LanguageTool("en-US")
from django.http import HttpResponse
from rest_framework import viewsets, generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import spacy
from collections import Counter
import pandas as pd
import nltk
from sklearn.feature_extraction.text import CountVectorizer 
from sklearn.metrics.pairwise import cosine_similarity
from nltk.tokenize import word_tokenize
nltk.download("punkt") 
from score.models import Answer, Question, Score
from score.serializers import AnswerSerializer, QuestionSerializer, RegistrationSerializer, ScoreSerializer
from rest_framework.permissions import IsAuthenticated
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.contrib.auth import login as django_login
from django.contrib.auth import logout as django_logout
from .serializers import LoginSerializer
from .models import Question, Answer, UserProfile
from django.contrib.auth.models import User 
from django.http import JsonResponse
import json


class HelloPythonistaAPIView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        return Response({"message": "Hello Pythonistas!"})
   
class LoginView(APIView):
       
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        
        # Validate the data using the serializer
        if serializer.is_valid():
            # Get the user from the serializer and log them in
            user = serializer.user
            django_login(request, user)
            return Response({"message": "Login successful"}, status=status.HTTP_200_OK)
        
        # If validation fails, return errors
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class LogoutView(APIView):
    def post(self, request):
        django_logout(request)  # Log the user out
        return Response({"message": "Logout successful"}, status=status.HTTP_200_OK)


@csrf_exempt
@require_POST
def get_score(request):
    try:
        # Extract reference_answer and answer from POST data if provided
        if request.body:
            data = json.loads(request.body)
            reference_answer = data.get("reference_answer", "machine learning is a subset of cs")
            answer = data.get("answer", "machine learning is a branch of cs")
        else:
            # Default values if no data is provided
            reference_answer = "machine learning is a subset of cs"
            answer = "machine learning is a branch of cs"

        # Tokenize and create a bag-of-words model
        tokens = nltk.word_tokenize(reference_answer + " " + answer)
        vectorizer = CountVectorizer().fit_transform([reference_answer, answer])

        # Calculate cosine similarity
        cosine_similarities = cosine_similarity(vectorizer)

        # Return the cosine similarity score as JSON
        return JsonResponse({
            "score": cosine_similarities[0, 1]
        })

    except Exception as e:
        # Return error message if any exception occurs
        return JsonResponse({
            "error": str(e)
        }, status=500)
    #return cosine_similarities[0, 1]   # Return the cosine similarity between the two answers
    #provided_answer = "NLP is a branch of AI that deals with interaction between computers and humans using natural language."  # Sample answer
    #similarity_score = get_cosine_similarity(reference_answer, provided_answer) # Calculate the similarity score
    #print("Similarity Score:", similarity_score)
    
class QuestionView(generics.ListAPIView):
    queryset=Question.objects.all()
    serializer_class = QuestionSerializer
    
class AnswerView(generics.ListAPIView):
    queryset=Answer.objects.all()
    serializer_class = AnswerSerializer
    
class QuestionCreateAPIView(generics.CreateAPIView):
    queryset=Question.objects.all()
    serializer_class = QuestionSerializer

class AnswerCreateAPIView(generics.CreateAPIView):
    queryset=Answer.objects.all()
    serializer_class = AnswerSerializer
 

class RegistrationView(APIView):
    def post(self, request):
        serializer = RegistrationSerializer(data=request.data)

        if serializer.is_valid():
            username = serializer.validated_data['username']

            # Check if the username already exists
            if User.objects.filter(username=username).exists():
                return Response(
                    {"message": "Username already taken. Please log in or choose a different username."},
                    status=status.HTTP_400_BAD_REQUEST
                )

            # If the username does not exist, create the user
            serializer.save()  # Create the user with the data in the serializer
            return Response({"message": "Registration successful"}, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
    # API for updating questions
class QuestionUpdateAPIView(generics.UpdateAPIView):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    lookup_field = 'id'  # You can use a different field as needed

# API for updating answers
class AnswerUpdateAPIView(generics.UpdateAPIView):
    queryset = Answer.objects.all()
    serializer_class = AnswerSerializer
    lookup_field = 'id'  # Update based on the answer's ID

# API for deleting questions
class QuestionDeleteAPIView(generics.DestroyAPIView):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    lookup_field = 'id'  # Delete question by its ID

# API for deleting answers
class AnswerDeleteAPIView(generics.DestroyAPIView):
    queryset = Answer.objects.all()
    serializer_class = AnswerSerializer
    lookup_field = 'id'  # Delete answer by its ID