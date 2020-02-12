from rest_framework import serializers
from .models import Class,Subject,Topic,Quiz,Questions,Mcqs,Theory,AnswerChoice,CorrectAnswer,School

class ClassSerializer(serializers.ModelSerializer):
    class Meta:
        model  = Class
        fields = '__all__'
class SubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model  = Subject
        fields = '__all__'
class TopicSerializer(serializers.ModelSerializer):
    class Meta:
        model  = Topic
        fields = '__all__'
class QuizSerializer(serializers.ModelSerializer):
    class Meta:
        model  = Quiz
        fields = '__all__'
class QuestionsSerializer(serializers.ModelSerializer):
    class Meta:
        model  = Questions
        fields = '__all__'
class McqsSerializer(serializers.ModelSerializer):
    class Meta:
        model  = Mcqs
        fields = '__all__'
class TheorySerializer(serializers.ModelSerializer):
    class Meta:
        model  = Theory
        fields = '__all__'
class AnswerChoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model  = AnswerChoice
        fields = '__all__'
class CorrectAnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model  = CorrectAnswer
        fields = '__all__'
class SchoolSerializer(serializers.ModelSerializer):
    class Meta:
        model  = School
        fields = '__all__'