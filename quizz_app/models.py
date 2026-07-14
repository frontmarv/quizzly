from django.db import models
from django.contrib.auth.models import User


class Quizz(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='quizzes')
    title = models.CharField(max_length=255)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    video_url = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.title


class Question(models.Model):
    quizz = models.ForeignKey(
        Quizz, on_delete=models.CASCADE, related_name='questions')
    question_title = models.CharField(max_length=500)
    question_options = models.JSONField(default=list)
    correct_answer_index = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.question_title
