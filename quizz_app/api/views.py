import json
import os

from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from quizz_app.api.serializers import QuizzSerializer, QuizRequestSerializer
from quizz_app.models import Quizz, Question
from ..services.download_youtube_audio import download_youtube_audio
from ..services.transcribe_audio import transcribe_audio
from ..services.generate_quiz_from_text import generate_quiz_from_text


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
        """Retrieve a specific quiz by its ID.

        Fetches the quiz and returns its serialized data if it belongs to
        the authenticated user.

        Args:
            request: HTTP request object
            pk: Primary key of the quiz to retrieve

        Returns:
            Response: Serialized quiz data with 200 status code,
                or error response with 404/403 status code
        """
        quizz, error_response = self.get_user_quizz(pk, request)
        if error_response:
            return error_response

        serializer = QuizzSerializer(quizz)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def patch(self, request, pk):
        """Partially update a quiz.

        Allows the quiz owner to update specific fields of the quiz.
        Supports partial updates (only provided fields are updated).

        Args:
            request: HTTP request object with partial quiz data
            pk: Primary key of the quiz to update

        Returns:
            Response: Updated serialized quiz data with 200 status code,
                error response with 400/403/404 status code if update fails
        """
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
        """Delete a specific quiz.

        Permanently removes the quiz and all associated questions if the
        quiz belongs to the authenticated user.

        Args:
            request: HTTP request object
            pk: Primary key of the quiz to delete

        Returns:
            Response: Empty response with 204 status code on success,
                or error response with 403/404 status code if deletion fails
        """
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
        """Retrieve all quizzes for the authenticated user.

        Returns a list of all quizzes created by the authenticated user,
        including all associated questions.

        Args:
            request: HTTP request object

        Returns:
            Response: List of serialized quiz data with 200 status code
        """
        quizzes = Quizz.objects.filter(user=request.user)
        serializer = QuizzSerializer(quizzes, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        """Create a new quiz from a YouTube video.

        Processes a YouTube video by downloading its audio, transcribing it,
        and generating a quiz from the transcript. Creates the quiz with
        all associated questions in the database.

        Args:
            request: HTTP request object containing:
                - url (str): YouTube video URL

        Returns:
            Response: Serialized quiz data with 201 status code on success,
                or error response with 400/500 status code on failure.
                The response includes the created quiz and all questions.
        """
        serializer = QuizRequestSerializer(data=request.data)
        if serializer.is_valid():
            try:
                url = serializer.validated_data['url']

                audio_path = download_youtube_audio(
                    url, output_filename="temp_video")
                transcript = transcribe_audio(audio_path)
                quiz_data_json = generate_quiz_from_text(transcript)
                quiz_data = json.loads(quiz_data_json)

                quizz = Quizz.objects.create(
                    user=request.user,
                    title=quiz_data['title'],
                    description=quiz_data['description'],
                    video_url=url
                )

                for q in quiz_data['questions']:
                    Question.objects.create(
                        quizz=quizz,
                        question_title=q['question_title'],
                        question_options=q['question_options'],
                        correct_answer_index=q['correct_answer_index']
                    )
                if os.path.exists(audio_path):
                    os.remove(audio_path)

                serializer = QuizzSerializer(quizz)
                return Response(serializer.data, status=status.HTTP_201_CREATED)

            except Exception as e:
                return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
