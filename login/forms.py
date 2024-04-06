from django import forms

class login_form(forms.Form):
    username = forms.CharField(max_length=20, label= "", widget=forms.TextInput(attrs={            
            'placeholder': 'Username', 
            'style': 'width: 100%;', 
            'class': 'form-control bg-dark text-white',}), 
            required=False)
    password = forms.CharField(label= "", widget=forms.PasswordInput(attrs={            
            'placeholder': 'Password', 
            'style': 'width: 100%;', 
            'class': 'form-control bg-dark text-white',}), 
            required=False)


# user creation form
class reg_form(forms.Form):
    firstname = forms.CharField(max_length=20, label= "", widget=forms.TextInput(attrs={            
            'placeholder': 'First Name', 
            'style': 'width: 100%;', 
            'class': 'form-control bg-dark text-white',}), 
            required=False)  
    lastname = forms.CharField(max_length=20, label= "", widget=forms.TextInput(attrs={            
            'placeholder': 'Last Name', 
            'style': 'width: 100%;', 
            'class': 'form-control bg-dark text-white',}), 
            required=False)
    username = forms.CharField(max_length=20, label= "", widget=forms.TextInput(attrs={            
            'placeholder': 'Username', 
            'style': 'width: 100%;', 
            'class': 'form-control bg-dark text-white',}), 
            required=False)
    email = forms.EmailField(label= "", widget=forms.EmailInput(attrs={            
            'placeholder': 'Email', 
            'style': 'width: 100%;', 
            'class': 'form-control bg-dark text-white',}), 
            required=False)
    password = forms.CharField(label= "", widget=forms.PasswordInput(attrs={            
            'placeholder': 'Password', 
            'style': 'width: 100%;', 
            'class': 'form-control bg-dark text-white',}), 
            required=False)
    confirm_password = forms.CharField(label= "", widget=forms.PasswordInput(attrs={            
            'placeholder': 'Confirm password', 
            'style': 'width: 100%;', 
            'class': 'form-control bg-dark text-white',}), 
            required=False)
