import datetime

from django.test import TestCase
from django.utils import timezone

from .models import Question


class QuestionModelTests(TestCase):

    def test_was_published_recently_with_future_question(self):
        """
        was_published_recently() returns False for questions whose pub_date
        is in the future.
        """
        time = timezone.now() + datetime.timedelta(days=30)
        future_question = Question(pub_date=time)
        self.assertIs(future_question.was_published_recently(), False)

    def test_was_published_recently_with_old_question(self):
        """
        was_published_recently() returns False for questions whose pub_date
        is older than 1 day.
        """
        time = timezone.now() - datetime.timedelta(days=1, seconds=1)
        old_question = Question(pub_date=time)
        self.assertIs(old_question.was_published_recently(), False)

    def test_was_published_recently(self):
        # Create an Question with a publication date in the past
        past_Question = Question.objects.create(pub_date=timezone.now() - datetime.timedelta(days=2))
        self.assertFalse(past_Question.was_published_recently())
        
        # Create an Question with a publication date in the future
        future_Question = Question.objects.create(pub_date=timezone.now() + datetime.timedelta(days=2))
        self.assertFalse(future_Question.was_published_recently())
        
        # Create an Question with a publication date within the last day
        recent_Question = Question.objects.create(pub_date=timezone.now() - datetime.timedelta(hours=12))
        self.assertTrue(recent_Question.was_published_recently())