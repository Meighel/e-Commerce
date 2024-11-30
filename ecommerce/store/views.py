from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from store.models import User, Order, CartItem
from store.serializers import UserSerializer, OrderSerializer, CartItemSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.permissions import AllowAny
from uuid import UUID
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

class UserView(APIView):

    @swagger_auto_schema(
        operation_description="Create a new user",
        request_body=UserSerializer,  
        responses={201: UserSerializer(), 400: 'Invalid data'}
    )
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        operation_description="Retrieve user information",
        responses={200: UserSerializer(), 404: 'User not found'}
    )
    
    def get(self, request, user_id=None):
        if user_id:
            try:
                user = User.objects.get(id=user_id)
            except User.DoesNotExist:
                return Response(
                    {"error": "User not found"},
                    status=status.HTTP_404_NOT_FOUND,
                )
            serializer = UserSerializer(user)
            return Response(serializer.data)
        
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)

class OrderView(APIView):

    @swagger_auto_schema(
        operation_description="Get details of an order by its ID",
        responses={200: OrderSerializer(), 404: 'Order not found'}
    )

    def get(self, request, order_id=None):
        try:
            if order_id:
                order = Order.objects.get(id=order_id)
                serializer = OrderSerializer(order)
                return Response(serializer.data)
            orders = Order.objects.all()
            serializer = OrderSerializer(orders, many=True)
            return Response(serializer.data)
        except Order.DoesNotExist:
            return Response({"error": "Order not found."}, status=status.HTTP_404_NOT_FOUND)

    @swagger_auto_schema(
        operation_description="Update an order status or details",
        responses={200: OrderSerializer(), 400: 'Bad request', 404: 'Order not found'}
    )

    def put(self, request):
        try:
            order = Order.objects.get(id=request.data['id'])
            serializer = OrderSerializer(order, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Order.DoesNotExist:
            return Response({"error": "Order not found."}, status=status.HTTP_404_NOT_FOUND)

    @swagger_auto_schema(
        operation_description="Delete an order by ID",
        responses={204: 'Order deleted successfully', 404: 'Order not found'}
    )

    def delete(self, request):
        try:
            order = Order.objects.get(id=request.data['id'])
            order.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Order.DoesNotExist:
            return Response({"error": "Order not found."}, status=status.HTTP_404_NOT_FOUND)

class CartItemView(APIView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        operation_description="Get all cart items",
        responses={200: CartItemSerializer(many=True), 404: 'No cart items found'}
    )

    def get(self, request, cart_item_id=None):

        if cart_item_id:
            try:
                cart_item_id = CartItem.objects.get(id=cart_item_id)
            except CartItem.DoesNotExist:
                return Response({"error": "Cart item not found."}, status=status.HTTP_404_NOT_FOUND,)
        cart_items = CartItem.objects.all()
        if cart_items.exists():
            serializer = CartItemSerializer(cart_items, many=True)
            return Response(serializer.data)
        return Response({"error": "No cart items found."}, status=status.HTTP_404_NOT_FOUND)

    @swagger_auto_schema(
        operation_description="Add a new cart item",
        request_body=CartItemSerializer,  
        responses={201: CartItemSerializer(), 400: 'Invalid data'}
    )

    #post with specific id is not working as it should be

    def post(self, request):
        serializer = CartItemSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @swagger_auto_schema(
        operation_description="Update a cart item by its ID.",
        responses={
            200: CartItemSerializer(),
            400: "Invalid data",
            404: "Cart item not found or ID not provided",
        },
        request_body=CartItemSerializer
    )
    def put(self, request, cart_item_id=None):
        if cart_item_id:
            try:
                # Fetch the cart item by the ID provided in the URL
                cart_item = CartItem.objects.get(id=cart_item_id)
                serializer = CartItemSerializer(cart_item, data=request.data, partial=True)
                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data, status=status.HTTP_200_OK)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            except CartItem.DoesNotExist:
                return Response(
                    {"error": "Cart item not found."}, status=status.HTTP_404_NOT_FOUND
                )
        else:
            return Response(
                {"error": "Cart item ID is required to update an item."},
                status=status.HTTP_404_NOT_FOUND,
            )


    @swagger_auto_schema(
        operation_description="Delete a cart item",
        responses={204: 'Cart item deleted', 404: 'Cart item not found'},
    )

    def delete(self, request, cart_item_id=None):

        if cart_item_id:
            try:
                cart_item = CartItem.objects.get(id=cart_item_id)
                cart_item.delete()
                return Response(status=status.HTTP_204_NO_CONTENT)
            except CartItem.DoesNotExist:
                return Response({"error": "Cart item not found."}, status=status.HTTP_404_NOT_FOUND)
        else:
            # If no 'id' is provided, delete all cart items
            CartItem.objects.all().delete()
            return Response({"message": "All cart items deleted."}, status=status.HTTP_204_NO_CONTENT)

class CheckoutView(APIView):

    @swagger_auto_schema(
        operation_description="Process an order by changing its status to 'Processed'",
        responses={200: 'Order processed successfully', 400: 'Invalid order status', 404: 'Order not found'}
    )

    def put(self, request, order_id):
        try:
            order = Order.objects.get(id=order_id)
        except Order.DoesNotExist:
            return Response({"error": "Order not found"}, status=status.HTTP_400_BAD_REQUEST)

        if order.status == 'Pending':
            order.status = 'Processed'
            order.save()
            return Response({"message": "Order processed successfully."}, status=status.HTTP_200_OK)
        elif order.status == 'Processed':
            return Response({"message": "Order has already been processed."}, status=status.HTTP_200_OK)
        else:
            return Response({"error": "Invalid order status."}, status=status.HTTP_400_BAD_REQUEST)




