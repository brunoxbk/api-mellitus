from rest_framework import serializers
from instruments.models import Form, Question, Choice, AnswerSheet, Answer


class ChoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Choice
        fields = '__all__'

class ChoiceNestedSerializer(serializers.ModelSerializer):
    class Meta:
        model = Choice
        fields = ['text', 'is_correct', 'weight']

class QuestionSerializer(serializers.ModelSerializer):
    choices = ChoiceNestedSerializer(many=True, required=False)
    
    class Meta:
        model = Question
        fields = '__all__'

    def create(self, validated_data):
        choices_data = validated_data.pop('choices')
        question = Question.objects.create(**validated_data)
        for choice_data in choices_data:
            Choice.objects.create(question=question, **choice_data)
        return question

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
