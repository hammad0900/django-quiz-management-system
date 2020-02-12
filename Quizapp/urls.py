from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token 
from . import views
urlpatterns=[
    path('topics/',views.topiclist.as_view()),
    path('topics_list/',views.alltopics.as_view()),
    path('particulartopic/<str:id>',views.particular_topic_update,name='particulartopic'),
    path('delete_topic/<str:id>',views.delete_topic,name='delete_topic'),
    path('subjects_list/',views.SubjectsList.as_view()),
    path('add_subject/',views.AddSubject.as_view()),
    path('delete_subject/<str:id>',views.delete_subject,name='delete_subject'),
    path('subject_update/<str:id>',views.particular_subject_update,name='subject_update'),
    path('add_class/',views.AddClass.as_view()),
    path('class_list/',views.ClassList.as_view()),
    path('delete_class/<str:id>',views.delete_class,name='delete_class'),
    path('class_update/<str:id>',views.particular_class_update,name='class_update'),
    path('add_quiz/',views.AddQuiz.as_view()),
    path('quiz_list/',views.QuizList.as_view()),
    path('quiz_update/<str:id>',views.quiz_update,name='quiz_update'),
    path('quiz_delete/<str:id>',views.quiz_delete,name='quiz_delete'),
    path('questions_details/<str:id>',views.questions_details.as_view(),name='questions_details'),
    path('manage_questions/',views.manage_questions.as_view()),
    path('update_manage_questions_mcqs/<str:id>',views.update_given_mcqs_data.as_view(),name='update_manage_questions_mcqs'),
    path('manage_theory_question/',views.manage_theory_question.as_view(),name='manage_theory_question'),
    path('update_question/<str:id>',views.update_question.as_view(),name='update_question'),
    path('delete_manage_questions_mcqs/<str:id>',views.delete_manage_questions_mcqs.as_view(),name='delete_manage_questions_mcqs'),
    path('delete_theory_question/<str:id>',views.delete_theory_question.as_view(),name='delete_theory_question'),
    path('add_question/',views.AddQuestions.as_view()),
    path('questions_list/',views.QuestionsList.as_view()),
    path('delete_questions/<str:id>',views.delete_questions,name='delete_questions'),
    path('addmcqs/',views.AddMcqs.as_view()),
    path('mcqs_list/',views.McqsList.as_view()),
    path('addtheory/',views.AddTheory.as_view()),
    path('theory_list/',views.TheoryList.as_view()),
    path('delete_theory/<str:id>',views.delete_theory,name='delete_theory'),
    path('addanswerchoice/',views.AddAnswerChoice.as_view()),
    path('answerchoice_list/',views.AnswerChoiceList.as_view()),
    path('addcorrectanswer/',views.AddCorrectAnswer.as_view()),
    path('correctanswerlist/',views.CorrectAnswerList.as_view()),
    path('delete_correctanswer/<str:id>',views.delete_correctanswer,name='delete_correctanswer'),
    path('load/', views.load_subjects.as_view(), name='load'),
    path('subjectload/', views.subjectload.as_view(), name='subjectload'),
    path('questions/',views.questions.as_view()),
    path('',views.quizpage.as_view(),name='main_page'),
    path('quiz_section/',views.teacher_quiz.as_view(),name='quiz_section'),
    path('conduct_quiz/',views.conduct_quiz().as_view(),name='conduct_quiz'),
    path('endresult/',views.result,name='endresult'),
    path('result/',views.user_result().as_view(),name='result'),
    path('timer/',views.timer,name='timer'),
    path('add_school/',views.add_school.as_view(),name='add_school'),
    path('update_school/<str:id>',views.particular_school_update,name='particular_school_update'),
    path('delete_school/<str:id>',views.delete_school,name='delete_school'),
    path('schools_list/',views.all_school.as_view(),name='all_school'),







    
]