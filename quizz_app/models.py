from django.db import models


class Quizz(models.Model):
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
    # Speichert die Optionen als JSON Array
    question_options = models.JSONField(default=list)
    answer = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.question_title
