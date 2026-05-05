from django.urls import path
from . import views

app_name = 'orders'

urlpatterns = [
    path('pos/', views.POSView.as_view(), name='pos'),
    path('receipt/<int:order_id>/', views.ReceiptView.as_view(), name='receipt'),
    path('transactions/', views.TransactionListView.as_view(), name='transaction_list'),
    path('transactions/<int:pk>/edit/', views.TransactionUpdateView.as_view(), name='transaction_edit'),
    path('transactions/<int:pk>/delete/', views.TransactionDeleteView.as_view(), name='transaction_delete'),
]
