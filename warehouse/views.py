from django.shortcuts import render, redirect
from django.urls import reverse
from django.shortcuts import get_object_or_404, get_list_or_404
from users.models import User, Profile
from orders.models import Order, OrderItem
from .models import Warehouse, KeyVal
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from math import sin, cos, sqrt, atan2, radians, pi
import json

localities = {
    "Bhim Colony": "23.02579,72.58727",
    "Basai Enclave-2": "12.97194,77.59369",
    "Chandan Vihar": "13.08784,80.27847",
    "Ganga Vihar": "24.879999,74.629997",
    "Sai Kunj": "26.263863, 73.008957",
    "Shri Ram Colony": "21.250000 ,81.629997",
    "Amanpura Colony": "24.882618,72.858894",
    "Patel Nagar Ext": "25.771315,73.323685",
    "Shiv Nagar": "28.65195,77.23149",
    "Vikas Nagar": "17.38405,78.45636",
    "Basai Enclave Ext": "26.46523,80.34975",
    "Krishna Nagar": "22.56263,88.36304",
    "Surya Vihar": "19.07283,72.88261",
    "Ashok Vihar": "16.994444 , 73.300003",
    "Rajeev colony": "18.51957,73.85535",
    "Nihal Vihar": "21.19594,72.83023",
    "Mayur Kunj": "26.264776, 82.072708",
    "Ryan Enclave": "26.839281,80.923133",
    "Shyam Kunj": "25.615379,85.101027",
    "Shanti Kunj": "22.717736,75.85859",
    "Mohan Nagar": "22.299405,73.208119",
    "Vatika Kunj": "23.254688,77.402892",
    "Defense Enclave": "11.005547,76.966122",
    # "Agra": "27.187935,78.003944",
    # "Meerut": "28.980018,77.706356",
    # "Madurai": "9.917347,78.119622",
    # "Guwahati": "26.176076,91.762932",
    # "Thiruvananthapuram": "8.485498,76.949238",
    # "Tiruchchirappalli": "10.815499,78.696513",
    # "Kota": "25.182544,75.839065",
    # "Jammu": "32.735686,74.869112",
    # "Mangalore": "12.865371,74.842432",
    # "Ajmer": "26.452103,74.638667",
    # "Shillong": "25.573987,91.896807",
    # "New Delhi": "28.6,77.2"
}


def getDistanceFromLatLonInKm(lat1, lon1, lat2, lon2):
    R = 6371
    dLat = deg2rad(lat2 - lat1)
    dLon = deg2rad(lon2 - lon1)
    a = sin(dLat / 2) * sin(dLat / 2) + cos(deg2rad(lat1)) * \
        cos(deg2rad(lat2)) * sin(dLon / 2) * sin(dLon / 2)
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    d = R * c
    return d


def deg2rad(deg):
    return deg * (pi / 180)


def searchproducts(request):
    fcart = OrderItem.objects.filter(order_id=request.session['order.id'])
    totalitems = OrderItem.objects.filter(
        order_id=request.session['order.id']).count()
    warehouses = Warehouse.objects.all()
    user_order = get_object_or_404(Order, id=request.session['order.id'])
    user_loc = user_order.locality
    print(user_loc)
    lat1, lon1 = localities.get(user_loc).split(",")
    dis = {}
    count = 0
    extra = False
    for item in fcart:
        min_dist = 10000000000.00
        nearest_war = ''
        for wh in warehouses:
            try:
                wareitem = get_object_or_404(
                    KeyVal, locname=wh, product=item.product)
            except:
                continue
            if (wareitem.quantity >= item.quantity):
                if user_loc == wh.location:  # Skip distance calculation
                    min_dist = 0
                    nearest_war = wh
                    break
                lat2 = wh.loc_x
                lon2 = wh.loc_y
                lat1, lon1, lat2, lon2 = float(lat1), float(
                    lon1), float(lat2), float(lon2)
                dist = getDistanceFromLatLonInKm(lat1, lat2, lon1, lon2)
                # print(item.product.name)
                # print(wh.location)
                # print(dist)
                if (dist <= min_dist):
                    min_dist = dist
                    nearest_war = wh
                else:
                    continue
                print(nearest_war.location)
            else:
                continue
        if nearest_war and nearest_war.time_slot == item.order.time_slot:
            count = count+1

        dis[item.product.name] = nearest_war
        if(nearest_war):
            item.selected_shop = nearest_war
            item.save()
            print(nearest_war.location)
        else:
            user_order.total_price = user_order.total_price-item.get_cost()
            print(user_order.total_price)

    # print(count)
    # Adding extra charge to the user's account
    if count < (totalitems/2):
        extra = 50

    return render(request, 'warehouse/delivery_area.html', {'waredis': dis, 'extra': extra, 'user_order': user_order})


@staff_member_required
def shopkeeper_view(request):
    cur_user = request.user
    items = OrderItem.objects.filter(selected_shop=cur_user.profile.warehouse)
    # unplaced_order=OrderItem.objects.filter(order__paid=False)
    return render(request, 'shopkeeper.html', {'items': items})

# @login_required
# def delivery_boy(request):
#     user = User.objects.get(id=request.user.id)
#     boy = Profile.objects.filter(delivery_boy=True)

#     return redirect('warehouse: delivery_boy.html')
