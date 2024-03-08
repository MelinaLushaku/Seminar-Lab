from django.shortcuts import render, redirect
from .models import Book
from django.core.paginator import Paginator
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

from Books.recommender_engine import Recommender

def index(request):
    books = Book.objects.all()
    page_size = request.GET.get("page_size")
    page_size = int(page_size) if page_size is not None else 10
    if (page_size == 0):
        page_size = len(books)
    paginator = Paginator(books.order_by("created_on"), page_size)
    
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    context = {
        "page_obj": page_obj,
        "page_size": page_size
    }
    return render(request, template_name='index.html', context=context)

def book_details(request, id):
    book = Book.objects.get(id=id)
    print(book.title)
    recommender = Recommender()
    recommendedBooks = recommender.getRecommendedBooks(book.title)
    return render(request, 'book.html', context={
        "book": book,
        "recommendedBooks": recommendedBooks
    })

def login_user(request):
    if (request.method == 'POST'):
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)
        print(user)
        if user is not None:
            # A backend authenticated the credentials
            login(request, user=user)
    return redirect('/')

def logout_user(request):
    logout(request)
    return redirect('/')