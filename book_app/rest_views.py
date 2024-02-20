from rest_framework import generics
from .models import *
from .serializers import *

class BookListView(generics.ListCreateAPIView):
    queryset=Book.objects.all()
    serializer_class=BookSerializer
    
class BookDetailView(generics.RetrieveUpdateDestroyAPIView):
    
    queryset=Book.objects.all()
    serializer_class=BookSerializer
    
class OrderListView(generics.RetrieveUpdateDestroyAPIView):
    
    queryset=Order.objects.all()
    serializer_class=OrderSerializer
    lookup_field='customer'