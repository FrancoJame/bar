from django.views.generic import ListView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from .models import Product, Category

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
        return context

class ManagerRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.role == 'MANAGER'

class ProductCreateView(LoginRequiredMixin, ManagerRequiredMixin, CreateView):
    model = Product
    template_name = 'products/product_form.html'
    fields = ['name', 'category', 'description', 'price', 'stock_quantity', 'image', 'is_active']
    success_url = reverse_lazy('products:product_list')
