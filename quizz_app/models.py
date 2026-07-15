from django.db import models
from django.conf import settings


class Quizz(models.Model):
    """Represents a quiz created from a video.

    Attributes:
        user: Foreign key to the user who created the quiz
        title: Title of the quiz
        description: Description of the quiz content
        created_at: Timestamp when the quiz was created
        updated_at: Timestamp when the quiz was last updated
        video_url: URL of the source video
    """
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='quizzes')
    title = models.CharField(max_length=255)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    video_url = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.title


class Question(models.Model):
    """Represents a single question within a quiz.

    Attributes:
        quizz: Foreign key to the parent quiz
        question_title: The question text
        question_options: List of answer options in JSON format
        correct_answer_index: Index of the correct answer in question_options
        created_at: Timestamp when the question was created
        updated_at: Timestamp when the question was last updated
    """
    quizz = models.ForeignKey(
        Quizz, on_delete=models.CASCADE, related_name='questions')
    question_title = models.CharField(max_length=500)
    question_options = models.JSONField(default=list)
    correct_answer_index = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.question_title
