from django.urls import path
from adminapp import views

urlpatterns = [
    path('adminorder/', views.AdminOrderView.as_view(), name="admin_order_view"),
    path('send-email/<int:user_id>/<int:order_id>/', views.SendEmailView.as_view(), name="send_email"),
    path('delete-orders/<int:user_id>/', views.DeleteOrdersView.as_view(), name="delete_orders"),
]