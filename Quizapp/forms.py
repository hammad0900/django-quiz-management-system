from django import forms
from .models import *

class TopicForm(forms.ModelForm):
    class Meta:
        model = Topic
        fields = '__all__'
class QuizForm(forms.ModelForm):
    class Meta:
        model = Quiz
        fields ='__all__'
class ClassForm(forms.ModelForm):
    class Meta:
        model = Class
        fields ='__all__'

class SubjectForm(forms.ModelForm):
    class Meta:
        model = Subject
        fields = '__all__'
class SchoolForm(forms.ModelForm):
    class Meta:
        model = School
        fields = '__all__'
    
        