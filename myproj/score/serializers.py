from rest_framework import serializers
from score.models import Question, Answer, Score, UserProfile
from django.contrib.auth import authenticate
from django.contrib.auth.models import User

class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = '__all__'  # Specific fields to include

class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = '__all__'  # Fields to serialize

class ScoreSerializer(serializers.ModelSerializer):
    question = QuestionSerializer(read_only=True)  # Read-only to prevent modification through Score
    answer = AnswerSerializer(read_only=True)  # Read-only Answer relationship

    class Meta:
        model = Score
        fields = ('id', 'score_value', 'question', 'answer')  # Define specific fields
        

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150, required=True)
    password = serializers.CharField(write_only=True, required=True)

    def validate(self, data):
        username = data.get('username')
        password = data.get('password')

        # Attempt to authenticate the user with the provided credentials
        user = authenticate(username=username, password=password)

        if user is None:
            raise serializers.ValidationError("Invalid username or password.")

        if not user.is_active:
            raise serializers.ValidationError("This account is inactive.")

        # Store the authenticated user in the serializer's instance for later use
        self.user = user
        
        return data
    
class RegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})
    password_confirm = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})
    email = serializers.EmailField(required=True)  # Retain the email field

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'password_confirm']

    def validate(self, data):
        if data['password'] != data['password_confirm']:
            raise serializers.ValidationError("Passwords must match.")
        
        return data

    def create(self, validated_data):
        validated_data.pop('password_confirm')  # Ensure password_confirm is removed
        return User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )