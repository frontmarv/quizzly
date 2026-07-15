import json
import os

from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from quizz_app.api.serializers import QuizzSerializer, QuestionSerializer, QuizRequestSerializer
from quizz_app.models import Quizz, Question
from ..services.services import download_youtube_audio, transcribe_audio, generate_quiz_from_text


class QuizzDetailView(APIView):
    """Handle individual quiz CRUD operations.

    Provides endpoints to retrieve, update, and delete a specific quiz.
    Ensures that only the quiz owner can perform these operations.
    """
    permission_classes = [IsAuthenticated]

    def get_user_quizz(self, pk, request):
        """Get quiz and verify it belongs to the user.

        Args:
            pk: Primary key of the quiz
            request: HTTP request object

        Returns:
            tuple: (quizz object, error_response) or (None, error_response)
                Returns the quiz if found and belongs to user, otherwise None
                with appropriate error response
        """
        try:
            quizz = Quizz.objects.get(pk=pk)
        except Quizz.DoesNotExist:
            return None, Response({"detail": "Quiz not found"}, status=status.HTTP_404_NOT_FOUND)

        if quizz.user != request.user:
            return None, Response({"detail": "Quiz does not belong to the user"}, status=status.HTTP_403_FORBIDDEN)

        return quizz, None

    def get(self, request, pk):
        quizz, error_response = self.get_user_quizz(pk, request)
        if error_response:
            return error_response

        serializer = QuizzSerializer(quizz)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def patch(self, request, pk):
        quizz, error_response = self.get_user_quizz(pk, request)
        if error_response:
            return error_response

        serializer = QuizzSerializer(
            quizz, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        quizz, error_response = self.get_user_quizz(pk, request)
        if error_response:
            return error_response

        quizz.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class QuizView(APIView):
    """Handle quiz listing and creation from YouTube videos.

    Provides endpoints to retrieve all quizzes for the authenticated user
    and to create new quizzes from YouTube video transcripts.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        quizzes = Quizz.objects.filter(user=request.user)
        serializer = QuizzSerializer(quizzes, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = QuizRequestSerializer(data=request.data)
        if serializer.is_valid():
            try:
                url = serializer.validated_data['url']

                # 1. Download audio from YouTube video
                audio_path = download_youtube_audio(
                    url, output_filename="temp_video")
                # 2. Transcribe audio to text
                transcript = transcribe_audio(audio_path)
                # 3. Generate quiz from transcript
                quiz_data_json = generate_quiz_from_text(transcript)
                # Convert JSON string to Python dict
                quiz_data = json.loads(quiz_data_json)

                # 1. Save quiz
                quizz = Quizz.objects.create(
                    user=request.user,
                    title=quiz_data['title'],
                    description=quiz_data['description'],
                    video_url=url
                )

                # 2. Save questions
                for q in quiz_data['questions']:
                    Question.objects.create(
                        quizz=quizz,
                        question_title=q['question_title'],
                        question_options=q['question_options'],
                        correct_answer_index=q['correct_answer_index']
                    )
                # 3. Delete temporary audio file
                if os.path.exists(audio_path):
                    os.remove(audio_path)

                serializer = QuizzSerializer(quizz)
                return Response(serializer.data, status=status.HTTP_201_CREATED)

            except Exception as e:
                return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
