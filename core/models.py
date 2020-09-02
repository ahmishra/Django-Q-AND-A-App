from django.db import models
from django.contrib.auth import get_user_model
import misaka
from django.urls import reverse

# Create your models here.
User = get_user_model()


class Question(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=256)
    date = models.DateTimeField(auto_now=True)
    question = models.TextField()
    question_html = models.TextField(editable=False, default='', blank=True)
    related_tag = models.CharField(
        max_length=256, null=True, blank=True, default='No Related Tag')

    def save(self, *args, **kargs):
        self.question_html = misaka.html(self.question)
        super().save(*args, *kargs)

    def __str__(self):
        return str(self.title)

    def get_absolute_url(self):
        return reverse('core:all-questions')

    class Meta:
        ordering = ['-date']


class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now=True)
    answer = models.TextField()
    answer_html = models.TextField(editable=False, default='', blank=True)

    def __str__(self):
        return str(self.answer)



    def get_absolute_url(self):
        return reverse('core:all-questions')
