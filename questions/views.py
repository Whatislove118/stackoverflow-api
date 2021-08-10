from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
from questions.models import Question


def test_questions(request, id):
    questions = Question.top_objects.all()
    print(questions)
    return HttpResponse('OK')
