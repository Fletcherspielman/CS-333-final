from django.test import TestCase
from login.forms import login_form, reg_form
from django.contrib import auth
from django.contrib.auth.models import User
# Create your tests here.

class registration_form_test(TestCase):

    def test_create_user(self):
        user_info = {
                     'firstname': 'Fletcher', 
                     'lastname': 'spielman', 
                     'username': 'fletch', 
                     'email': 'test@test123.com', 
                     'password': 'test123!', 
                     'confirm_password': 'test123!'
                    }
        form = reg_form(data=user_info)
        self.assertTrue(form.is_valid())
    
    def test_login_user(self):
        login_info = {
            'username': 'fletch',
            'password': 'test123!'
        }
        form = login_form(data=login_info)
        self.assertTrue(form.is_valid())

    def test_create_user_fail_email(self):
        # bad email
        user_info = {
                     'firstname': 'Fletcher', 
                     'lastname': 'spielman', 
                     'username': 'fletch', 
                     'email': 'testtest123.com', 
                     'password': 'test123!', 
                     'confirm_password': 'test123!'
                    }
        form = reg_form(data=user_info)
        self.assertFalse(form.is_valid())

class post_view_testing(TestCase):
    def setUp(self):
        User.objects.create_user(username='fletch-test', password='test123!!')

    def test_view(self):  
        # user sign in 
        self.client.post('/', {'username': 'fletch-test', 'password': 'test123!!'})
        user = auth.get_user(self.client)
        self.assertTrue(user.is_authenticated)
        self.client.logout()


        self.client.post('/', {'username': 'fletch-test', 'password': 'test123!!!'})
        user = auth.get_user(self.client)
        self.assertFalse(user.is_authenticated)
        self.client.logout()

    def test_create_user(self):
        # check signup post
        self.client.post('/signup', {
                     'firstname': 'Fletcher', 
                     'lastname': 'spielman', 
                     'username': 'fletch', 
                     'email': 'test@test123.com', 
                     'password': 'test123!', 
                     'confirm_password': 'test123!'
                    })
        self.assertTrue(User.objects.filter(username='fletch').exists())
        self.assertFalse(User.objects.filter(username='fletcher').exists())
        # test for username is being used again
        self.client.post('/signup', {
                     'firstname': 'Fletcherremake', 
                     'lastname': 'spielman', 
                     'username': 'fletch', 
                     'email': 'test@test123.com', 
                     'password': 'test123!', 
                     'confirm_password': 'test123!'
                    })
        self.assertFalse(User.objects.filter(first_name='Fletcherremake').exists())

class test_intergration_cs333(TestCase):
    def test_signup_login(self):
        # failed login
        code = self.client.post('/', {"username": "user1", "password": "1234"})
        msg = code.context['messages']
        self.assertTrue(len(msg) == 1)
        # make account
        data = {
            "firstname": "test",
            "lastname": "testme",
            "username": "user1",
            "email": "test@test.com",
            "password": "1234",
            "confirm_password": "1234",
        }
        code = self.client.post("/signup", data)
        self.assertTrue(User.objects.filter(username="user1").exists())
        self.client.post('/', {"username": "user1", "password": "1234"})
        try:
            msg = code.context['messages']
            self.assertTrue(len(msg) == 0)
        except:
            pass
        self.assertTrue(auth.get_user(self.client))

