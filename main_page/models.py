from django.db import models
from django.contrib.auth.models import User
from django.utils.html import mark_safe
from django.utils.timezone import localtime
from django.core.validators import validate_image_file_extension
from django.core.exceptions import ValidationError
from PIL import Image
import pathlib

# save pictures to folder with user designation
def picture_upload_location(instance, filename):
    file_ext = pathlib.Path(filename).suffix
    filename = "{0}{1}.{2}".format(instance.author, localtime(),str(file_ext))
    return "user_{0}/{1}".format(instance.author, filename)

def file_user_picture_location(instance, filename):
    file_ext = pathlib.Path(filename).suffix
    filename = "{0}{1}.{2}".format(instance.user, "pf_pic",str(file_ext))
    return "user_{0}/{1}".format(instance.user, filename)

def image_validation(image):
    max_width = 5000
    max_height = 4000
    img = Image.open(image)
    if img.width > max_width or img.height > max_height or img.width < 100 or img.height < 100:
        raise ValidationError("Image should be larger than 100 by 100 pixels and should be smaller than " + str(max_width) + " by " + str(max_height))
    

class comments_replies(models.Model):
    text = models.TextField()
    author = models.ForeignKey(User, on_delete=models.PROTECT)
    likes_comment = models.ManyToManyField(User, related_name='comment_com_like', blank=True)
    created = models.DateTimeField(auto_now_add=True)
    @property
    def like_comment_total(self):
        return self.likes_comment.count()
    def __str__(self):
        return self.author.username + ": " + self.text

class comments_post(models.Model):
    text = models.TextField()
    author = models.ForeignKey(User, on_delete=models.PROTECT)
    likes_comment = models.ManyToManyField(User, related_name='comment_like', blank=True)
    created = models.DateTimeField(auto_now_add=True)
    comment_replies = models.ManyToManyField(comments_replies, related_name='comment_replies', blank=True)
    @property
    def like_comment_total(self):
        return self.likes_comment.count()
    def __str__(self):
        return self.author.username + ": " + self.text
    

# class report_main(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     post = models.ForeignKey(comments_post, on_delete=models.CASCADE, blank=True)
#     def __str__(self):
#         return self.user.username
    

class userpost(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE) # copy from auth system
    posted_date = models.DateTimeField(auto_now_add=True)
    rating = models.FloatField(default=0)
    likes = models.ManyToManyField(User, related_name='like_post', blank=True)
    caption = models.CharField(max_length=255)
    picture = models.ImageField(upload_to=picture_upload_location, validators=[validate_image_file_extension, image_validation])
    comments = models.ManyToManyField(comments_post, related_name='comments', blank=True)
    active = models.BooleanField(default=True)

    def image_view(self):
        return mark_safe(f'<img src = "{self.picture.url}" width = "300"/>')
    @property
    def like_total(self):
        return self.likes.count()
    def __str__(self):
        return self.author.username + ": " + self.caption

class report_post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(userpost, on_delete=models.CASCADE, blank=True)
    
    class Meta:
        unique_together = ('user', 'post') # user can only report a post once

    def __str__(self):
        return self.user.username

class ReportedPost(models.Model):
    post = models.ForeignKey(userpost, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.post.caption

class ReportComment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.ForeignKey(comments_post, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'comment')

    def __str__(self):
        return self.comment.text
        
class ReportedComment(models.Model):
    comment = models.ForeignKey(comments_post, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.comment.text

class user_information(models.Model):
    user = models.OneToOneField(User, related_name='profile_pic', on_delete=models.CASCADE, primary_key=True) 
    user_profile_picture = models.ImageField(upload_to=file_user_picture_location, blank=True, validators=[validate_image_file_extension], default='static/default-profile.png')
    
    def image_view(self):
        return mark_safe(f'<img src = "{self.user_profile_picture.url}" width = "300"/>')
    def __str__(self):
        return self.user.username


class user_friends(models.Model):
    user = models.OneToOneField(User, related_name='friends_user', on_delete=models.CASCADE, primary_key=True) 
    friends = models.ManyToManyField(User, related_name='friends', blank=True)
    def __str__(self):
        return self.user.username
    def friends_total(self):
        return self.friends.count()

class friend_request_model(models.Model):
    request = models.ForeignKey(User, related_name='friend_request', on_delete=models.CASCADE)
    sent = models.ForeignKey(User, related_name='friend_sent', on_delete=models.CASCADE)
    def __str__(self):
        return self.request.username + ": " + self.sent.username
    def sent_name(self):
        return self.request
    def request_name(self):
        return self.sent
    




