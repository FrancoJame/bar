from django.urls import path
from django.views.generic import TemplateView
from . import views

app_name = 'bookings'

urlpatterns = [
    path('', views.LoungeListView.as_view(), name='lounge_list'),
    path('book/<int:room_id>/', views.CreateBookingView.as_view(), name='create_booking'),
    path('my-bookings/', views.UserBookingListView.as_view(), name='user_bookings'),
    path('staff-manage/', views.StaffBookingManageView.as_view(), name='staff_manage'),
    path('update-status/<int:pk>/', views.UpdateBookingStatusView.as_view(), name='update_status'),
    path('booking-success/', TemplateView.as_view(template_name='bookings/booking_success.html'), name='booking_success'),
]
