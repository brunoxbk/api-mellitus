from rest_framework import serializers
from instruments.models import Form, Question, Choice, AnswerSheet, Answer


class ChoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Choice
        fields = '__all__'

class QuestionSerializer(serializers.ModelSerializer):
    choices = ChoiceSerializer(many=True, read_only=True)
    
    class Meta:
        model = Question
        fields = '__all__'

class FormSerializer(serializers.ModelSerializer):
    questions = QuestionSerializer(many=True, read_only=True)
    
    class Meta:
        model = Form
        fields = '__all__'

class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = '__all__'

class AnswerSheetSerializer(serializers.ModelSerializer):
    sheet_answers = AnswerSerializer(many=True, read_only=True)
    
    class Meta:
        model = AnswerSheet
        fields = '__all__'
