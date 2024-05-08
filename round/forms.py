from django import forms
from .models import Course, HoleDetail, Tip, Score
from django.forms import Textarea, TextInput, NumberInput

def get_all_courses(): 
    courses = Course.objects.all()
    course_options = [(course.course_id, course.course_name) for course in courses]
    return course_options

class CourseForm(forms.Form):
    course = forms.ChoiceField(choices=get_all_courses, widget=forms.Select(attrs={
            'style': 'width: 100%;', 
            'class': 'form-control',}), 
            required=False)
    
class TipsForm(forms.ModelForm):
    class Meta:
        model = Tip
        fields = {"header", "body","gps_cords_lat","gps_cords_long"}
        labels = {
            'header': '',
            'body': '',
            "gps_cords_lat": '',
            "gps_cords_long": '',
        }
        widgets = {
        'header' : TextInput(attrs={
            'placeholder': 'Header',
            'style': 'width: 100%;',
            'class': 'form-control',
            }),
        'body' : Textarea(attrs={
            'placeholder': 'Your tip', 
            'style': 'width: 100%;', 
            'class': 'form-control',
            }),
        'gps_cords_lat' : NumberInput(attrs={
            'placeholder': '', 
            'type': 'hidden',
            'id': 'coords_lng',
            "required": False
            }),
        'gps_cords_long' : NumberInput(attrs={
            'placeholder': '', 
            'type': 'hidden',
            'id': 'coords_lat',
            "required": False
            }),
        }
        field_order = ['header', 'body', 'gps_cords_lat', 'gps_cords_long']

class ScoreForm(forms.Form):
    score = forms.IntegerField(label='Score')