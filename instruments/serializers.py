from rest_framework import serializers
from instruments.models import Form, Question, \
    Choice, AnswerSheet, Answer


class ChoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Choice
        fields = '__all__'

class ChoiceNestedSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    class Meta:
        model = Choice
        fields = ['id', 'text', 'is_correct', 'weight']

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


class AnswerSerializer(serializers.Serializer):
    form = serializers.IntegerField()
    answers = serializers.DictField(child=serializers.IntegerField())

    def validate_answers(self, answers):
        validated_answers = {}
        for key, choice_id in answers.items():
            question_id = int(key.split('_')[1])

            try:
                question = Question.objects.get(id=question_id)
                choice = Choice.objects.get(id=choice_id, question=question)
                validated_answers[question] = choice
            except (Question.DoesNotExist, Choice.DoesNotExist):
                raise serializers.ValidationError(f"Invalid question or choice for {key}.")
        
        return validated_answers


class AnswerListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = '__all__'


class AnswerSheetSerializer(serializers.ModelSerializer):
    sheet_answers = AnswerListSerializer(many=True, read_only=True)
    
    class Meta:
        model = AnswerSheet
        fields = '__all__'