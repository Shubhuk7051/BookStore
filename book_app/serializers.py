from .models import *
from rest_framework import serializers

class BookSerializer(serializers.ModelSerializer):
    class Meta:
        
        model=Book
        fields ='__all__'
        
class OrderSerializer(serializers.ModelSerializer):
    
    class Meta:
        
        model=Order
        lookup_field = 'customer'
        fields ='__all__'
        