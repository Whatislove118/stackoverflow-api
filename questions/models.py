from datetime import datetime


from django.db import models


# Create your models here.
from users.models import User


class TopQuestionsManager(models.Manager):
    def get_queryset(self):
        return super(TopQuestionsManager, self).get_queryset().order_by('-views')

    def all(self):
        return self.get_queryset().filter(views__gt=1)


class Question(models.Model):
    title = models.CharField(max_length=50, blank=False)
    description = models.TextField(blank=False)
    date_created = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, blank=True, null=True, on_delete=models.CASCADE)
    views = models.IntegerField(default=1)
    objects = models.Manager()
    top_objects = TopQuestionsManager()

    def __str__(self):
        return self.title


class Comment(models.Model):
    description = models.TextField(blank=False)
    user = models.ForeignKey(User, blank=True, null=True, on_delete=models.DO_NOTHING)
    like = models.IntegerField(default=0)
    is_useful = models.BooleanField(default=False)
    question = models.OneToOneField(Question, blank=True, null=True, on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.description
