from django.views.generic import ListView, CreateView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.db.models import Sum, Count
from django.http import JsonResponse
from .models import Product, Category
from orders.models import Order, OrderItem
from bookings.models import Booking, LoungeRoom
from accounts.models import CustomUser

class ProductListView(ListView):
    model = Product
    template_name = 'products/product_list.html'
    context_object_name = 'products'

    def get_queryset(self):
        category_id = self.kwargs.get('category_id')
        if category_id:
            return Product.objects.filter(category_id=category_id, is_active=True)
        return Product.objects.filter(is_active=True)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        # Group products by category
        category_id = self.kwargs.get('category_id')
        if not category_id:
            categories_with_products = []
            for cat in Category.objects.all():
                products = Product.objects.filter(category=cat, is_active=True)
                if products.exists():
                    categories_with_products.append({
                        'category': cat,
                        'products': products
                    })
            context['categories_with_products'] = categories_with_products
        return context

class ManagerRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.role == 'MANAGER'

class ProductCreateView(LoginRequiredMixin, ManagerRequiredMixin, CreateView):
    model = Product
    template_name = 'products/product_form.html'
    fields = ['name', 'category', 'description', 'price', 'stock_quantity', 'image', 'is_active']
    success_url = reverse_lazy('products:product_list')

class DashboardView(LoginRequiredMixin, ManagerRequiredMixin, TemplateView):
    template_name = 'admin_dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Most sold products
        top_products = OrderItem.objects.values('product__name').annotate(
            total_quantity=Sum('quantity')
        ).order_by('-total_quantity')[:5]
        
        # Most used rooms
        top_rooms = Booking.objects.values('room__name').annotate(
            booking_count=Count('id')
        ).filter(status='BUSY').order_by('-booking_count')[:5]
        
        # Most active staff
        top_staff = Order.objects.values('staff_member__username').annotate(
            order_count=Count('id')
        ).order_by('-order_count')[:5]
        
        context['top_products'] = list(top_products)
        context['top_rooms'] = list(top_rooms)
        context['top_staff'] = list(top_staff)
        
        return context

class DashboardDataView(LoginRequiredMixin, ManagerRequiredMixin, TemplateView):
    def get(self, request, *args, **kwargs):
        # Most sold products for pie chart
        top_products = OrderItem.objects.values('product__name').annotate(
            total_quantity=Sum('quantity')
        ).order_by('-total_quantity')[:5]
        
        product_labels = [item['product__name'] for item in top_products]
        product_data = [item['total_quantity'] for item in top_products]
        
        # Most used rooms
        top_rooms = Booking.objects.values('room__name').annotate(
            booking_count=Count('id')
        ).order_by('-booking_count')[:5]
        
        room_labels = [item['room__name'] for item in top_rooms]
        room_data = [item['booking_count'] for item in top_rooms]
        
        # Most active staff
        top_staff = Order.objects.values('staff_member__username').annotate(
            order_count=Count('id')
        ).order_by('-order_count')[:5]
        
        staff_labels = [item['staff_member__username'] if item['staff_member__username'] else 'Unknown' for item in top_staff]
        staff_data = [item['order_count'] for item in top_staff]
        
        return JsonResponse({
            'products': {
                'labels': product_labels,
                'data': product_data
            },
            'rooms': {
                'labels': room_labels,
                'data': room_data
            },
            'staff': {
                'labels': staff_labels,
                'data': staff_data
            }
        })
