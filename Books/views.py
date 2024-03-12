from django.shortcuts import render, redirect
from .models import Book, Profile
from django.core.paginator import Paginator
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.shortcuts import render, redirect
from .models import Category
from .categoriesform import CategoryForm
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import redirect, HttpResponse

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

def user_profile(request, id):
    profile = Profile.objects.get(user=id)
    return render(request, 'profile.html', {
        "profile": profile,
    })

def wish_list(request):
    return render(request, 'wishList.html', {})

def add_book(request):
    return render(request, 'addBook.html', {})

def login_user(request):
    if (request.method == 'POST'):
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)
        print(user)
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
        profile = Profile.objects.create(firstName = firstname, lastName= lastname, user=user)
        profile.save()
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

    # Pagination logic
    paginator = Paginator(categories, 5)  # 10 categories per page
    page_number = request.GET.get('page')
    try:
        categories = paginator.page(page_number)
    except PageNotAnInteger:
        categories = paginator.page(1)
    except EmptyPage:
        categories = paginator.page(paginator.num_pages)

    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()  # Save the form data as a new Category instance
            return render(request, 'manage_categories.html', {'form': form, 'categories': categories})
    else:
        form = CategoryForm()

    return render(request, 'manage_categories.html', {'form': form, 'categories': categories})

def delete_category(request):
    if request.method == 'POST':
        category_id = request.POST.get('category')
        try:
            category = Category.objects.get(id=category_id)
            category.delete()
            return redirect('manage_categories')
        except Category.DoesNotExist:
            return HttpResponse("Category does not exist.", status=404)
    return HttpResponse("Invalid request method.", status=400)
