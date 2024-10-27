from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from instruments.models import Form, Question, Choice, AnswerSheet, Answer
from instruments.serializers import FormSerializer, QuestionSerializer, \
    ChoiceSerializer, AnswerSheetSerializer, AnswerSerializer


class FormListCreateView(generics.ListCreateAPIView):
    queryset = Form.objects.all()
    serializer_class = FormSerializer
    permission_classes = [AllowAny]

class FormDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Form.objects.all()
    serializer_class = FormSerializer
    permission_classes = [IsAuthenticated]

class QuestionListCreateView(generics.ListCreateAPIView):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    permission_classes = [AllowAny]

class QuestionDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    permission_classes = [IsAuthenticated]

class ChoiceListCreateView(generics.ListCreateAPIView):
    queryset = Choice.objects.all()
    serializer_class = ChoiceSerializer
    permission_classes = [AllowAny]

class ChoiceDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Choice.objects.all()
    serializer_class = ChoiceSerializer
    permission_classes = [IsAuthenticated]

class AnswerSheetListCreateView(generics.ListCreateAPIView):
    queryset = AnswerSheet.objects.all()
    serializer_class = AnswerSheetSerializer
    permission_classes = [IsAuthenticated]

class AnswerSheetDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = AnswerSheet.objects.all()
    serializer_class = AnswerSheetSerializer
    permission_classes = [IsAuthenticated]

class AnswerListCreateView(generics.ListCreateAPIView):
    queryset = Answer.objects.all()
    serializer_class = AnswerSerializer
    permission_classes = [IsAuthenticated]

class AnswerDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Answer.objects.all()
    serializer_class = AnswerSerializer
    permission_classes = [IsAuthenticated]


class QuestionBulkCreateView(APIView):
    permission_classes = [AllowAny]
    def post(self, request, *args, **kwargs):
        serializer = QuestionSerializer(data=request.data, many=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SubmitAnswersView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        user = self.request.user
        serializer = AnswerSerializer(data=request.data)
        
        if serializer.is_valid():
            form = serializer.validated_data['form']
            answers = serializer.validated_data['answers']

            answer_sheet, created = AnswerSheet.objects.get_or_create(
                form_id=form,
                user=user,
            )

            for question, choice in answers.items():
                answer, created = Answer.objects.get_or_create(
                    answer_sheet=answer_sheet,
                    question=question,
                    defaults={
                        'choice': choice
                    }
                )

                answer.choice = choice
                answer.save()

            return Response({"message": "Answers submitted successfully."}, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
