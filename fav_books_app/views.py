from django.shortcuts import render, HttpResponse, redirect
from .models import User, Book
from .forms import RegisterForm, LoginForm
from django.contrib import messages

# Create your views here.
def index(request): #used to be register
    myForm = RegisterForm()
    loginForm = LoginForm()
    context = {
        'myform': myForm,
        'loginform': loginForm
    }
    return render(request, 'index.html', context)

def register(request):
    if request.method =='GET':
        return redirect('/')
        #validation
    errors = User.objects.validate(request.POST)
    if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect('/')
    else:
        new_user = User.objects.register(request.POST) # moved to register in models(first_name = request.POST['first_name'], last_name = request.POST['last_name'], bday = request.POST['bday'], email = request.POST['email'], pw = request.POST['password'])
        request.session['user_id'] = new_user.id
        messages.success(request, 'you have successfully registered!')
    return redirect('/books')

def login(request):
    if request.method=='GET':
        return redirect('/')
    if not User.objects.authenticate(request.POST['email'], request.POST['password']):
        messages.error(request, 'Invalid email/password')
        return redirect('/')
    user = User.objects.get(email = request.POST['email'])
    request.session['user_id'] = user.id
    messages.success(request, "You have successfully logged in!")
    return redirect('/books')

def logout(request):
    # clear session
    request.session.clear()
    return redirect('/')

def books(request):
    if 'user_id' not in request.session:
        return redirect('/')
    user = User.objects.get(id = request.session['user_id']) #creates a variable 'user' to access user_id through session, then passes into context
    context = {
        'user': user,
        'books': Book.objects.all()
    }
    return render(request, 'books.html', context)

def edit_book(request, book_id):
    favedBook = Book.objects.filter()
    context = {
        'book': Book.objects.get(id = book_id),
        'current_user': User.objects.get(id = request.session['user_id']),
    }
    return render(request, 'edit.html', context)

def book_update(request, book_id):
    update_book = Book.objects.get(id = book_id)
    update_book.description = request.POST['description']
    update_book.save()
    return redirect('/books')

def other_books(request, id):
    return HttpResponse(f'This worked for {{book_id}}other_books')

def create_book(request, user_id):
    if request.method =='GET':
        return redirect('/')
        #validation
    errors = Book.objects.bookValidate(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/books')
    else:
        user = User.objects.get(id = user_id)
        bookVar = Book.objects.create(title = request.POST['title'], description = request.POST['description'], uploaded_by = user)
        user.liked_books.add(bookVar)
        messages.success(request, 'you have successfully created a book!')
    return redirect('/books')

def delete_book(request, book_id):
    bye_book = Book.objects.get(id = book_id)
    bye_book.delete()
    return redirect('/books')

def favorite(request, user_id, book_id):
    userFav = User.objects.get(id = request.session['user_id'])
    bookFaved = Book.objects.get(id = book_id)
    userFav.liked_books.add(bookFaved)
    return redirect('/books/{{book_id}}')

