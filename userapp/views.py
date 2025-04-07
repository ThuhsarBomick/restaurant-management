from django.shortcuts import render,redirect
from django.views.generic import TemplateView,CreateView,FormView,ListView,DetailView,DeleteView
from django.contrib.auth.models import User
from userapp.models import Cart,Orders
from userapp.forms import RegisterForm,LoginForm,CartForm,OrderForm
from django.contrib.auth import authenticate,login,logout
from django.urls import reverse_lazy
from userapp.models import Category,Product
from django.views import View
from django.contrib import messages
from django.views.generic import ListView
from userapp.models import Orders, Bill
from django.shortcuts import redirect
from django.contrib.auth import authenticate, login
from django.views.generic.edit import FormView
from .forms import LoginForm

from django.conf import settings


# Create your views here.

class HomeView(TemplateView):
    template_name='index.html'

class Logout(View):
    def get(self,request):
        logout(request)
        messages.success(request,'logout successful')
        return redirect('login_view')     



class RegisterView(CreateView):
    template_name='register.html'
    model=User
    success_url=reverse_lazy('register_view')
    form_class=RegisterForm

    def form_valid(self, form):
        User.objects.create_user(**form.cleaned_data)
        messages.success(self.request,'Registration successful')
        return redirect('login_view')
    def form_invalid(self, form):
        messages.error(self.request,'Registration failed')
        
        return redirect('register_view')
    
    


class LoginView(FormView):
    form_class = LoginForm
    template_name = 'login.html'

    def post(self, request, *args, **kwargs):
        uname = request.POST.get('username')
        psw = request.POST.get('password')
        user = authenticate(request, username=uname, password=psw)
        
        if user:
            login(request, user)
            
            # Check if the user is a superuser and has a specific ID
            if user.is_superuser:
                if user.id == 11:
                    return redirect('admin_order_view')
                elif user.id == 10:
                    return redirect('kitchen_view')
            
            
            return redirect('home_view')
        
       
        return redirect('login_view')

class Menulist(TemplateView):
    template_name='menu.html'
    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)
        context['products']=Product.objects.all()
        return context

class ProductDetailView(DetailView):
    template_name='detail.html'
    pk_url_kwarg='id'
    model=Product
    context_object_name='products'   

class CartView(TemplateView):
    template_name="addtocart.html"

    def get_context_data(self, **kwargs):
       context=super().get_context_data(**kwargs)  
       context['products']=Product.objects.get(id=kwargs.get("id"))
       context['form']=CartForm()
       return context  

    
    def post(self, request, *args, **kwargs):
        user = request.user
        id = kwargs.get("id")
        product = Product.objects.get(id=id)
        quantity = request.POST.get("quantity")
        quantity = int(quantity)  
        print(quantity)

        cart_list = Cart.objects.filter(user=user, product=product,status='in-cart')
        
        if cart_list:
            cart = cart_list[0]
            cart.quantity = cart.quantity + quantity 
            cart.save()
            return redirect('menu_view')
        else:
            Cart.objects.create(user=user, product=product, quantity=quantity)
            return redirect('menu_view')
           

class CartListView(ListView):   
    
    model = Cart
    template_name = 'cart.html'
    
    context_object_name = 'cartlist'

    def get_queryset(self):
        return Cart.objects.filter(user=self.request.user).exclude(status='order-placed') 

class PlaceOrderView(TemplateView):
    template_name = 'placeorder.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cart_item = Cart.objects.get(id=kwargs.get("id"))
        context['products'] = cart_item  
        return context

    def post(self, request, *args, **kwargs):
        cart_item = Cart.objects.get(id=kwargs.get("id"))
        user = request.user
        table_no = request.POST.get("table_No")  

        if not table_no:
            return redirect("order_view", id=cart_item.id)  

        order = Orders.objects.create(
            user=user,
            product=cart_item,  
            quantity=cart_item.quantity,  
            price=cart_item.product.price,  
            table_No=table_no,  
            status='order-placed'  
        )

        
        cart_item.status = 'order-placed'
        cart_item.save()

        return redirect("cartlist_view")  
    



class OrderListView(ListView):
    model = Orders
    template_name = 'orderlist.html'
    context_object_name = 'orderslist'

    def get_queryset(self):
        return Orders.objects.filter(user=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        total_bill = sum(order.product.product.price * order.quantity for order in context['orderslist'])
        context['total_bill'] = total_bill

        table_no = context['orderslist'].first().table_No if context['orderslist'] else None

        if total_bill > 0 and table_no:
            Bill.objects.create(
                user=self.request.user,
                total=total_bill,
                table_No=table_no
            )

        context['razorpay_key'] = settings.RAZORPAY_KEY_ID
        context['currency'] = 'INR'
        context['company_name'] = 'Your Company Name'

        return context

class OrderCancelView(DeleteView):
    model=Orders
    template_name='cart_delete.html'
    pk_url_kwarg='id'
    success_url=reverse_lazy('orderlist_view')    