from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .forms import SingUpForm, LoginForm, ProfileForm
from .models import BookModel, ProfileDataModel, UserPurchaseHistoryModel
from django.shortcuts import render, redirect


def sing_up_view(request):
    if request.user.is_authenticated:
        if request.user.is_staff:
            return redirect('admin:index')
        else:
            return redirect('book_store_app:client_index')

    if request.method == 'POST':
        form = SingUpForm(request.POST)
        if form.is_valid():
            new_user = User.objects.create_user(form.cleaned_data['username'], form.cleaned_data['email'],
                                                form.cleaned_data['password'])
            ProfileDataModel.objects.create(user_id=new_user.id)
            return redirect('book_store_app:login')

    form = SingUpForm()
    return render(request, 'book_store_app/sing_up.html', {'form': form})


def login_view(request):
    if request.user.is_authenticated:
        if request.user.is_staff:
            return redirect('admin:index')
        else:
            return redirect('book_store_app:client_index')

    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(request, username=form.cleaned_data['username'],
                                password=form.cleaned_data['password'])
            if user is not None:
                login(request, user)
                return redirect('book_store_app:client_index')

    form = LoginForm()
    return render(request, 'book_store_app/login.html', {'form': form})


@login_required(login_url='book_store_app:login')
def client_index_view(request):
    if request.user.is_staff:
        return redirect('admin:index')
    books = BookModel.objects.all()
    book_coins = request.user.profiledatamodel.book_coins
    return render(request, 'book_store_app/client_index.html', {'books': books, 'book_coins': book_coins})


@login_required(login_url='book_store_app:login')
def client_profile_view(request):
    if request.user.is_staff:
        return redirect('admin:index')

    if request.method == 'POST':
        form = ProfileForm(request.POST)
        if form.is_valid():
            request.user.first_name = form.cleaned_data['first_name']
            request.user.last_name = form.cleaned_data['last_name']
            request.user.save()

            request.user.profiledatamodel.country = form.cleaned_data['country']
            request.user.profiledatamodel.city = form.cleaned_data['city']
            request.user.profiledatamodel.address = form.cleaned_data['address']
            request.user.profiledatamodel.zip_or_postal_code = form.cleaned_data['zip_or_postal_code']
            request.user.profiledatamodel.phone = form.cleaned_data['phone']
            request.user.profiledatamodel.save()

            return render(request, 'book_store_app/client_profile.html', {'profile_form': form})

    user_profile_data = {'first_name': request.user.first_name,
                         'last_name': request.user.last_name,
                         'country': request.user.profiledatamodel.country,
                         'city': request.user.profiledatamodel.city,
                         'address': request.user.profiledatamodel.address,
                         'zip_or_postal_code': request.user.profiledatamodel.zip_or_postal_code,
                         'phone': request.user.profiledatamodel.phone}
    profile_form = ProfileForm(user_profile_data)

    return render(request, 'book_store_app/client_profile.html', {'profile_form': profile_form})


@login_required(login_url='book_store_app:login')
def client_purchases_history_view(request):
    if request.user.is_staff:
        return redirect('admin:index')
    if (request.user.first_name is None or
            request.user.last_name is None or
            request.user.profiledatamodel.city is None or
            request.user.profiledatamodel.address is None or
            request.user.profiledatamodel.phone is None or
            request.user.profiledatamodel.zip_or_postal_code is None or
            request.user.profiledatamodel.country is None):
        return redirect('book_store_app:client_profile')

    status = ''
    if request.method == 'POST':
        book = BookModel.objects.get(pk=request.POST['book_id'])
        book_qty_asked = float(request.POST['book_qty'])
        total_price = book_qty_asked * book.price
        if book.stock >= book_qty_asked and request.user.profiledatamodel.book_coins >= total_price:
            new_purchase = UserPurchaseHistoryModel.objects.create(user_id=request.user.id)
            new_purchase.book = book
            new_purchase.save()

            new_purchase.price = total_price
            new_purchase.qty = book_qty_asked
            new_purchase.save()

            request.user.profiledatamodel.book_coins -= total_price
            request.user.profiledatamodel.save()

            book.stock -= book_qty_asked
            book.save()
            status = 'Purchase completed'
        else:
            status = 'Something went wrong'
    purchased_books = UserPurchaseHistoryModel.objects.filter(user_id=request.user.id)
    return render(request, 'book_store_app/purchase_history.html',
                  {'status': status, 'purchased_books': purchased_books})


def logout_view(request):
    logout(request)
    return redirect('book_store_app:login')


def index_view(request):
    if request.user.is_authenticated:
        if request.user.is_staff:
            return redirect('admin:index')
        else:
            return redirect('book_store_app:client_index')
    return render(request, 'book_store_app/index.html')
