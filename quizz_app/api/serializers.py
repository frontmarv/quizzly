from rest_framework import serializers
from quizz_app.models import Quizz, Question


class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ['id', 'question_title', 'question_options',
                  'answer', 'created_at', 'updated_at']


class QuizzSerializer(serializers.ModelSerializer):
    questions = QuestionSerializer(many=True, read_only=True)

    class Meta:
        model = Quizz
        fields = ['id', 'title', 'description', 'created_at',
                  'updated_at', 'video_url', 'questions']
