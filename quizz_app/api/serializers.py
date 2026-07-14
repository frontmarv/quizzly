from rest_framework import serializers
from quizz_app.models import Quizz, Question
from urllib.parse import urlparse, parse_qs


class QuestionSerializer(serializers.ModelSerializer):
    answer = serializers.SerializerMethodField()

    class Meta:
        model = Question
        fields = ['id', 'question_title', 'question_options',
                  'answer', 'created_at', 'updated_at']

    def get_answer(self, obj):
        return obj.question_options[obj.correct_answer_index]


class QuizzSerializer(serializers.ModelSerializer):
    questions = QuestionSerializer(many=True, read_only=True)

    class Meta:
        model = Quizz
        fields = ['id', 'title', 'description', 'created_at',
                  'updated_at', 'video_url', 'questions']
        read_only_fields = ['id', 'created_at',
                            'updated_at', 'video_url', 'questions']


class QuizRequestSerializer(serializers.Serializer):
    url = serializers.URLField(required=True)

    def validate_url(self, value):
        parsed = urlparse(value)
        video_id = None

        # Geteilter Link (youtu.be/ID)
        if parsed.hostname == 'youtu.be':
            video_id = parsed.path.lstrip('/')

        # Adresszeilen-Link (youtube.com/watch?v=ID)
        elif parsed.hostname in ['www.youtube.com', 'youtube.com'] and parsed.path == '/watch':
            video_id = parse_qs(parsed.query).get('v', [None])[0]

        if not video_id:
            raise serializers.ValidationError(
                "Not a valid URL. Please provide a valid YouTube video URL.")
        return f"https://www.youtube.com/watch?v={video_id}"
