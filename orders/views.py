from django.shortcuts import render
from rest_framework import viewsets
from .models import Order
from .serializers import OrderSerializer


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer


from client.models import CustomUser
from .models import Order

# def create_order(request):
#     user = request.user
#     order = Order(user=user)
#     order.save()