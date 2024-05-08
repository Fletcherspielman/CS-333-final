from django import forms
from .models import userpost, user_information, comments_post, comments_replies
from django.forms import TextInput, FileInput, Textarea, PasswordInput
from django.contrib.auth.models import User

class image_fourms(forms.ModelForm):
    class Meta:
        model = userpost
        fields = ["caption", "picture"]
        field_order  = ['caption', 'picture']
        labels = {
            'caption': '',
            'picture': '',
        }
        widgets = {
        'caption' : Textarea(attrs={
            'placeholder': 'Caption', 
            'style': 'width: 100%;', 
            'class': 'form-control bg-transparent text-white border-0 shadow-none',
            'rows': '2',
            }),
        'picture' : FileInput(attrs={
            'style': 'width: 100%;',
            'class': 'form-control  bg-transparent text-white border-0 shadow-none',
            }),
        }

class user_profile_pic_form(forms.ModelForm):
    class Meta:
        model = user_information
        fields = {"user_profile_picture"}
        labels = {
            'user_profile_picture': '',
        }
        widgets = {
        'user_profile_picture' : FileInput(attrs={
            'style': 'width: 100%;',
            'class': 'form-control',
            }),
        }

class comment_form_post(forms.ModelForm):
    class Meta:
        model = comments_post
        fields = {"text"}
        labels = {
            "text": ""
        }
        widgets = {
        'text' : forms.HiddenInput()
        }

class comment_form_reply(forms.ModelForm):
    class Meta:
        model = comments_replies
        fields = {"text"}
        labels = {
            "text": ""
        }
        widgets = {
        'text' : forms.HiddenInput()
        }


class update_profile(forms.Form):
    firstname = forms.CharField(label='firstname', max_length=20, min_length=1, required=False)
    lastname = forms.CharField(label='lastname', max_length=20, min_length=1, required=False)
    email = forms.EmailField(label="email", max_length=50, min_length=3, required=False)

class update_security(forms.Form):
    current_password = forms.CharField(label='current_password', max_length=20)
    new_password = forms.CharField(label='new_password', max_length=20)
    confirm_new_password = forms.CharField(label="confirm_new_password", max_length=50)
    

