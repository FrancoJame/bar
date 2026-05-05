from django.views.generic import TemplateView, DetailView, ListView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .models import Order, OrderItem
from products.models import Product, Category
from django.shortcuts import redirect
from django.urls import reverse_lazy

class StaffRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.role in ['STAFF', 'MANAGER']

class ManagerRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.role == 'MANAGER'

class StaffOnlyRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.role == 'STAFF'

class POSView(LoginRequiredMixin, StaffOnlyRequiredMixin, TemplateView):
    template_name = 'orders/pos.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        context['products'] = Product.objects.filter(is_active=True)
        return context

class ReceiptView(LoginRequiredMixin, StaffRequiredMixin, DetailView):
    model = Order
    template_name = 'orders/receipt.html'
    context_object_name = 'order'
    pk_url_kwarg = 'order_id'

class TransactionListView(LoginRequiredMixin, StaffRequiredMixin, ListView):
    model = Order
    template_name = 'orders/transaction_list.html'
    context_object_name = 'transactions'
    
    def get_queryset(self):
        return Order.objects.all().order_by('-created_at')

class TransactionUpdateView(LoginRequiredMixin, ManagerRequiredMixin, UpdateView):
    model = Order
    template_name = 'orders/transaction_form.html'
    fields = ['customer_name', 'payment_method', 'amount_paid', 'transaction_id', 'payment_phone', 'is_paid']
    success_url = reverse_lazy('orders:transaction_list')

class TransactionDeleteView(LoginRequiredMixin, ManagerRequiredMixin, DeleteView):
    model = Order
    template_name = 'orders/transaction_confirm_delete.html'
    success_url = reverse_lazy('orders:transaction_list')
