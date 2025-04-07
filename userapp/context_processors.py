from userapp.models import Cart
from userapp.models import Orders

def cart_count(request):
    if request.user.is_authenticated:
        count=Cart.objects.filter(user=request.user).exclude(status="order-placed").count()
        return {'count':count}
    else:
        return {'count':0}
    
def order_count(request):
    if request.user.is_authenticated:
        count=Orders.objects.filter(user=request.user).exclude(status="in-cart").count()
        return {'ord_count':count} 
    else:
        return{'ord_count':0}   