import datetime
from django.test import TestCase
from .models import Question
from django.utils import timezone
from django.urls import reverse

# Create your tests here.
class QuestionModelTests(TestCase):
    
    def test_was_published_recent_with_future_question(self):
        """
        was_published_recent() returns false for questions whose pub_date is in the future.
        """
        time = timezone.now() + datetime.timedelta(days=30)
        future_question = Question(pub_date = time)
        self.assertIs(future_question.was_published_recent(), False)
        
        
    def test_was_published_recent_with_old_question(self):
        """
        was_published_recent returns false for question with pub_dates older than a day.
        """
        past = timezone.now() - datetime.timedelta(days=1, seconds=1)
        old_question = Question(pub_date=past)
        self.assertIs(old_question.was_published_recent(), False)
    
    
    def test_was_published_recent_with_recent_question(self):
        """was_published_recent returns True for questions published less than a day. """
        time = timezone.now() - datetime.timedelta(hours=23, minutes=59, seconds=59)
        recent_question = Question(pub_date=time)
        self.assertIs(recent_question.was_published_recent(), True)
        


def create_question(question_text, days):
    """
    Create a question with the given `question_text` and published the
    given number of `days` offset to now (negative for questions published
    in the past, positive for questions that have yet to be published).
    """ 
    date = timezone.now() + datetime.timedelta(days=days)
    question = Question.objects.create(question_text=question_text, pub_date=date)
    return question



class QuestionIndexViewTests(TestCase):
    
    def test_no_questions(self):
        '''If no question exists, an appropriate message is displayed'''
        response = self.client.get(reverse('polls:index'))
        self.assertEqual(response.status_code, 200)
        # self.assertContains(response, 'No polls available')
        self.assertQuerysetEqual(response.context['latest_question_list'], [])
        
        
    def test_past_question(self):
        '''Questions with publication dates in the past are displayed on the index page'''
        create_question(question_text="Past Question.", days=-30)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(response.context['latest_question_list'], ['<Question: Past Question.>'])
        
        
    def test_future_question(self):
        '''Questions with publication dates in the future are not on the index page'''
        create_question(question_text="Future Question", days=30)
        response = self.client.get(reverse('polls:index'))
        # self.assertContains(response, 'No polls available')
        self.assertQuerysetEqual(response.context['latest_question_list'], [])
        
    def test_future_and_past_questions(self):
        '''Even if both future and past questions exist, only past questions are displayed'''
        create_question(question_text="Past Question", days = -30)
        create_question(question_text="Future Question", days=30)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(response.context['latest_question_list'], ['<Question: Past Question>'])
        
    def test_two_past_questions(self):
        create_question(question_text="First one", days=-20)
        create_question(question_text="Second one", days=-10)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(response.context['latest_question_list'], ['<Question: Second one>', '<Question: First one>'])
        
        
class QuestionDetailViewTests(TestCase):
    
    def test_future_question(self):
        """
        The detail view of a question with a pub_date in the future
        returns a 404 not found.
        """
        future_question = create_question(question_text="Future Question", days=2)
        response = self.client.get(reverse('polls:detail', args = (future_question.id,)))
        self.assertEqual(response.status_code, 404)
        
        
    def test_past_question(self):
        past_question = create_question(question_text="Past Question", days=-2)
        response = self.client.get(reverse('polls:detail', args=(past_question.id,)))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, past_question.question_text)