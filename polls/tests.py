import datetime

from django.test import TestCase
from django.utils import timezone
from django.urls import reverse
from django.contrib.auth.models import User

from .models import Question, Choice


def create_question(question_text, days):
    """
    Create a question with the given `question_text` and published the
    given number of `days` offset to now (negative for questions published
    in the past, positive for questions that have yet to be published).
    """
    time = timezone.now() + datetime.timedelta(days=days)
    return Question.objects.create(question_text=question_text, pub_date=time)


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

    def test_was_published_recently_with_recent_question(self):
        """
        was_published_recently() returns True for questions whose pub_date
        is within the last day.
        """
        time = timezone.now() - datetime.timedelta(
            hours=23, minutes=59, seconds=59)
        recent_question = Question(pub_date=time)
        self.assertIs(recent_question.was_published_recently(), True)

    def test_current_date_is_on_or_after_publishing_date(self):
        """
        is_published should return True if current date is on
        or after question’s publication date. Return False if
        current date is before question’s publication date.
        """
        now = timezone.now()
        time = datetime.timedelta(days=1, seconds=1)

        # test Question with pub_date = now
        question_1 = Question(pub_date=now)
        self.assertTrue(question_1.is_published())

        # test Question with pub_date < now
        question_2 = Question(pub_date=now - time)
        self.assertTrue(question_2.is_published())

        # test Question with pub_date > now
        question_3 = Question(pub_date=now + time)
        self.assertFalse(question_3.is_published())

    def test_published_date_is_in_future(self):
        """can_vote should return False if current
        date is before question’s publication date"""
        now = timezone.now()
        time = datetime.timedelta(days=1, seconds=1)

        question_2 = Question(pub_date=now + time)
        self.assertFalse(question_2.can_vote())

    def test_current_date_the_same_as_published_date_or_end_date(self):
        """can_vote should return True if current
        date is exactly the published date
        and False if current date is the end date.
        """
        now = timezone.now()

        question = Question(pub_date=now, end_date=now)
        self.assertTrue(question.can_vote())

    def test_current_date_is_after_end_date(self):
        """can_vote should return False if current date is after end date."""
        now = timezone.now()
        time = datetime.timedelta(days=1, seconds=1)

        question = Question(pub_date=now, end_date=now - time)
        self.assertFalse(question.can_vote())

    def test_end_date_is_null(self):
        """can_vote should return True even the poll has no end date."""
        now = timezone.now()
        question = Question(pub_date=now)

        self.assertEqual(None, question.end_date)
        self.assertTrue(question.can_vote())


class QuestionIndexViewTests(TestCase):

    def test_no_questions(self):
        """
        If no questions exist, an appropriate message is displayed.
        """
        response = self.client.get(reverse('polls:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No polls are available.")
        self.assertQuerysetEqual(response.context['latest_question_list'], [])

    def test_past_question(self):
        """
        Questions with a pub_date in the past are displayed on the
        index page.
        """
        question = create_question(question_text="Past question.", days=-30)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_question_list'], [question],
        )

    def test_future_question(self):
        """
        Questions with a pub_date in the future aren't displayed on
        the index page.
        """
        create_question(question_text="Future question.", days=30)
        response = self.client.get(reverse('polls:index'))
        self.assertContains(response, "No polls are available.")
        self.assertQuerysetEqual(response.context['latest_question_list'], [])

    def test_future_question_and_past_question(self):
        """
        Even if both past and future questions exist, only past questions
        are displayed.
        """
        question = create_question(question_text="Past question.", days=-30)
        create_question(question_text="Future question.", days=30)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            [question],
        )

    def test_two_past_questions(self):
        """
        The questions index page may display multiple questions.
        """
        question1 = create_question(question_text="Past question 1.", days=-30)
        question2 = create_question(question_text="Past question 2.", days=-5)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            [question2, question1],
        )


class QuestionDetailViewTests(TestCase):

    def test_future_question(self):
        """
        The detail view of a question with a pub_date in the future
        must redirect the page to index page.
        """
        future_question = \
            create_question(question_text='Future question.', days=5)
        url = reverse('polls:detail', args=(future_question.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)

    def test_past_question(self):
        """
        The detail view of a question with a pub_date in the past
        displays the question's text.
        """
        past_question = \
            create_question(question_text='Past Question.', days=-5)
        url = reverse('polls:detail', args=(past_question.id,))
        response = self.client.get(url)
        self.assertContains(response, past_question.question_text)


class VoteTests(TestCase):

    def setUp(self):
        """Set up elements for testing."""
        self.question1 = Question.objects.create(
            question_text="test_question", pub_date=timezone.now(),
            end_date=timezone.now() + datetime.timedelta(days=1, seconds=1))

        self.choice1 = Choice.objects.create(
            question=self.question1, choice_text="Test Choice1")
        self.choice1.save()

        self.choice2 = Choice.objects.create(
            question=self.question1, choice_text="Test Choice2")
        self.choice2.save()

        self.user = User.objects.create_user(
            username="test_user", password="test1234")
        self.user.save()

    def test_vote_when_logged_in(self):
        """Only an authenticated (logged in) user can submit a vote."""
        self.client.login(username="test_user", password="test1234")
        vote_target_url = reverse("polls:vote", args=(self.question1.id,))
        vote_data = {"choice": self.choice1.id}

        response = self.client.post(vote_target_url, data=vote_data)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse(
            "polls:results", args=(self.question1.id,)))
        self.assertEqual(self.choice1.votes, 1)

    def test_vote_without_login(self):
        """If user click vote when they are not login
        then the application will redirect them to login page."""
        vote_target_url = reverse("polls:vote", args=(self.question1.id,))
        vote_data = {"choice": self.choice1.id}

        response = self.client.post(vote_target_url, data=vote_data)

        self.assertEqual(
            response.url, f'/accounts/login/?next=/{self.choice1.id}/vote/')

    def test_vote_without_select_choice(self):
        """If user click vote without selecting any choice,
        then the error message must appear."""
        self.client.login(username="test_user", password="test1234")
        vote_target_url = reverse("polls:vote", args=(self.question1.id,))

        response = self.client.post(vote_target_url)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response,
                            text="You didn't select a choice.", html=True)

    def test_vote_change_choice(self):
        """User can change their choice any
        time and the vote should count correctly."""
        self.client.login(username="test_user", password="test1234")
        vote_target_url = reverse("polls:vote", args=(self.question1.id,))

        self.client.post(vote_target_url, data={"choice": self.choice1.id})
        self.assertEqual(self.choice1.votes, 1)
        self.assertEqual(self.choice2.votes, 0)

        self.client.post(vote_target_url, data={"choice": self.choice2.id})
        self.assertEqual(self.choice1.votes, 0)
        self.assertEqual(self.choice2.votes, 1)
