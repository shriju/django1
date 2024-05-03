from django.contrib import admin
from .models import Answer, Question, Score, UserProfile

# Register your models here.
admin.site.register(Answer)
admin.site.register(Question)
admin.site.register(Score)
admin.site.register(UserProfile)
