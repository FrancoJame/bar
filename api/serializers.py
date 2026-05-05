from rest_framework import serializers
from products.models import Product, Category
from bookings.models import Booking
from orders.models import Order, OrderItem

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class ProductSerializer(serializers.ModelSerializer):
    category_name = serializers.ReadOnlyField(source='category.name')
    class Meta:
        model = Product
        fields = '__all__'

class BookingSerializer(serializers.ModelSerializer):
    user_name = serializers.ReadOnlyField(source='user.username')
    room_name = serializers.ReadOnlyField(source='room.name')
    class Meta:
        model = Booking
        fields = '__all__'

class OrderItemSerializer(serializers.ModelSerializer):
    product_name = serializers.ReadOnlyField(source='product.name')
    class Meta:
        model = OrderItem
        fields = '__all__'
        read_only_fields = ['order']

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True)
    account_staff_name = serializers.ReadOnlyField(source='staff_member.username')
    
    class Meta:
        model = Order
        fields = ['id', 'staff_member', 'customer_name', 'staff_name', 'total_amount', 'created_at', 'is_paid', 'payment_method', 'amount_paid', 'transaction_id', 'payment_phone', 'items', 'account_staff_name']
        read_only_fields = ['staff_member']

    def create(self, validated_data):
        items_data = validated_data.pop('items')
        # Get staff from context (request.user)
        request = self.context.get('request')
        if request and hasattr(request, 'user'):
            validated_data['staff_member'] = request.user
            
        order = Order.objects.create(**validated_data)
        for item_data in items_data:
            OrderItem.objects.create(order=order, **item_data)
        return order
