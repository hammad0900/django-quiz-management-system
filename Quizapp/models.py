from django.db import models
import secrets
from django.db.models.signals import post_save
import uuid
from django.dispatch import receiver
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from django.http import HttpResponse
from django.conf import settings
from uuid import UUID
# Create your models here.

class Class(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=20,null=False)
    code = models.CharField(max_length=15,null=False,blank=False)
    
    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Classes"


class Subject(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name     = models.CharField(max_length=15,null=False)
    code     = models.CharField(max_length=15,null=False,blank=False)
    class_id = models.ForeignKey(
        to = Class,
        on_delete = models.CASCADE,
    )

    def __str__(self):
        return (self.name)
    class Meta:
        verbose_name_plural = "Subjects"


class Topic(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name     = models.CharField(max_length=15,null=False)
    code     = models.CharField(max_length=15,null=False,blank=False)
    Sub_id   = models.ForeignKey(
        to = Subject,
        on_delete = models.CASCADE,
    )
    def __str__(self):
        return self.name
    class Meta:
        verbose_name_plural = "Topics"

class Quiz(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    Class      = models.ForeignKey(
        to=Class,
        on_delete=models.CASCADE,
        blank=False,null=False,

    )
    subject    = models.ForeignKey(
        to=Subject,
        on_delete=models.CASCADE,
        blank=False,null=False,
    )
    topic      = models.OneToOneField(
        to=Topic,
        on_delete=models.CASCADE,
        blank=False,null=False,
    )
    name       = models.CharField(max_length=15,unique=True,blank=False,null=False,)
    code       = models.CharField(max_length=15,null=False,blank=False)
    created_by = models.CharField(max_length=15 ,blank=False,null=False,)
    
    def __str__(self):
        return (self.name)
    class Meta:
        verbose_name_plural = "Quizes"


class Questions(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    questype = models.CharField(max_length=15,null=False)
    marks    = models.IntegerField(null=False)
    quiz_id  = models.ForeignKey(
        to=Quiz,
        on_delete=models.CASCADE
        )
    def __str__(self):
        return (self.questype)

    class Meta:
        verbose_name_plural = "Questions"


class Mcqs(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    mcq_question    = models.TextField(max_length=500,null=False)
    mcq_picture     = models.FileField(upload_to='images/',null=True,blank=True)
    question_id     = models.ForeignKey(
        to=Questions,
        on_delete=models.CASCADE
    )

    def __str__(self):
        return str(self.mcq_question)
    class Meta:
        verbose_name_plural = "MCQS"    

class Theory(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    theory_question = models.TextField(max_length=500,null=False)
    correct_ans     = models.CharField(max_length=200,null=False)
    theory_pic      = models.FileField(upload_to='images/',null=True,blank=True)
    question_id     = models.ForeignKey(
         to=Questions,
         on_delete=models.CASCADE
        )
    def __str__(self):
        return (self.theory_question) 
    class Meta:
        verbose_name_plural = "Theories"


class AnswerChoice(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    answer  = models.CharField(max_length=200,null=False)
    mcqs_id = models.ForeignKey(
        to=Mcqs,
        on_delete=models.CASCADE
    )
    def __str__(self):
        return (self.answer)
    class Meta:
        verbose_name_plural = "Answer's Choices"


class CorrectAnswer(models.Model):
    correct_ans = models.ForeignKey(to=AnswerChoice,on_delete=models.CASCADE)
    mcqs_id     = models.ForeignKey(
        to=Mcqs,
        on_delete=models.CASCADE
    )

    def __str__(self):
        return str((self.correct_ans))
    class Meta:
        verbose_name_plural = "Correct Answers"

        
class School(models.Model):
    name    = models.CharField(max_length=200)
    address = models.CharField(max_length=150)
    