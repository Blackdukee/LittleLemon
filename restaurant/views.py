from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics

from rest_framework.response import Response

from .models import Booking, Menu
from .serializers import BookingSerializer, MenuSerializer
# Create your views here.
def index(request):
        return render(request, 'index.html', {})
        

class BookingViewSet(ModelViewSet):
        queryset = Booking.objects.all()
        serializer_class = BookingSerializer
        permission_classes = [IsAuthenticated]
        
        

class MenuItemsView(generics.ListCreateAPIView):
        queryset = Menu.objects.all()
        serializer_class = MenuSerializer
        permission_classes = [IsAuthenticated]
        
class SingleMenuItemView(generics.RetrieveUpdateDestroyAPIView):
        queryset = Menu.objects.all()
        serializer_class = MenuSerializer
        permission_classes = [IsAuthenticated]
        