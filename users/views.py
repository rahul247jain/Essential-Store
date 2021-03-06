from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.shortcuts import render, redirect
from django.urls import reverse
from .forms import SignUpForm
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import update_session_auth_hash
from orders.models import OrderItem, Order
from shop.models import Product


def signup_view(request):
    """The view that handles sign ups

    Arguments:
        request {request} -- The request

    Returns:
        render -- The sign up form or a redirect to the index
    """

    if request.method == 'POST':
        form = SignUpForm(request.POST)

        if form.is_valid():
            user = form.save()
            user.refresh_from_db()
            user.profile.address = form.cleaned_data.get('address')
            user.profile.city = form.cleaned_data.get('city')
            user.profile.postcode = form.cleaned_data.get('postcode')
            user.profile.date_birth = form.cleaned_data.get('date_birth')
            user.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)

            return redirect('/')
    else:
        form = SignUpForm()

    return render(request, 'users/signup.html', {'form': form})


def login_view(request):
    """The view that handles logins

    Arguments:
        request {request} -- The request

    Returns:
        render -- The login form or the index is the attempt is successfull
    """
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            # login the user
            user = form.get_user()
            login(request, user)
            if 'next' in request.POST:
                return redirect(request.POST.get('next'))
            if user.profile.shopkeeper:
                return redirect('warehouse:shopkeeper_view')
            return redirect('/')
        else:
            # messages.error(request, 'Username or Password not correct')
            return redirect('users:login')
    else:
        form = AuthenticationForm()
    return render(request, 'users/login.html', {'form': form})


def logout_view(request):
    """The view that handles logouts

    Arguments:
        request {request} -- The request

    Returns:
        render -- The logged out page
    """
    if request.method == 'POST':
        logout(request)
        return render(request, 'users/logout.html')


def myorders(request):
    user_order = Order.objects.all()
    item_order = OrderItem.objects.all()
    product = Product.objects.all()
    return render(request, 'users/myorders.html', {'item_order': item_order, 'user_order': user_order, 'product': product})


def detail_view(request):

    return render(request, 'users/user_details.html')


def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(
                request, 'Your password was successfully updated!')
            return render(request, 'users/password_changed.html')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'users/password_change.html', {
        'form': form
    })
