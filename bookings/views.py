from django.views.generic import ListView, CreateView, View
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import get_object_or_404, redirect
from .models import LoungeRoom, Booking
from django.urls import reverse_lazy

class LoungeListView(ListView):
    model = LoungeRoom
    template_name = 'bookings/lounge_list.html'
    context_object_name = 'rooms'

class CreateBookingView(CreateView):
    model = Booking
    template_name = 'bookings/booking_form.html'
    fields = ['booking_type', 'start_time', 'end_time', 'customer_nin', 'customer_phone', 'customer_email']
    success_url = reverse_lazy('bookings:booking_success')

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated and getattr(request.user, 'role', '') == 'MANAGER':
            from django.core.exceptions import PermissionDenied
            raise PermissionDenied("Managers cannot make bookings directly.")
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        room = LoungeRoom.objects.get(id=self.kwargs['room_id'])
        # Assign user only if logged in
        if self.request.user.is_authenticated:
            form.instance.user = self.request.user
        else:
            form.instance.user = None
        form.instance.room = room

        if form.instance.booking_type == 'FULL_DAY':
            form.instance.total_price = room.price_full_day
            if not form.instance.end_time:
                form.instance.end_time = form.instance.start_time.replace(hour=23, minute=59)
        else:
            duration = form.cleaned_data['end_time'] - form.cleaned_data['start_time']
            hours = duration.total_seconds() / 3600
            form.instance.total_price = room.price_per_hour * max(int(hours), 1)

        return super().form_valid(form)

class UserBookingListView(LoginRequiredMixin, ListView):
    model = Booking
    template_name = 'bookings/user_bookings.html'
    context_object_name = 'bookings'

    def get_queryset(self):
        return Booking.objects.filter(user=self.request.user).order_by('-created_at')

class StaffBookingManageView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = Booking
    template_name = 'bookings/staff_manage.html'
    context_object_name = 'bookings'

    def test_func(self):
        return self.request.user.role in ['STAFF', 'MANAGER']

    def get_queryset(self):
        return Booking.objects.all().order_by('-created_at')

class UpdateBookingStatusView(LoginRequiredMixin, UserPassesTestMixin, View):
    def test_func(self):
        return self.request.user.role in ['STAFF', 'MANAGER']

    def post(self, request, pk):
        booking = get_object_or_404(Booking, pk=pk)
        status = request.POST.get('status')
        if status in [choice[0] for choice in Booking.STATUS_CHOICES]:
            booking.status = status
            booking.save()
        return redirect('bookings:staff_manage')
