from django.shortcuts import render
from django.views.generic import ListView
from userapp.models import Orders
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from userapp.models import Orders

# Create your views here.

class KitchenView(ListView):
    model = Orders
    template_name = 'kitchen.html'
    context_object_name = 'orders'

    def get_queryset(self):
        # Get all orders that are not yet on the table
        return Orders.objects.filter(status='order-placed')

    def get_context_data(self, **kwargs):
        # Add additional context data (e.g., user and table number)
        context = super().get_context_data(**kwargs)
        return context
    


@csrf_exempt
def update_order_status(request, order_id):
    if request.method == 'POST':
        try:
            order = Orders.objects.get(id=order_id)
            order.status = 'prepared'  # Update status to 'prepared'
            order.save()
            return JsonResponse({'success': True})
        except Orders.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Order not found'})
    return JsonResponse({'success': False, 'error': 'Invalid request method'})    
