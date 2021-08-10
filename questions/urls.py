from django.urls import path
from . import views

urlpatterns = [
    path('questions/<int:id>', views.test_questions)
]