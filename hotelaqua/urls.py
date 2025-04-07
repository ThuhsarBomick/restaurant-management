"""
URL configuration for hotelaqua project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from userapp import views
from django.conf.urls.static import static
from django.conf import settings
from django.urls import include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('index/',views.HomeView.as_view(),name='home_view'),
    path('register/',views.RegisterView.as_view(),name='register_view'),
    path('logout/',views.Logout.as_view(),name='logout_view'),
    path('',views.LoginView.as_view(),name='login_view'),
    path('menu/',views.Menulist.as_view(),name='menu_view'),
    path('detail/<int:id>/',views.ProductDetailView.as_view(),name='detail_view'),
    path('add/<int:id>/', views.CartView.as_view(), name='addcart_view'),
    path('list',views.CartListView.as_view(),name='cartlist_view'),
    path('order/<int:id>/',views.PlaceOrderView.as_view(),name='order_view'),
    path('orderlist/',views.OrderListView.as_view(),name='orderlist_view'),
    path('orderdelete/<int:id>/',views.OrderCancelView.as_view(),name='orderdelete_view'),
    path('a/',include('adminapp.urls')),
    path('k/',include('kitchen.urls')),


   
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) 
