from django.contrib import admin
from .models import Book, Customer

# Register your models here.

admin.site.register(Customer)
admin.site.register(Book)

