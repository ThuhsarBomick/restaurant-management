from django.urls import path
from kitchen import views

urlpatterns = [
    path('kitchen',views.KitchenView.as_view(), name="kitchen_view"),
    path('update-order-status/<int:order_id>/', views.update_order_status, name='update_order_status'),
]