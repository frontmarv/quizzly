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

    def get(self, request, pk):
        try:
            quizz = Quizz.objects.get(pk=pk, user=request.user)
            serializer = QuizzSerializer(quizz)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Quizz.DoesNotExist:
            return Response({"detail": "Quiz not found"}, status=status.HTTP_404_NOT_FOUND)

    def patch(self, request, pk):
        try:
            quizz = Quizz.objects.get(pk=pk, user=request.user)
            serializer = QuizzSerializer(
                quizz, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Quizz.DoesNotExist:
            return Response({"detail": "Quiz not found"}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, pk):
        try:
            quizz = Quizz.objects.get(pk=pk, user=request.user)
            quizz.delete()
            return Response({"detail": "Quiz deleted"}, status=status.HTTP_204_NO_CONTENT)
        except Quizz.DoesNotExist:
            return Response({"detail": "Quiz not found"}, status=status.HTTP_404_NOT_FOUND)


class GenerateQuizView(APIView):
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
