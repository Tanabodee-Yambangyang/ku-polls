import datetime

from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


class Question(models.Model):
    """
    A model used to create poll questions.

    Attributes:
        question_text (string): String representing the question

        pub_date (Datetime): datetime object that
        represents the question's published date.

        end_date (DateTime): datetime object represents
        the end date of the question.
    """
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')
    end_date = models.DateTimeField("end date", null=True)

    def __str__(self):
        """String representing the question"""
        return self.question_text

    def was_published_recently(self):
        """Check if the question was published recently.

        Returns:
            The return value. True if yes, False otherwise.
        """
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now

    def is_published(self):
        """Check if the question is published or not.

        Returns:
            The return value. True if the question is published,
            False otherwise.
        """
        now = timezone.now()

        if self.pub_date > now:
            return False
        return self.pub_date <= now

    def can_vote(self):
        """Check if the current time is within the
        publish date and the end date. If so,
        visitors can vote on the question.

        Returns:
            True if the current time is within the
            publish date and the end date, False otherwise.
        """
        now = timezone.now()

        if not self.is_published():
            return False
        if not self.end_date:
            return True
        return self.pub_date <= now <= self.end_date


class Choice(models.Model):
    """
    A model used to create choices for each question.

    Attributes:
        question (Question): A Question
        choice_text (string): String representing choices of each question
        votes (int): Number of choices in each question
    """
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)

    @property
    def votes(self):
        return Vote.objects.filter(choice=self).count()

    def __str__(self):
        """String representing the choices"""
        return self.choice_text


class Vote(models.Model):
    user = models.ForeignKey(User,
                             on_delete=models.CASCADE)
    choice = models.ForeignKey(Choice, on_delete=models.CASCADE)

    def __str__(self):
        return f"User {self.user.username} has " \
               f"already voted {self.choice.choice_text}."
