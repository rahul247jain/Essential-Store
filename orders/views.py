from django.contrib.auth.models import User
from django.shortcuts import redirect, render, get_object_or_404, render
from django.urls import reverse
from .models import OrderItem
from .forms import Order, OrderCreateForm
from cart.cart import Cart
import math


def order_create(request):
    cart = Cart(request)
    if request.user.is_authenticated:
        user_id = request.user.id
        current_user_object = User.objects.get(id=user_id)
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.total_price = math.ceil(cart.get_total_price())
            order.user = current_user_object
            order = form.save()
            for item in cart:
                OrderItem.objects.create(order=order,
                                         product=item['product'],
                                         price=item['price'],
                                         quantity=item['quantity'])
            cart.clear()

            request.session['order.id'] = order.id
            # redirect for warehouse
            return redirect(reverse('warehouse:searchproducts'))
        else:
            return render(request, 'orders/order/create.html', {'form': form})
