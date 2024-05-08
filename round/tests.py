from django.test import TestCase
from django.contrib.auth.models import User
from .models import Course, HoleDetail, Score, Tip
import random
from datetime import datetime

class test_round(TestCase):
    def setUp(self):
        User.objects.create_user(
            username='fletch', password='test1234'
        )
        User.objects.create_user(
            username='test', password='test1234'
        )
        self.client.login(username='fletch', password='test1234')

    def test_connections(self):
        code = self.client.get('/round/selection/')
        self.assertEqual(code.status_code, 200)
        code = self.client.get('/round/scorecard/')
        self.assertEqual(code.status_code, 200)

    def make_course(self, id, name, city, state, coords_lat, coords_long):
        Course.objects.create(
            course_id = id,
            course_name = name,
            city = city,
            state = state,
            gps_cords_lat = coords_lat,
            gps_cords_long = coords_long,
        )
        course = Course.objects.get(course_id = id)
        self.make_fake_holes(course)

    def make_fake_holes(self, course):
        i = 0
        for x in range(18):
            HoleDetail.objects.create(
                course_id = course,
                hole_id = i,
                hole_number = i,
                par_number = 0,
                yardage = random.randrange(100, 300),
                handicap = random.randrange(1,3),
            )
            i += 1

    def test_course(self):
        self.make_course(1, "test", "Reno", "Nevada", 100, 200)
        course = Course.objects.get(course_id = 1)
        user = User.objects.get(username='fletch')
        score = Score.objects.create(
                player = user,
                course_id = Course.objects.get(course_id = 1),
                datetime_played = datetime.now()
        )
        code = self.client.get('/round/stats/1/1/1/')
        self.assertEqual(code.status_code, 200)
        data = {
           'state': 'Nevada', 
           'course': '1' 
        }
        code = self.client.post('/round/stats/1/1/1/', data)
        self.assertEqual(code.status_code, 200)

    def test_home(self):
        self.client.get('/round/stats/1/1/1/')
        
