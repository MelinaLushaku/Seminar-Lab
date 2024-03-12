from django.shortcuts import render, redirect
from .models import Book, Profile, WishList
from django.core.paginator import Paginator
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.shortcuts import render, redirect
from .models import Category
from .categoriesform import CategoryForm

from Books.recommender_engine import Recommender

def index(request):
    books = Book.objects.all()
    
    user = User.objects.get(username=request.user.username)
    profile = Profile.objects.get(user=user)
    wish_list = WishList.objects.get(user=profile)
    
    page_size = request.GET.get("page_size")
    page_size = int(page_size) if page_size is not None else 10
    if (page_size == 0):
        page_size = len(books)
    paginator = Paginator(books.order_by("created_on"), page_size)
    
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    context = {
        "page_obj": page_obj,
        "page_size": page_size,
        "wishList_id": wish_list.id,
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

def user_profile(request):
    user = User.objects.get(username=request.user.username)
    profile = Profile.objects.get(user=user)
    return render(request, 'profile.html', {
        "profile": profile,
    })

def wish_list(request):
    user = User.objects.get(username=request.user.username)
    profile = Profile.objects.get(user=user)
    wish_list = WishList.objects.get(user=profile)
    books = Book.objects.filter(wishList = wish_list.id)
    return render(request, 'wishList.html', {
        "saved_books": books,
    })

def add_book(request):
    return render(request, 'addBook.html', {})

def login_user(request):
    if (request.method == 'POST'):
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user=user)
    return redirect('/')


def register_user(request):
    if (request.method == 'POST'):
        firstname = request.POST['firstname']
        lastname = request.POST['lastname']
        email = request.POST['email']
        username = request.POST['username']
        password = request.POST['password']

        user = User.objects.create_user(
            username,
            email,
            password,
            first_name = firstname,
            last_name=lastname,
        )

        user.save()

        # Custom profile for user
        profile = Profile.objects.create(firstName = firstname, lastName= lastname, user=user)
        profile.save()

        # Only one wish list per User
        wishlist = WishList.objects.create(user=profile)
        wishlist.save()
        if user is not None:
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user=user)
    return redirect('/')

def logout_user(request):
    logout(request)
    return redirect('/')

def manage_categories(request):
    categories = Category.objects.all()

    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('manage_categories')
    else:
        form = CategoryForm()

    return render(request, 'manage_categories.html', {'form': form, 'categories': categories})

def save_book_to_wishlist(request, id):
    book = Book.objects.get(id=id)
    user = User.objects.get(username=request.user.username)
    profile = Profile.objects.get(user=user)
    wish_list = WishList.objects.get(user=profile)
    book.wishList = wish_list
    book.save()
    return redirect('/')

def remove_book_to_wishlist(request, id):
    book = Book.objects.get(id=id)
    book.wishList = None
    book.save()
    return redirect('/wish-list')