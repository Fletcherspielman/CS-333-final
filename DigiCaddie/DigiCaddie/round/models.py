from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

class Course(models.Model):
    course_id = models.IntegerField(primary_key = True)
    course_name = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    gps_cords_lat = models.FloatField(default= -119.4856)
    gps_cords_long = models.FloatField(default= 39.3247)

class HoleDetail(models.Model):
    hole_id = models.IntegerField(primary_key = True)
    course_id = models.ForeignKey(Course, on_delete=models.CASCADE)
    hole_number = models.IntegerField()
    par_number = models.IntegerField()
    yardage = models.IntegerField()
    handicap = models.IntegerField()

class Score(models.Model):
    player = models.ForeignKey(User, on_delete=models.CASCADE)
    course_id = models.ForeignKey(Course, on_delete=models.CASCADE)
    datetime_played = models.DateTimeField(default=timezone.now)
    favorite = models.BooleanField(default=False)
    hole_1 = models.IntegerField(default=0)
    hole_2 = models.IntegerField(default=0)
    hole_3 = models.IntegerField(default=0)
    hole_4 = models.IntegerField(default=0)
    hole_5 = models.IntegerField(default=0)
    hole_6 = models.IntegerField(default=0)
    hole_7 = models.IntegerField(default=0)
    hole_8 = models.IntegerField(default=0)
    hole_9 = models.IntegerField(default=0)
    total_9 = models.IntegerField(default=0)
    hole_10 = models.IntegerField(default=0)
    hole_11 = models.IntegerField(default=0)
    hole_12 = models.IntegerField(default=0)
    hole_13 = models.IntegerField(default=0)
    hole_14 = models.IntegerField(default=0)
    hole_15 = models.IntegerField(default=0)
    hole_16 = models.IntegerField(default=0)
    hole_17 = models.IntegerField(default=0)
    hole_18 = models.IntegerField(default=0)
    round_total = models.IntegerField(default=0)

    def save(self, *args, **kwargs):
        total_sum = sum(
            getattr(self, f"hole_{i}")
            for i in range(1, 19)
        )
        self.round_total = total_sum
        super().save(*args, **kwargs)

class Tip(models.Model):
    tip_id = models.IntegerField(primary_key = True)
    player = models.ForeignKey(User, on_delete=models.CASCADE)
    hole_id = models.ForeignKey(HoleDetail, on_delete=models.CASCADE)
    header = models.CharField(max_length = 255)
    body = models.TextField()
    gps_cords_lat = models.FloatField(default= -119.4856)
    gps_cords_long = models.FloatField(default= 39.3247)
    icon = models.TextField(default= 'golf')