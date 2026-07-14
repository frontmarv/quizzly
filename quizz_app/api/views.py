import os

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from quizz_app.models import Quizz, Question
from quizz_app.api.serializers import QuizzSerializer, QuestionSerializer, QuizRequestSerializer
from rest_framework.permissions import IsAuthenticated
import json
from ..services.services import download_youtube_audio, transcribe_audio, generate_quiz_from_text


class QuizzDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get_user_quizz(self, pk, request):
        """Get quiz and verify it belongs to the user. Returns (quizz, error_response)."""
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

                # 1. Audio laden
                audio_path = download_youtube_audio(
                    url, output_filename="temp_video")
                # 2. Text transkribieren
                transcript = transcribe_audio(audio_path)
                # Quizz erstellen
                quiz_data_json = generate_quiz_from_text(transcript)
                # JSON String zu Python Dict
                quiz_data = json.loads(quiz_data_json)

                # 1. Quiz speichern
                quizz = Quizz.objects.create(
                    user=request.user,
                    title=quiz_data['title'],
                    description=quiz_data['description'],
                    video_url=url
                )

                # 2. Fragen speichern
                for q in quiz_data['questions']:
                    Question.objects.create(
                        quizz=quizz,
                        question_title=q['question_title'],
                        question_options=q['question_options'],
                        correct_answer_index=q['correct_answer_index']
                    )
                # 3. Temporäre Audiodatei löschen
                if os.path.exists(audio_path):
                    os.remove(audio_path)

                serializer = QuizzSerializer(quizz)
                return Response(serializer.data, status=status.HTTP_201_CREATED)

            except Exception as e:
                return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
