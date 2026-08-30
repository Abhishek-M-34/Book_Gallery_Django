from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib import messages
from .models import Profile, Book, Order
from .forms import RegistrationForm, BookForm
from django.db.models import Q
from django.contrib import messages

from django.contrib.auth.decorators import login_required

# Create your views here.
def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit = False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            Profile.objects.create(
                user = user,
                address = form.cleaned_data['address'],
                phone_number = form.cleaned_data['phone_number']
            )
            messages.success(request, 'Account created successfully! Please login.')
            return redirect('login')
    else:
        form = RegistrationForm()
    return render(request, 'gallery/register.html',{'form':form})

@login_required
def home(request):
    profile = request.user.profile
    books = request.user.books.all().order_by('-created_at')
    context = {
        'profile': profile,
        'books': books,
    }
    return render(request,'gallery/home.html',context)

@login_required
def add_book(request):
    if request.method == 'POST':
        form = BookForm(request.POST)
        if form.is_valid():
            book = form.save(commit=False)
            book.seller = request.user
            book.save()
            messages.success(request, 'Book added successfully!')
            return redirect('home')
    else:
        form = BookForm()
    return render(request, 'gallery/add_book.html', {'form': form})

@login_required
def edit_book(request, book_id):
    book = get_object_or_404(Book, id=book_id, seller=request.user)
    if request.method == 'POST':
        form = BookForm(request.POST, instance=book)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = BookForm(instance=book)
    return render(request, 'gallery/edit_book.html', {'form': form, 'book': book})

@login_required
def delete_book(request, book_id):
    book = get_object_or_404(Book, id=book_id, seller=request.user)
    if request.method == 'POST':
        book.delete()
        messages.success(request, 'Book deleted successfully!')
        return redirect('home')
    return render(request, 'gallery/delete_book.html', {'book': book})

def book_feed(request):
    query = request.GET.get('q', '')
    books = Book.objects.all().order_by('-created_at')
    if query:
        books = books.filter(Q(title__icontains=query))
    return render(request,'gallery/book_feed.html',
        {
            'books': books,
            'query': query,
        }
    )

@login_required
def request_purchase(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    if book.seller == request.user:
        return redirect('book_feed')
    if request.method == 'POST':
        Order.objects.get_or_create(book=book, buyer=request.user, defaults={'status': 'Pending'})
        messages.success(request, 'Purchase request sent successfully!')
        return redirect('purchase_history')
    return render(request, 'gallery/request_purchase.html',{'book': book})

@login_required
def home(request):
    profile = request.user.profile
    books = request.user.books.all().order_by('-created_at')
    orders = Order.objects.filter(book__seller=request.user).select_related('book','buyer').order_by('-created_at')
    context = {
        'profile': profile,
        'books': books,
        'orders': orders,
    }
    return render(request, 'gallery/home.html', context)

@login_required
def update_order_status(request, order_id, status):
    order = get_object_or_404(Order, id=order_id, book__seller=request.user)
    if request.method == 'POST':
        if status == 'Approved':
            order.status = 'Approved'
            order.save()
            messages.success(request, 'Purchase request approved!')
        elif status == 'Rejected':
            order.status = 'Rejected'
            order.save()
            messages.warning(request, 'Purchase request rejected.')
    return redirect('home')

@login_required
def purchase_history(request):
    orders = Order.objects.filter(buyer=request.user).select_related('book', 'book__seller').order_by('-created_at')
    return render(request, 'gallery/purchase_history.html', {'orders': orders})

def landing_page(request):
    return render(request, 'gallery/landing.html')