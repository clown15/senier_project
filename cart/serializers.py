from rest_framework import serializers
from .models import Cart

class CartCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = ('user', 'product', 'quantity')