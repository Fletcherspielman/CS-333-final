
from django import forms
from .models import userpost
from django.contrib.auth.models import User
from django.utils.timezone import localtime
from django.shortcuts import render

class image_fourms(forms.ModelForm):
    model = userpost
    fields = {"pictire", "caption"}



def upload_image(request):
    if request.method == 'POST':
        form = image_fourms(request.POST, request.FILES)
        if form.is_valid():
            test = form.save(commit=False) # we need to add data for the class or an error will occur 
            test.author = request.user
            test.caption = form.cleaned_data["caption"]
            test.rating = 0 
            test.save() # save the data
            return render(request, "main_page/mainpage.html")
    else:
        form = image_fourms()
        return render(request, "main_page/mainpage.html", {"form": form})

    


