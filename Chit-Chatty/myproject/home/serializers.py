from rest_framework import serializers
from .models import Member, Quiz, Question


# Serializer for the Member model
class MemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = Member
        fields = '__all__'


# Serializer for the Quiz Model
class QuizSerializer(serializers.ModelSerializer):
    class Meta:
        model = Quiz
        fields = '__all__'


# Serializer for the Question Model
class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = '__all__'
