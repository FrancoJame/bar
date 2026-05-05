from django.urls import path
from . import views

app_name = 'products'

urlpatterns = [
    path('', views.ProductListView.as_view(), name='product_list'),
    path('add/', views.ProductCreateView.as_view(), name='product_add'),
    path('category/<int:category_id>/', views.ProductListView.as_view(), name='product_list_by_category'),
    path('dashboard/', views.DashboardView.as_view(), name='dashboard'),
    path('api/dashboard-data/', views.DashboardDataView.as_view(), name='dashboard_data'),
]
