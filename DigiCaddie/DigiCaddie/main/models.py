from django.db import models

class userpost(models.Model):
    author = models.CharField(max_length=20)
    posted_date = models.DateField()
    rating = models.FloatField()
    caption = models.CharField(max_length=255)
    picture = models.ImageField(upload_to='pictures/')

    
