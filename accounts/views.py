from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from django.views.generic import TemplateView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.shortcuts import redirect
from .forms import CustomUserCreationForm
from .models import CustomUser
from bookings.models import Booking

class CustomLoginView(LoginView):
    """Custom login view that redirects based on user role"""
    template_name = 'accounts/login.html'
    
    def get_success_url(self):
        user = self.request.user
        
        # Redirect based on user role
        if user.role == 'MANAGER':
            return reverse_lazy('products:dashboard')
        elif user.role == 'STAFF':
            return reverse_lazy('orders:pos')
        else:  # CUSTOMER
            return reverse_lazy('customer_dashboard')

class SignUpView(CreateView):
    form_class = CustomUserCreationForm
    template_name = 'accounts/signup.html'

    def get_success_url(self):
        next_url = self.request.GET.get('next')
        if next_url:
            return f"{reverse_lazy('login')}?next={next_url}"
        return reverse_lazy('login')

class CustomerDashboardView(LoginRequiredMixin, TemplateView):
    """Customer account dashboard showing profile and booking status"""
    template_name = 'accounts/customer_dashboard.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        
        # Get all bookings for this customer
        bookings = Booking.objects.filter(user=user).order_by('-created_at')
        
        # Count bookings by status
        pending_count = bookings.filter(status='PENDING').count()
        confirmed_count = bookings.filter(status__in=['AVAILABLE', 'FREE_SOON']).count()
        cancelled_count = bookings.filter(status='CANCELLED').count()
        
        context['user_profile'] = user
        context['bookings'] = bookings
        context['pending_count'] = pending_count
        context['confirmed_count'] = confirmed_count
        context['cancelled_count'] = cancelled_count
        context['total_bookings'] = bookings.count()
        
        return context
