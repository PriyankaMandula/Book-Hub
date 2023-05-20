from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Book
from django import forms

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Field

# Create your forms here.

class newUserForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ("username", "email", "password1","password2")

    def save(self, commit=True):
        user = super(newUserForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user

class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ('title','author','pdf')



class ContactForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super(ContactForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()

        self.helper.form_method = 'post'
        self.helper.form_action = '/contact'

        self.helper.add_input(Submit('submit', 'Submit'))
        
    email = forms.EmailField(max_length=254)
    message = forms.CharField(max_length=254, widget=forms.Textarea)
