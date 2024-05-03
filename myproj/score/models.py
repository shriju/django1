from django.contrib.auth.models import User
from django.db import models

class Question(models.Model):
    student_name = models.CharField(max_length=50)
    question_id = models.CharField(max_length=10)
    question_text = models.TextField()
    question_category = models.CharField(max_length=30, null=True, blank=True)

class Answer(models.Model):
    student_name = models.CharField(max_length=50)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    answer_text = models.CharField(max_length=200, default="No answer provided")
    answer_category = models.CharField(max_length=30, null=True, blank=True)
    from django.db import models

class Score(models.Model):
    student_name = models.CharField(max_length=50)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE)
    score_value = models.FloatField(default=0)

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    bio = models.TextField(blank=True)  # Example custom field
    website = models.URLField(blank=True)  # Example custom field
    birth_date = models.DateField(null=True, blank=True)  # Example custom field
    email=models.EmailField(max_length=254, blank=True)
    
    def __str__(self):
        return self.user.username
    
