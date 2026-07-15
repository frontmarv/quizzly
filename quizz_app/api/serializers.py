from urllib.parse import urlparse, parse_qs

from rest_framework import serializers

from quizz_app.models import Quizz, Question


class QuestionSerializer(serializers.ModelSerializer):
    """Serialize question data with the correct answer included.

    Extends ModelSerializer to include the correct answer as a read-only
    field derived from the question_options list.
    """
    answer = serializers.SerializerMethodField()

    class Meta:
        model = Question
        fields = ['id', 'question_title', 'question_options',
                  'answer', 'created_at', 'updated_at']

    def get_answer(self, obj):
        return obj.question_options[obj.correct_answer_index]


class QuizzSerializer(serializers.ModelSerializer):
    """Serialize quiz data with nested questions.

    Provides a complete representation of a quiz including all related
    questions and metadata.
    """
    questions = QuestionSerializer(many=True, read_only=True)

    class Meta:
        model = Quizz
        fields = ['id', 'title', 'description', 'created_at',
                  'updated_at', 'video_url', 'questions']
        read_only_fields = ['id', 'created_at',
                            'updated_at', 'video_url', 'questions']


class QuizRequestSerializer(serializers.Serializer):
    """Serialize quiz creation request with YouTube URL validation.

    Validates YouTube URLs in both formats (youtu.be and youtube.com)
    and normalizes them to the standard format.
    """
    url = serializers.URLField(required=True)

    def validate_url(self, value):
        """Validate and normalize YouTube URL.

        Accepts URLs in both youtu.be and youtube.com formats and
        converts them to the standard youtube.com/watch?v=ID format.

        Args:
            value: URL to validate

        Returns:
            str: Normalized YouTube URL
        """
        parsed = urlparse(value)
        video_id = None

        # Short link format (youtu.be/ID)
        if parsed.hostname == 'youtu.be':
            video_id = parsed.path.lstrip('/')

        # Standard link format (youtube.com/watch?v=ID)
        elif parsed.hostname in ['www.youtube.com', 'youtube.com'] and parsed.path == '/watch':
            video_id = parse_qs(parsed.query).get('v', [None])[0]

        if not video_id:
            raise serializers.ValidationError(
                "Not a valid URL. Please provide a valid YouTube video URL.")
        return f"https://www.youtube.com/watch?v={video_id}"
