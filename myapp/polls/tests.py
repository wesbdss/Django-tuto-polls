from django.test import TestCase, Client

import datetime
from django.utils import timezone

from .models import Question

from django.urls import reverse


# Create your tests here.

def create_question(question_text, days):
    """
    Cria uma questão e passa question_text e publica com o numero de didas dado a partir de agora
    """
    time = timezone.now() + datetime.timedelta(days=days)
    return Question.objects.create(question_text=question_text,pub_date=time)
class QuestionDetailViewTests(TestCase):
    client = Client()
    def test_future_question(self):
        """
            retorna a view detail com as questions com futuro retorna 404
        """
        future_question = create_question(question_text = 'Future question.', days=5)
        url = reverse('polls:detail', args= (future_question.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_past_question(self):
        """
            Os view detail mostra as questões que estão no passado
        """

        past_question = create_question(question_text = "Past Question.", days=-5)
        url = reverse('polls:detail', args=(past_question.id,))
        response = self.client.get(url)
        self.assertContains(response, past_question.question_text)

class QuestionIndexViewTests(TestCase):
    client = Client()
    def test_no_querions(self):
        """
        Se a mensagem apropriada é emitida caso não tenha questões
        """
        response = self.client.get(reverse('polls:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No polls are available")
        
        self.assertQuerysetEqual(response.context['latest_question_list'],[])

    def test_past_question(self):
        """
            QUestões com a pub_date no passado é mostrado na index page
        """
        question = create_question(question_text="Questão do Passado", days =-30)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(response.context['latest_question_list'], [question])


    def test_future_question(self):
        """
        Questões com o pub_date no futuro não são mostradas na index pages
        """
        create_question(question_text="Future Question", days=30)
        response = self.client.get(reverse('polls:index'))
        print(response)

        self.assertContains(response, "No polls are available")
        self.assertQuerysetEqual(response.context['latest_question_list'], [])

    def test_future_question_and_past_question(self):
        """
        Sempre que tiver uma questão do passado e do futuro, apenas as do passado são mostradas
        """
        question = create_question(question_text="Questão do passado", days=-30)
        create_question(question_text="Questão do Futuro", days=30)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(response.context['latest_question_list'], [question])

    def test_two_past_questions(self):
        """
         As questions da index page vai mostrar multiplas questões
        """

        question1 = create_question(question_text="Questão do passado 1", days=-30)
        question2 = create_question(question_text="Questão do passado 2", days= -5)
        response= self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(response.context['latest_question_list'], [question2, question1])
class QuestionModelTests(TestCase):
    def test_was_published_recently_with_future_question(self):
        """ was_published_recently() """
        time = timezone.now() + datetime.timedelta(days=30)
        future_question = Question(pub_date=time)
        self.assertIs(future_question.was_published_recently(), False)
    
    def test_was_published_recently_with_old_question(self):
        """
            was_published_reccently usando uma questão com mais de 1 dia
        """
        time = timezone.now() - datetime.timedelta(days=1, seconds= 1)
        old_question = Question(pub_date=time)
        self.assertIs(old_question.was_published_recently(), False)
    
    def test_was_published_recently_with_recent_question(self):
        """
            was_published_reccently usando com menos de um dia
        """
        time = timezone.now() - datetime.timedelta(hours=23, minutes=59,seconds=59)
        recent_question = Question(pub_date=time)
        self.assertIs(recent_question.was_published_recently(), True)
