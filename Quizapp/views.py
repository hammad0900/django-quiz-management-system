from django.shortcuts import render,render_to_response,redirect,get_object_or_404
from collections import defaultdict
from django.views.decorators.csrf import csrf_exempt
import datetime
from collections import OrderedDict
from random import randint
import re
import secrets
from django.core.exceptions import ObjectDoesNotExist
import random
from django.db.models import Q
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
import MySQLdb
import json
from django.middleware.csrf import get_token
from .serializers import *
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from rest_framework.renderers import TemplateHTMLRenderer
import base64
from django.views.decorators.cache import cache_control
from rest_framework.permissions import AllowAny
from django.core.paginator import Paginator
from .models import *
from django.http import HttpResponseRedirect
from django.core.cache import cache
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated 
from rest_framework import status
from django import template
from rest_framework.response import Response
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import permission_classes
from django.views.decorators.cache import cache_page
from django.contrib.auth import authenticate, login
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from django.contrib import messages
from .forms import TopicForm,QuizForm,ClassForm,SubjectForm
import math
register = template.Library()

# Create your views here.
class dasboardview(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'index.html'
    style = {'template_pack': 'rest_framework/vertical/'}
    def get(self,request):
        topic_count=Topic.objects.all().count()
        subject_count=Subject.objects.all().count()
        class_count=Class.objects.all().count()
        return Response({'topic_count': topic_count, 'subject_count': subject_count,'class_count':class_count})

# Dashboard Section


# Topic Add/Update/Delete
class topiclist(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'topics/topic_detail.html'
    style = {'template_pack': 'rest_framework/vertical/'}

    def get(self, request):
        tok=secrets.token_hex(5)
        serializer = TopicSerializer()
        return Response({'serializer': serializer,'token':tok, 'style': self.style})

    def post(self, request):
        tok=secrets.token_hex(5)
        serializer = TopicSerializer(data=request.data)
        if serializer.is_valid():  
         serializer.save()
         return HttpResponseRedirect(redirect_to='/topics')
        
        return Response({'serializer': serializer,'token':tok, 'style': self.style})

def delete_topic(request,id):
    try:
        obj = Topic.objects.get(id=id)
        obj.delete()
        return redirect('/topics_list')
    except:
        return redirect('/topics_list')






class quizpage(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'quiz_main.html'
    permission_classes = [AllowAny]
    def get(self,request):
        return Response({'null':'null'})



class alltopics(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'topics/alltopics.html'
    def get(self, request):
        queryset = Topic.objects.all()
        serializer = TopicSerializer(queryset,many=True)
        return Response({'serializer':serializer.data,'topics': queryset})


def particular_topic_update(request, id):

    obj= get_object_or_404(Topic, id=id)
    form = TopicForm(request.POST or None, instance= obj)
    context= {'form': form}
    if form.is_valid():
            obj= form.save(commit= False)
            obj.save()
            messages.success(request, "You successfully updated the content")
            context= {'form': form}
            return render(request, 'topics/update_topic.html', context)
    else:
            context= {'form': form,
                        'error': ''}
            return render(request,'topics/update_topic.html' , context)
            
# Class Section
class SubjectsList(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name    = 'subjects/all_subjects.html'
    def get(self,request):
        try:
            subject = Subject.objects.all()
            serializer = SubjectSerializer(subject,many=True)
            return Response({'serializer':serializer.data,'subjects':subject})
        except:
            return HttpResponse("Some error ocurred")


class AddSubject(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name    = 'subjects/addsubject.html'
    style            = {'template_pack':'rest_framework/inline/'}

    def get(self,request):
        try:
            tok=secrets.token_hex(5)
            serializer = SubjectSerializer()
            return Response({'serializer':serializer,'token':tok,'style':self.style})
        except:
            return HttpResponse("Some error ocurred")
    def post(self, request):
        tok=secrets.token_hex(5)
        serializer = SubjectSerializer(data=request.data)
        if serializer.is_valid():  
         serializer.save()
         return HttpResponseRedirect(redirect_to='/add_subject')
         
        return Response({'serializer': serializer,'token':tok, 'style': self.style})


def delete_subject(request,id):
    try:
        obj=Subject.objects.get(id=id)
        obj.delete()
        return redirect('/all_subjects')
    except:
        return redirect('/all_subjects')

def particular_subject_update(request, id):
    obj= get_object_or_404(Subject, id=id)
    form = SubjectForm(request.POST or None, instance= obj)
    context= {'form': form}
    if form.is_valid():
            obj= form.save(commit= False)
            obj.save()
            messages.success(request, "You successfully updated the content")
            context= {'form': form}
            return render(request, 'subjects/update_subject.html', context)
    else:
            context= {'form': form,
                        'error': ''}
            return render(request,'subjects/update_subject.html' , context)


# Class Add/Update/Delete
class ClassList(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name    = 'classes/allclass.html'
    def get(self,request):
        classes = Class.objects.all()
        serializer = ClassSerializer(classes,many=True)
        return Response({'serializer':serializer.data,'classes':classes})

class AddClass(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name    = 'classes/addclass.html'
    style            = {'template_pack':'rest_framework/inline/'}
    def get(self,request):
        tok=secrets.token_hex(5)
        serializer = ClassSerializer()
        return Response({'serializer':serializer,'token':tok,'style':self.style})
    def post(self, request):
        tok=secrets.token_hex(5)
        serializer = ClassSerializer(data=request.data)
        if serializer.is_valid():  
         serializer.save()
         return HttpResponseRedirect(redirect_to='/add_class')
        
        return Response({'serializer': serializer,'token':tok, 'style': self.style})

def delete_class(request,id):
    try:
        obj = Class.objects.get(id=id)
        obj.delete()
        return redirect('/class_list')
    except:
        return redirect('/class_list')
def particular_class_update(request, id):
    obj= get_object_or_404(Class, id=id)
    form = ClassForm(request.POST or None, instance= obj)
    context= {'form': form}
    if form.is_valid():
            obj= form.save(commit= False)
            obj.save()
            messages.success(request, "You successfully updated the content")
            context= {'form': form}
            return render(request, 'classes/updateclass.html', context)
    else:
            context= {'form': form,
                        'error': ''}
            return render(request,'classes/updateclass.html' , context)

# Quiz Add/Update/Delete
class AddQuiz(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name    = 'quizes/addquiz.html'
    style            = {'template_pack':'rest_framework/inline/'}
    def get(self,request):
        tok=secrets.token_hex(5)
        serializer = QuizSerializer()
        return Response({'serializer':serializer,'token':tok,'style':self.style})
    def post(self, request):
        tok=secrets.token_hex(5)
        serializer = QuizSerializer(data=request.data)
        if serializer.is_valid():  
         serializer.save()
         return HttpResponseRedirect(redirect_to='/add_quiz')
        else:
            print(serializer.errors)
        return Response({'serializer': serializer,'token':tok, 'style': self.style,'errors':serializer.errors})
class QuizList(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name    = 'quizes/allquiz.html'
    def get(self,request):
        # conn = MySQLdb.connect('localhost', user='root', password='', db="quizdb")
        # cursor = conn.cursor()
        # cursor.execute("ALTER TABLE quizapp_topic ORDER BY quizapp_topic.id DESC")
        quizes = Quiz.objects.all()
        serializer = QuizSerializer(quizes,many=True)
        return Response({'serializer':serializer.data,'quizes':quizes})

def quiz_update(request, id):
    obj= get_object_or_404(Quiz, id=id)
    form = QuizForm(request.POST or None, instance= obj)
    context= {'form': form}
    if form.is_valid():
            obj= form.save(commit= False)
            obj.save()
            return redirect('/quiz_list')
            messages.success(request, "You successfully updated the Quiz")
            context= {'form': form}
            return render(request, 'quizes/updatequiz.html', context)
    else:
            context= {'form': form,
                        'error': ''}
            return render(request,'quizes/updatequiz.html' , context)

def quiz_delete(request,id):
    try:
        obj=Quiz.objects.get(id=id)
        obj.delete()
        return redirect('/quiz_list')
    except:
        return redirect('/quiz_list')


    
# Questions Add/Update/Delete
class AddQuestions(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name    = 'questions/addquestions.html'
    style            = {'template_pack':'rest_framework/inline/'}
    def get(self,request):
        serializer = QuestionsSerializer()
        return Response({'serializer':serializer,'style':self.style})
    def post(self, request):
        serializer = QuestionsSerializer(data=request.data)
        if serializer.is_valid():  
         serializer.save()
         return HttpResponseRedirect(redirect_to='/questions')
        return Response({'serializer': serializer, 'style': self.style})
class QuestionsList(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name    = 'quiz/allquiz.html'
    def get(self,request):
        questions = Questions.objects.all()
        serializer = QuestionsSerializer(questions,many=True)
        return Response({'serializer':serializer.data,'questions':questions})

def delete_questions(request,id):
    try:
        obj=Questions.objects.get(id=id)
        obj.delete()
        
        return redirect('/allquiz')
    except:
        return redirect('/allquiz')
# Mcqs Add/Update/Delete
class AddMcqs(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name    = 'mcqs/addmcqs.html'
    style            = {'template_pack':'rest_framework/inline/'}
    def get(self,request):
        serializer = McqsSerializer()
        return Response({'serializer':serializer,'style':self.style})
    def post(self, request):
        serializer = McqsSerializer(data=request.data)
        # for loop options
        if serializer.is_valid():  
         serializer.save()
        return Response({'serializer': serializer, 'style': self.style})
class McqsList(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name    = 'mcqs/allmcqs.html'
    def get(self,request):
        mcqs = Mcqs.objects.all()
        serializer = McqsSerializer(quizes,many=True)
        return Response({'serializer':serializer.data,'mcqs':mcqs})

# Theory Add/Update/Delete
class AddTheory(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name    = 'theory/addtheory.html'
    style            = {'template_pack':'rest_framework/inline/'}
    def get(self,request):
        serializer = TheorySerializer()
        return Response({'serializer':serializer,'style':self.style})
    def post(self, request):
        serializer = TheorySerializer(data=request.data)
        if serializer.is_valid():  
         serializer.save()
        return Response({'serializer': serializer, 'style': self.style})
class TheoryList(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name    = 'theory/alltheory.html'
    def get(self,request):
        theory = Theory.objects.all()
        serializer = McqsSerializer(theory,many=True)
        return Response({'serializer':serializer.data,'theories':theory})


def delete_theory(request,id):
    try:
        obj = Theory.objects.get(id=id)
        obj.delete()
        return redirect('/alltheory')
    except:
        return redirect('/alltheory')
# AnswerChoice Add/Update/Delete
class AddAnswerChoice(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name    = 'answerchoice/addanswerchoice.html'
    style            = {'template_pack':'rest_framework/inline/'}
    def get(self,request):
        serializer = AnswerChoiceSerializer()
        return Response({'serializer':serializer,'style':self.style})
    def post(self, request):
        serializer = AnswerChoiceSerializer(data=request.data)
        if serializer.is_valid():  
         serializer.save()
        return Response({'serializer': serializer, 'style': self.style})
class AnswerChoiceList(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name    = 'answerchoice/allanswerchoice.html'
    def get(self,request):
        choices = AnswerChoice.objects.all()
        serializer = AnswerChoiceSerializer(choices,many=True)
        return Response({'serializer':serializer.data,'answerchoices':choices})
# CorrectAnswer Add/Update/Delete
class AddCorrectAnswer(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name    = 'correctanswer/addcorrectanswer.html'
    style            = {'template_pack':'rest_framework/inline/'}
    def get(self,request):
        serializer = CorrectAnswerSerializer()
        return Response({'serializer':serializer,'style':self.style})
    def post(self, request):
        serializer = CorrectAnswerSerializer(data=request.data)
        if serializer.is_valid():  
         serializer.save()
        return Response({'serializer': serializer, 'style': self.style})
class CorrectAnswerList(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name    = 'mcqs/allmcqs.html'
    def get(self,request):
        try:
            correct = CorrectAnswer.objects.all()
            serializer = CorrectAnswerSerializer(correct,many=True)
            return Response({'serializer':serializer.data,'correctanswers':correct})
        except:
            return HttpResponse("Some error ocurred")

def delete_correctanswer(request,id):
    try:
        obj = CorrectAnswer.objects.get(id=id)
        obj.delete()
        return redirect('/allmcqs')
    except:
        return redirect('/allmcqs')



class load_subjects(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name    = 'subjects_dropdown_list_options.html'
    style            = {'template_pack':'rest_framework/inline/'}
    permission_classes = [AllowAny]
    def get(self,request):
        try:
            classid = request.GET.get('classes')
            subjects =  Subject.objects.filter(class_id=classid)
            serializer = SubjectSerializer(subjects,many=True)
            return Response({'serializer':serializer.data,'subjects':subjects})
        except:
            return HttpResponse("Some error ocurred")

class subjectload(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name    = 'topics_dropdown_list_options.html'
    style            = {'template_pack':'rest_framework/inline/'}
    permission_classes = [AllowAny]
    def get(self,request):
        try:
            array_list=None
            selected_topics_array=request.GET.getlist('topics_selected[]')
            topic_new=[]
            subname = request.GET.get('subjects')
            topic      =  Topic.objects.filter(Sub_id=subname)
            topic_array = list(topic)

            
            if selected_topics_array:
                array_list=list(selected_topics_array)

            for t in topic_array:
                if array_list != None:
                    if str(t.id) not in array_list:
                        topic_new.append(t)
                else:
                    topic_new.append(t)
                            
            serializer = TopicSerializer(topic,many=True)
            return Response({'serializer':serializer.data,'topics':topic_new,'selected_topics_array':selected_topics_array})
        except:
            return HttpResponse("Some error ocurred")


class questions(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name    = 'questions/questions.html'
    style            = {'template_pack':'rest_framework/inline/'}
    
    
    def get(self,request):
        try:
            quizid=Quiz.objects.all()
            serializer = QuestionsSerializer()
            return Response({'serializer':serializer,'style':self.style,'quiz':quizid})
        except:
            return HttpResponse("Some error ocurred")

    def post(self,request):
        try:
            if self.request.POST.get('mcqs') == 'MCQS':
                try:
                    pic_data=request.FILES['myfile']
                except:
                    pic_data=None
                li=[]
                checkbox=[]
                quizid = request.POST.get('quizname',False)
                myquestion=request.POST.get('question')
                marks=request.POST.get('marks')
                types=request.POST.get('mcqs')
                z=request.POST.get('textbox1')
                li.append(z)
                i=request.POST.get('textbox2')
                li.append(i)
                u=request.POST.get('textbox3')
                li.append(u)
                p=request.POST.get('textbox4')
                li.append(p)
                k=request.POST.get('textbox5')
                li.append(k)
                l=request.POST.get('textbox6')
                li.append(l)
                str_list = [x for x in li if x != '']
                question_serializer = QuestionsSerializer(data={"questype":types,"marks":marks,"quiz_id":quizid})
            

                if question_serializer.is_valid():
                    question_serializer.save()
                else:
                    print("not valid")
                mcqs_serializer     = McqsSerializer(data={'mcq_question':myquestion,'mcq_picture':pic_data,'question_id':question_serializer.data['id']})
                
                if mcqs_serializer.is_valid():
                    mcqs_serializer.save()
                
                else:
                    print(mcqs_serializer.errors)
                for data in str_list:
                    answer_choice_serializer = AnswerChoiceSerializer(data={"answer":data,"mcqs_id":mcqs_serializer.data['id']})
            

                    if answer_choice_serializer.is_valid():
                        answer_choice_serializer.save()            
                    else:
                        print(answer_choice_serializer.errors)
                alad = AnswerChoice.objects.filter(mcqs_id=mcqs_serializer.data['id'])

                if self.request.POST.get('checkbox1')=='on':
                    correct_answer_serializer = CorrectAnswerSerializer(data={"correct_ans":str(alad[0].id),"mcqs_id":mcqs_serializer.data['id']})
                    if correct_answer_serializer.is_valid():
                        correct_answer_serializer.save()
                    else:
                        print(correct_answer_serializer.errors)
                    checkbox.append(alad[0])
                if self.request.POST.get('checkbox2')=='on':
                    correct_answer_serializer = CorrectAnswerSerializer(data={"correct_ans":str(alad[1].id),"mcqs_id":mcqs_serializer.data['id']})
                    if correct_answer_serializer.is_valid():
                        correct_answer_serializer.save()
                    else:
                        print(correct_answer_serializer.errors)
                    checkbox.append(alad[1])

                if self.request.POST.get('checkbox3')=='on':

                    correct_answer_serializer = CorrectAnswerSerializer(data={"correct_ans":str(alad[2].id),"mcqs_id":mcqs_serializer.data['id']})
                    if correct_answer_serializer.is_valid():
                        correct_answer_serializer.save()
                    else:
                        print(correct_answer_serializer.errors)
                    checkbox.append(alad[2])

                if self.request.POST.get('checkbox4')=='on':
                    correct_answer_serializer = CorrectAnswerSerializer(data={"correct_ans":str(alad[3].id),"mcqs_id":mcqs_serializer.data['id']})
                    if correct_answer_serializer.is_valid():
                        correct_answer_serializer.save()
                    else:
                        print(correct_answer_serializer.errors)
                    checkbox.append(alad[3])
                if self.request.POST.get('checkbox5')=='on':
                    correct_answer_serializer = CorrectAnswerSerializer(data={"correct_ans":str(alad[4].id),"mcqs_id":mcqs_serializer.data['id']})
                    
                    if correct_answer_serializer.is_valid():
                        correct_answer_serializer.save()
                    else:
                        print(correct_answer_serializer.errors)
                    checkbox.append(alad[4])
                if self.request.POST.get('checkbox6')=='on':
                    correct_answer_serializer = CorrectAnswerSerializer(data={"correct_ans":str(alad[5].id),"mcqs_id":mcqs_serializer.data['id']})
                
                    if correct_answer_serializer.is_valid():
                        correct_answer_serializer.save()
                    else:
                        print(correct_answer_serializer.errors)
                    checkbox.append(alad[5])
                return HttpResponseRedirect(redirect_to='/questions')
        

            # Theory Questions Add
            if self.request.POST.get('theory')=='Theory':
                try:
                    pic_data=request.FILES['myfile']
                except:
                    pic_data=None
                quizid = request.POST.get('theoryquizname')
                types=request.POST.get('theory')
                marks=request.POST.get('theorymarks')
                theoryquestions=request.POST.get('theoryquestion')
                theorycorrect=request.POST.get('theorycorrect')

                question_serializer = QuestionsSerializer(data={"questype":types,"marks":marks,"quiz_id":quizid})
                if question_serializer.is_valid():
                    question_serializer.save()
                else:
                    print(question_serializer.errors)
                
                theory_serializer = TheorySerializer(data={'theory_question':theoryquestions,'correct_ans':theorycorrect,'theory_pic':pic_data,'question_id':question_serializer.data['id']})
                if theory_serializer.is_valid():
                    theory_serializer.save()
                    return HttpResponseRedirect(redirect_to='/questions')
                else:
                    print(theory_serializer.errors)
                return Response({'questions_serializer':question_serializer,'style':self.style,})

                

            return Response({'style':self.style})
        except:
            return HttpResponse("Some error ocurred")

        
class questions_details(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name    = 'questions/questions_data.html'
    style            = {'template_pack':'rest_framework/inline/'}
        
    def get(self,request,id):
        try:
            li=[]
            ans=[]
            ye=Questions.objects.filter(quiz_id=id)
            if ye.first().questype =='MCQS':
            
                for data in ye:
                    li.append(data.id)
                for questions2 in li:
                    final2 = Mcqs.objects.filter(question_id=questions2)
                    if final2.exists():
                        ans.append(final2.first())
                for questions in li:
                    final3 = Theory.objects.filter(question_id=questions)
                    if final3.exists():
                        ans.append(final3.first())
                
            elif ye.first().questype =='Theory':            
                for data in ye:
                    li.append(data.id)
                for questions2 in li:
                    final2 = Mcqs.objects.filter(question_id=questions2)
                    if final2.exists():
                        ans.append(final2.first())
                for questions in li:
                    final3 = Theory.objects.filter(question_id=questions)
                    if final3.exists():
                        ans.append(final3.first())
            return Response({'data':ans})
        except:
            return Response({'data':ans})
class manage_questions(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name    = 'questions/manage_questions.html'
    style            = {'template_pack':'rest_framework/inline/'}
    def get(self,request):
        try:
            theory_list=Theory.objects.all()
            mcqs_list = Mcqs.objects.all()
            serializer = TheorySerializer(theory_list,many=True)
            mcqs_serializer = McqsSerializer(mcqs_list,many=True)
            return Response({'serializer':serializer,'theory_list':theory_list,'mcqs_serializer':mcqs_serializer,'mcqs_list':mcqs_list})
        except:
            return HttpResponse("Some error occured")
    
class update_given_mcqs_data(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name    = 'questions/update_mcqs_questions.html'
    style            = {'template_pack':'rest_framework/inline/'}

    def post(self,request,id):
        correct_ans=[]
        answer=[]
        mcq_obj=Mcqs.objects.get(id=id)
        quiz_id2=mcq_obj.question_id.quiz_id.id
        types=request.POST.get('mcqs')
        question=request.POST.get('question')
        marks_id=request.POST.get('marks')
        questions_id2=Questions.objects.filter(quiz_id=quiz_id2)
        que_obj=Questions.objects.get(id=mcq_obj.question_id.id)
        que_obj.delete()
        question_serializer = QuestionsSerializer(data={"questype":types,"marks":marks_id,"quiz_id":mcq_obj.question_id.quiz_id.id})
        if question_serializer.is_valid():
            question_serializer.save()
        else:
            print(question_serializer.errors)
        updated_question_id=question_serializer.data['id']
        mcqs_obj=Mcqs.objects.filter(question_id=updated_question_id)
        mcqs_obj.delete()
        mcqs_serializer   = McqsSerializer(data={'mcq_question':question,'question_id':question_serializer.data['id']})
            
        if mcqs_serializer.is_valid():
            mcqs_serializer.save()
        else:
            print(mcqs_serializer.errors)
        ansobj2 = AnswerChoice.objects.filter(mcqs_id=mcqs_serializer.data['id'])
        ansobj2.delete()
        for answers in request.POST.getlist('textbox'):
            if answers!='':
             answer.append(answers)
        for data in answer:
                answer_choice_serializer = AnswerChoiceSerializer(data={"answer":data,"mcqs_id":mcqs_serializer.data['id']})
    
                if answer_choice_serializer.is_valid():
                    answer_choice_serializer.save()    
                            
                else:
                    print(answer_choice_serializer.errors)
        ansobj = AnswerChoice.objects.filter(mcqs_id=mcqs_serializer.data['id'])
        mcqs_obj_correct_answer=CorrectAnswer.objects.filter(mcqs_id=mcqs_serializer.data['id'])
        mcqs_obj_correct_answer.delete()

        try:
            if request.POST.get('checkbox1'):
                correct_answer_serializer = CorrectAnswerSerializer(data={"correct_ans":str(ansobj[0].id),"mcqs_id":mcqs_serializer.data['id']})
                if correct_answer_serializer.is_valid():
                    correct_answer_serializer.save()
                else:
                    print(correct_answer_serializer.errors)
        except:
            pass
        try:
            if request.POST.get('checkbox2'):
                correct_answer_serializer = CorrectAnswerSerializer(data={"correct_ans":str(ansobj[1].id),"mcqs_id":mcqs_serializer.data['id']})
                if correct_answer_serializer.is_valid():
                    correct_answer_serializer.save()
                else:
                    print(correct_answer_serializer.errors)

        except:
            pass
        try:
            if request.POST.get('checkbox3'):
                correct_answer_serializer = CorrectAnswerSerializer(data={"correct_ans":str(ansobj[2].id),"mcqs_id":mcqs_serializer.data['id']})
                if correct_answer_serializer.is_valid():
                    correct_answer_serializer.save()
                else:
                    print(correct_answer_serializer.errors)

        except:
            pass
        try:
            if request.POST.get('checkbox4'):
                correct_answer_serializer = CorrectAnswerSerializer(data={"correct_ans":str(ansobj[3].id),"mcqs_id":mcqs_serializer.data['id']}) 
                if correct_answer_serializer.is_valid():               
                    correct_answer_serializer.save()
                else:
                    print(correct_answer_serializer.errors)

        except:
            pass
        try:
            if request.POST.get('checkbox5'):
                correct_answer_serializer = CorrectAnswerSerializer(data={"correct_ans":str(ansobj[4].id),"mcqs_id":mcqs_serializer.data['id']})
                if correct_answer_serializer.is_valid():
                    correct_answer_serializer.save()
                else:
                    print(correct_answer_serializer.errors)

        except:
            pass
        try:
            if request.POST.get('checkbox6'):
                correct_answer_serializer = CorrectAnswerSerializer(data={"correct_ans":str(ansobj[5].id),"mcqs_id":mcqs_serializer.data['id']})
                if correct_answer_serializer.is_valid():
                    correct_answer_serializer.save()
                else:
                    print(correct_answer_serializer.errors)

        except:
            pass
        return HttpResponseRedirect(redirect_to='/manage_questions')
        
       


    def get(self,request,id):
        li=[]
        li2=[]
        quizin=Quiz.objects.all()
        try:
            obj = Mcqs.objects.get(id=id)
            if obj.mcq_picture:
                mcq_picture=obj.mcq_picture
            else:
                mcq_picture=None
            answer=CorrectAnswer.objects.filter(mcqs_id=obj.id)
            Answer_choice = AnswerChoice.objects.filter(mcqs_id=obj.id)
            
            for cr in answer:
                li.append(cr)
            all_answers=[]
            for item in Answer_choice:
                for x in answer:
                    if (item.id == x.correct_ans_id):
                        item.flag = "True"
                        break
                    else:
                        item.flag = "False"
                all_answers.append(item)
            for ansch in Answer_choice:
                li2.append(ansch)

            for bc in li:
                for ans in li2:
                        if str(bc)==str(ans):
                            print()
                        else:
                            print()
            len_answer_choice=len(Answer_choice)  
            
            return Response({'quiz':obj.question_id.quiz_id,'question':obj.mcq_question,'picture':mcq_picture,'marks':obj.question_id.marks,'answerchoice':all_answers,'li':li,'li2':li2,'range':range(len_answer_choice,6)})
        except:
            return HttpResponseRedirect(redirect_to='/manage_questions')
    

            

        
class manage_theory_question(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name    = 'questions/update_theory_questions.html'
    style            = {'template_pack':'rest_framework/inline/'}
    def get(self,request):
        try:
            thoery_obj=Theory.objects.all()
            serializer = TheorySerializer(thoery_obj)
            return Response({"serializer":serializer,"theory_list":thoery_obj})
        except:
            return HttpResponse("Some error ocurred")

class update_question(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name    = 'questions/update_theory.html'
    style            = {'template_pack':'rest_framework/inline/'}
    def post(self,request,id):
        try:
            theory_obj=Theory.objects.get(id=id)
            quizid = request.POST.get('quiz_id')
            theory_question_id=request.POST.get('theoryquestion')
            theory_marks_id=request.POST.get('theorymarks')
            correct_answer_id=request.POST.get('theorycorrect')
            types=request.POST.get('theory')
            question_serializer = QuestionsSerializer(theory_obj.question_id,data={"questype":types,"marks":theory_marks_id,"quiz_id":theory_obj.question_id.quiz_id.id})
        
            if question_serializer.is_valid():
                question_serializer.save()
            else:
                print(question_serializer.errors)
            
            theory_serializer = TheorySerializer(theory_obj,data={'theory_question':theory_question_id,'correct_ans':correct_answer_id,'question_id':question_serializer.data['id']})
            if theory_serializer.is_valid():
                theory_serializer.save()
                return HttpResponseRedirect(redirect_to='/manage_theory_question')

            else:
                print(theory_serializer.errors)
            return HttpResponseRedirect(redirect_to='/manage_theory_question')
        except:
            return HttpResponseRedirect(redirect_to='/manage_theory_question')
    def get(self,request,id):
        try:
            request.session.flush()
            theory_obj=Theory.objects.get(id=id)
            question_id=theory_obj.question_id
            if theory_obj.theory_pic:
                theory_pic=theory_obj.theory_pic
            else:
                theory_pic=None
            theory_marks=theory_obj.question_id.marks
            correct_ans_id=theory_obj.correct_ans
            quiz_id=theory_obj.question_id.quiz_id
            return Response({"question":theory_obj,"marks":theory_marks,"answer":correct_ans_id,"quizid":quiz_id,'picture':theory_pic})
        except:
            return HttpResponse("Some error ocurred")
class delete_manage_questions_mcqs(APIView):
    def get(self,request,id):
        try:
            obj=Mcqs.objects.get(id=id)
            question_obj=Questions.objects.get(id=obj.question_id_id)
            question_obj.delete()
            return HttpResponseRedirect(redirect_to='/manage_questions')
        except:
            return HttpResponseRedirect(redirect_to='/manage_questions')
            
class delete_theory_question(APIView):
    def get(self,request,id):
        try:
            theory_obj=Theory.objects.get(id=id)
            question_obj=Questions.objects.get(id=theory_obj.question_id_id)
            question_obj.delete()
            return HttpResponseRedirect(redirect_to='/manage_theory_question')
        except:
            return HttpResponseRedirect(redirect_to='/manage_theory_question')
previous_page=[]
current_page=[]
class teacher_quiz(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name    = 'quiz_selection/teacher_selection_quiz.html'
    style            = {'template_pack':'rest_framework/inline/'}
    permission_classes = [AllowAny]
    def post(self,request):
        try:
            time_per_question=int(request.POST.get('timeperquestion'))
            time_per_question = time_per_question * 60
            request.session['total_time']=str(time_per_question)
            request.session['time_per_question']=str(time_per_question)
            d.clear()
            request.session['saved'] = None
            send_topics=[]
            topic_list=[]
            number_of_topics=[]
            questions_objs=[]
            questions_list=[]
            class_id=request.POST.get('Class')
            subject_id=request.POST.get('subject')
            for i in range(0,len(request.data)):
                if  request.data.get('topic'+str(i))!=None:
                    topic_list.append(request.data.get('topic'+str(i)))
                    send_topics.append(request.data.get('topic'+str(i)))
                    number_of_topics.append(request.data.get('num'+str(i)))
            number_of_topics=list(map(int, number_of_topics))
            topic_list=list(map(str, topic_list))
            quiz_obj=Quiz.objects.filter(Q(topic=topic_list[0]) & Q(Class=class_id) & Q(subject=subject_id))
            for count_mcqs in range (0,len(topic_list)):
                    quiz_obj=Quiz.objects.filter(Q(topic=str(topic_list[count_mcqs])) & Q(Class=class_id) & Q(subject=subject_id))
                    for p in quiz_obj:
                        ques=Questions.objects.filter(quiz_id=p)[:number_of_topics[count_mcqs]]
                        questions_objs.append(ques)
            data_check=Questions.objects.all()
            for q in questions_objs:
                for x in q:
                    questions_list.append(str(x.id))
            random.shuffle(questions_list)
            request.session['questions_list']=questions_list
            request.session['send_topics']=send_topics
            return HttpResponse("bye")
        except:
            return HttpResponseRedirect(redirect_to='/quiz_section')
        
    def get(self,request):
        try:

            d.clear()
            request.session.flush()
            current_page.clear()
            previous_page.clear()
            times.clear()
            classid=Class.objects.all()
            subjectid=Subject.objects.all()
            topicid=Topic.objects.all()
            return Response({'class':classid,'subject':subjectid,'topic':topicid})
        except:
            return HttpResponseRedirect(redirect_to='/quiz_section')

class conduct_quiz(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name    = 'quiz_selection/conduct_quiz.html'
    style            = {'template_pack':'rest_framework/inline/'}
    permission_classes = [AllowAny]
    

    def post(self,request):
        try:
            result=request.session['result_list']
            return HttpResponse(result)
        except:
            return HttpResponseRedirect(redirect_to='/quiz_section')
    def get(self,request):
                time_per_question=request.session.get('time_per_question')
                if request.build_absolute_uri() not in previous_page and request.build_absolute_uri() in current_page:
                    print('I AM REFRESHED')
                elif request.build_absolute_uri() in previous_page:
                    print('I BELONG TO PREVIOUS PAGE')
                    request.session.flush()
                    previous_page.clear()
                    current_page.clear()

                    return HttpResponseRedirect(redirect_to='/quiz_section')
                else:
                    print('I AM MOVING FORWARD, EVERYTHING IS FINE')
                    if "current_page_url" in request.session:
                        request.session['previous_page_url']=request.session['current_page_url']
                        previous_page.append(request.session['previous_page_url'])

                    request.session['current_page_url']=request.build_absolute_uri()   
                    current_page.append(request.session['current_page_url'])
    
                ques_obj=[]
                overall_questions=[]
                answer_choices=[]
                q_obj=[]
                questions_list=request.session['questions_list']
                for obj in questions_list:
                    ques_obj=Questions.objects.get(id=obj)
                    q_obj.append(ques_obj)

                for quest in q_obj:
                    if quest.questype == 'MCQS':
                            mcq_obj = Mcqs.objects.get(question_id=quest)
                            overall_questions.append(mcq_obj)
                    elif quest.questype =='Theory':
                        theory_obj = Theory.objects.get(question_id=quest)
                        overall_questions.append(theory_obj)
                    else:
                        pass     
                for l in overall_questions:
                    if l.question_id.questype =='MCQS':
                            if len(q_obj)==1:
                                ans_obj=AnswerChoice.objects.filter(mcqs_id=l.id)
                                answer_choices.append(ans_obj)
                            elif len(q_obj)>1:
                                ans_obj=AnswerChoice.objects.filter(mcqs_id=l.id)
                                answer_choices.append(ans_obj)
                            else:
                                pass

                question_type = ""
                all_questions = {}
                for count, item in enumerate(questions_list, start=1):
                    ques_obj=Questions.objects.get(id=item)
                    if ques_obj.questype == 'Theory':
                        item = ques_obj.theory_set.values_list('id', flat=True)[0]
                    if ques_obj.questype == 'MCQS':
                        item = ques_obj.mcqs_set.values_list('id', flat=True)[0]
                    all_questions[count] = item
                for question in overall_questions:
                    
                    if question.question_id.questype=="MCQS":
                        ans_obj=AnswerChoice.objects.filter(mcqs_id=question.id)
                        for answers in answer_choices:
                                if question.id==answers.first().mcqs_id.id:
                                    for complete_ans in answers:
                                        check=CorrectAnswer.objects.filter(mcqs_id=question.id)
                                        if len(check)>1:
                                            complete_ans.flag="True"
                                        else:
                                            complete_ans.flag="False"
                    
                paginator = Paginator(overall_questions,1)

                page=int(request.GET.get('page',1))
                questionsp=paginator.page(page)
                questionsp=paginator.get_page(page)
                for t in questionsp.object_list:
                    if 'Theory' in t.question_id.questype:
                        question_type='theory'
                    elif len(CorrectAnswer.objects.filter(mcqs_id=t)) > 1:
                        question_type='checkbox'
                    else:
                        question_type='radio'

                total_pages=paginator.count
                
                return Response({'question_type':question_type, 'questions':overall_questions,'answer_choice':answer_choices,'questionsp':questionsp,'time_per_question':time_per_question,'all_questions':all_questions, 'range':range(page,questionsp.paginator.num_pages + 1)})
     

d = defaultdict(list)
@csrf_exempt
def result(request):
    try:
        if request.method == 'POST': 
            result_data=[
                ("id",request.POST.get('answer[id]')),
                ("answer_submitted" , request.POST.getlist('answer[answer_submitted][]'))
                ]
            for k,v in result_data:
                d[k].append(v)
            for key,value in d.items():
                print("key",key)
                print("value",value)
            return HttpResponse("POST")
        elif request.method== 'GET':
            return HttpResponse("GET METHOD OF END RESULT")
    except:
        return HttpResponseRedirect(redirect_to='/quiz_section')



class user_result(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name    = 'quiz_selection/user_result.html'
    style            = {'template_pack':'rest_framework/inline/'}
    permission_classes = [AllowAny]
    def get(self,request):
        # try:
            print(request.session['time_taken'])
            minutes=math.floor(int(request.session['time_taken']) / 60)
            if minutes in range(0,10):
                minutes='0'+str(minutes)
            seconds=math.floor(int(request.session['time_taken']) % 60)
            if seconds in range(0,10):
                seconds='0'+str(seconds)
            topics=request.session['send_topics']
            topic_dict = defaultdict(list)
            len_flag=False
            wrong_answers_list=[]
            correct_answers_list=[]
            total_marks=[]
            overall_marks=[]
            topic_marks = {}
            x=d.items()
            total_length=len(d.get('id'))
            for topic in topics:
                topic_marks[topic]=defaultdict(int)
            for total_questions_id in range(0,total_length):
                for topic in topics:
                    try:
                        theory_obj=Theory.objects.get(id=d.get('id')[total_questions_id])
                        if str(theory_obj.question_id.quiz_id.topic.id) == str(topic):
                            topic_marks[topic]["total_questions"] = topic_marks[topic]["total_questions"] + 1
                    except ObjectDoesNotExist:
                        mcqs_obj=Mcqs.objects.get(id=d.get('id')[total_questions_id])
                        if str(mcqs_obj.question_id.quiz_id.topic.id) == str(topic):
                            topic_marks[topic]["total_questions"] = topic_marks[topic]["total_questions"] + 1
                try:
                    theory_obj=Theory.objects.get(id=d.get('id')[total_questions_id])
                    overall_marks.append(theory_obj.question_id.marks)
                    if theory_obj.correct_ans == ' '.join(d.get('answer_submitted')[total_questions_id]):
                        total_marks.append(theory_obj.question_id.marks)
                        for topic in topics:
                            if str(theory_obj.question_id.quiz_id.topic.id) == str(topic):
                                topic_marks[topic]["correct"] = topic_marks[topic]["correct"] + 1
                    else:
                        wrong_answers_list.append(theory_obj)
                        correct_answers_list.append(theory_obj.correct_ans)
                except ObjectDoesNotExist:
                    mcqs_obj=Mcqs.objects.get(id=d.get('id')[total_questions_id])
                    cr_obj=CorrectAnswer.objects.filter(mcqs_id=mcqs_obj.id)
                    overall_marks.append(mcqs_obj.question_id.marks)
                    mcq_ans =CorrectAnswer.objects.filter(mcqs_id=mcqs_obj)
                    mcq_ans_obj = ' '.join(map(str, mcq_ans.values_list('correct_ans_id')))
                    rep=mcq_ans_obj.replace(',','')
                    rep3=rep.replace(')','')
                    correct_answer_object=rep3.replace('(','')
                    correct_answer_object=correct_answer_object.replace('UUID','')
                    correct_answer_object=correct_answer_object.replace("'",'')
                    given_answer_object=' '.join(d.get('answer_submitted')[total_questions_id])
                    if str(correct_answer_object) == str(given_answer_object):
                        total_marks.append(mcqs_obj.question_id.marks)
                        for topic in topics:
                            if str(mcqs_obj.question_id.quiz_id.topic.id) == str(topic):
                                topic_marks[topic]["correct"] = topic_marks[topic]["correct"] + 1
                    else:
                        wrong_answers_list.append(mcqs_obj)
                        correct_answers_list.append(cr_obj)
            total_marks=sum(total_marks)
            overall_marks=sum(overall_marks)
            fusion = zip(wrong_answers_list, correct_answers_list) 
            dictionary=dict(fusion)
            

            for k,v in dictionary.items():
                for topic in topics:
                    if str(k.question_id.quiz_id.topic.id) == str(topic):
                        local_dict={k:v}
                        topic_dict[Topic.objects.get(id=topic)].append(local_dict)


            for key,value in topic_dict.items():
                for questions in value:
                    for k,v in questions.items():
                        try:
                            theoryobj=Theory.objects.get(theory_question=k)
                            k.len_flag ="True"
                        except ObjectDoesNotExist:
                            for answer in v:
                                print()
            for key,value in dictionary.items():
                try:
                    theoryobj=Theory.objects.get(theory_question=key)
                    key.len_flag ="True"
                except ObjectDoesNotExist:
                    for t in value:
                        print()
            topic_marks_refactored = {}
            for k, v in topic_marks.items():
                topic_marks_refactored[k] = dict(v)
            # request.session.flush()
            # current_page.clear()
            # previous_page.clear()
            
            return Response({'total_marks':total_marks,'overall_marks':overall_marks,'wrong_answers_list':wrong_answers_list,'correct_answers_list':correct_answers_list,'dictionary':topic_dict.items(),'topic_marks':topic_marks_refactored.items(),'minutes':minutes, 'seconds':seconds})

        # except:
        #     return HttpResponseRedirect(redirect_to='/quiz_section')   
times=[]
@csrf_exempt
def timer(request):
    if request.method=='GET':
        real_time=request.GET.get('timer')
       
        times.append(real_time)
        return HttpResponse("null")
    elif request.method=='POST':
        updated_time=request.POST.get('updated_time')
        # print(request.session.get('time_per_question'),"before updation")
        print(request.session['total_time'], 'THIS IS TOTAL TIME FOR QUIZ')
        print(updated_time, 'THIS IS TIMER GET')
        time_taken=int(request.session['total_time']) - int(updated_time)

        print(time_taken, 'THIS IS TIME TAKEN FOR QUIZ')
        if time_taken > 0:
            request.session['time_taken']=time_taken
        request.session['time_per_question']=updated_time
        request.session.save()
        return HttpResponse('null')

# Add SChool
class add_school(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'school/addschool.html'
    style = {'template_pack': 'rest_framework/vertical/'}

    def get(self, request):
        serializer = SchoolSerializer()
        return Response({'serializer': serializer, 'style': self.style})

    def post(self, request):
        serializer = SchoolSerializer(data=request.data)
        if serializer.is_valid():  
         serializer.save()
         return HttpResponseRedirect(redirect_to='/topics')
        
        return Response({'serializer': serializer, 'style': self.style})

def delete_school(request,id):
    try:
        obj = School.objects.get(id=id)
        obj.delete()
        return redirect('/topics_list')
    except:
        return redirect('/topics_list')




class all_school(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'school/all_school.html'
    def get(self, request):
        queryset = School.objects.all()
        serializer = SchoolSerializer(queryset,many=True)
        return Response({'serializer':serializer.data,'schools': queryset})


def particular_school_update(request, id):
    obj= get_object_or_404(School, id=id)
    form = SchoolForm(request.POST or None, instance= obj)
    context= {'form': form}
    if form.is_valid():
            obj= form.save(commit= False)
            obj.save()
            messages.success(request, "You successfully updated the content")
            context= {'form': form}
            return render(request, 'school/update_school.html', context)
    else:
            context= {'form': form,
                        'error': ''}
            return render(request,'school/update_school.html', context)