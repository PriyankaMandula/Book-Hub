from django.contrib.auth.models import User
from django.core.mail.message import EmailMessage
from django.shortcuts import render, redirect
from . import models
from .models import Book

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.db.models import Q
from .forms import newUserForm
from django.contrib.auth.forms import UserCreationForm
from django.views.generic.list import ListView

from django.views.generic import TemplateView, ListView, CreateView
from django.core.files.storage import FileSystemStorage
from django.urls import reverse_lazy

from .forms import BookForm
from .models import Book
from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse

from django.contrib import messages
from django.views.generic.edit import FormView

from .forms import ContactForm
from .models import Message


# Create your views here.

def home(request):
	return render(request,'accounts/opening.html')


def mainpage(request):
    books = Book.objects.all()
    return render(request, 'accounts/mainpage.html', {
        'books': books
    })
    
	#return render(request,'accounts/mainpage.html')

def register(request):
    form = newUserForm()
    if request.method == 'POST':
        form = newUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            customer = models.Customer.objects.create(
                user=user,
                email=form.cleaned_data['email'],
                name=form.cleaned_data['username']
            )
            customer.save()
            return redirect('login')

    context = {'form': form}
    return render(request, 'accounts/register.html', context)

			

def login_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request,user)
            return redirect('mainpage')
        else:
            messages.info(request, 'Please enter valid details:')

    return render(request, 'accounts/login.html')

def logout_user(request):
    logout(request)
    return redirect('home')



def upload_book(request):
    form = BookForm()
    if request.method == 'POST':
        form = BookForm(request.POST, request.FILES)
        print("hello")
        if form.is_valid():
            form.save()
            #return redirect('book_list')
            return redirect('mainpage')

    else:
        form = BookForm()
        return render(request, 'accounts/uploadbook.html', {
        'form': form
    })

def delete_book(request, pk):
    if request.method == 'POST':
        book = Book.objects.get(pk=pk)
        book.delete()
    #return redirect('book_list')
    return redirect('mainpage')


#def searchbar(request):
#   if request.method == 'GET':
#       search = request.GET.get('search')
#       post = Book.objects.all().filter(title=search)
#       return render(request,'accounts/searchbar.html',{'post':post})



def searchbar(request):
    if request.method=='GET':
       search = request.GET.get('search')
       post_title = Book.objects.all().filter(title__contains=search)
       post_desc = Book.objects.all().filter(author__contains=search)
       search_result = post_title.union(post_desc)
       #param = {'query':query, 'search_result':search_result}
       return render(request, 'accounts/searchbar.html', {'search_result':search_result})
       

class ContactFormView(FormView):
    template_name = 'contact_form/contact.html'
    form_class = ContactForm
    success_url = '/contact'    

    def form_valid(self, form):
        email = form.cleaned_data['email']
        message = form.cleaned_data['message']

        message = Message(email=email, message=message)
        message.save()
        
        messages.success(self.request, 'Message received 👽')
        
        return super().form_valid(form)
