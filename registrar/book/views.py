from django.shortcuts import render
from .models import Catagory, Book
# Create your views here.
def index(request):
    catagories = Catagory.objects.all()
    books = Book.objects.filter(published =True)
    return render(request, 'book/index.html', {
        'catagories' : catagories,
        'books':books,
        })