from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from quizz_app.models import Quizz, Question
from quizz_app.api.serializers import QuizzSerializer, QuestionSerializer


class QuizzListView(APIView):
    def get(self, request):
        quizzes = Quizz.objects.all()
        serializer = QuizzSerializer(quizzes, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = QuizzSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class QuizzDetailView(APIView):
    def get(self, request, pk):
        try:
            quizz = Quizz.objects.get(pk=pk)
            serializer = QuizzSerializer(quizz)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Quizz.DoesNotExist:
            return Response({"detail": "Quiz not found"}, status=status.HTTP_404_NOT_FOUND)

    def put(self, request, pk):
        try:
            quizz = Quizz.objects.get(pk=pk)
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
            quizz = Quizz.objects.get(pk=pk)
            quizz.delete()
            return Response({"detail": "Quiz deleted"}, status=status.HTTP_204_NO_CONTENT)
        except Quizz.DoesNotExist:
            return Response({"detail": "Quiz not found"}, status=status.HTTP_404_NOT_FOUND)
