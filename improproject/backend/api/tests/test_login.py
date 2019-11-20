from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APIClient, APITestCase
from ..models import Actor
from django.contrib.auth.models import User


#Test for the Authentication
PASSWORD = 'pAssw0rd!'


def create_user(username='user@example.com', password=PASSWORD): # new
        new_user = User.objects.create_user(username=username, password=password, email="null", is_staff=False)
        actor = Actor(user=new_user)
        return new_user

class AuthenticationTest(APITestCase):
    """
    Authentication Test
    """
    def setUp(self):
        self.client = APIClient()

    def test_user_can_sign_up(self):
        response = self.client.post(('/api/register'), data={
            'username': 'user@example.com',
            'password': PASSWORD,
            'is_director': True,
        })
        user = get_user_model().objects.last()
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        self.assertEqual(response.data['user'], user.id)


    def test_user_can_log_in(self): # new
        new_user = User.objects.create_user(username='user@example.com', password=PASSWORD, email="null", is_staff=False)
        actor = Actor(user=new_user)
        actor.save()
        response = self.client.post(('/api/login'), data={
            'username': new_user.username,
            'password': PASSWORD,
        })
        self.assertEqual(status.HTTP_200_OK, response.status_code)

