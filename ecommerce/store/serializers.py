from rest_framework import serializers
from store.models import User, Order, CartItem

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

class CartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = '__all__'

    def create(self, validated_data):
        request = self.context.get('request')  # Access the request from the serializer context
        if request and request.user.is_authenticated:
            validated_data['order'] = Order.objects.get_or_create(user=request.user, status="active")[0]  # Get or create order
        return super().create(validated_data)

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'
