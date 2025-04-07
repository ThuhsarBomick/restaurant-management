from django.views.generic import ListView, View
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from django.urls import reverse_lazy
from django.db.models import Max
from userapp.models import Bill, Orders
from django.shortcuts import render
import razorpay
from django.conf import settings
from django.shortcuts import get_object_or_404, redirect
from django.core.mail import send_mail
from django.contrib import messages


class AdminOrderView(ListView):
    model = Bill
    template_name = 'admin_order.html'
    context_object_name = 'orders'

    def get_queryset(self):
        latest_bills = Bill.objects.values('user').annotate(
            latest_date=Max('date')
        ).order_by('-latest_date')

        latest_bill_ids = []
        for bill in latest_bills:
            latest_bill = Bill.objects.filter(
                user=bill['user'],
                date=bill['latest_date']
            ).first()
            if latest_bill:
                latest_bill_ids.append(latest_bill.id)

        return Bill.objects.filter(id__in=latest_bill_ids)





class SendEmailView(View):
    def get(self, request, user_id, order_id, *args, **kwargs):
        order = get_object_or_404(Bill, id=order_id, user_id=user_id)
        user = order.user

        client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))

        try:
            payment_link = client.payment_link.create({
                "amount": int(order.total * 100),  
                "currency": "INR",
                "description": f"Payment for Order #{order.id}",
                "customer": {
                    "name": user.username,
                    "email": user.email,
                    "user": "user.user_name"  
                },
                "notify": {
                    "email": True,
                    "sms": True
                },
                "callback_url": "https://yourwebsite.com/payment-success/",  
                "callback_method": "get"
            })

            payment_link_url = payment_link['short_url']  

        except Exception as e:
            messages.error(request, f"Failed to create payment link: {str(e)}")
            return redirect('admin_order_view')  

        subject = f"Your Bill for Order #{order.id}"
        message = (
            f"Hello {user.username},\n\n"
            f"Thank you for dining with us. Here are your bill details:\n\n"
            f"Order ID: {order.id}\n"
            f"Table Number: {order.table_No}\n"
            f"Total Amount: ₹{order.total}\n"
            f"Date: {order.date}\n\n"
            f"Please click the link below to complete your payment:\n"
            f"{payment_link_url}\n\n"
            "We hope to see you again soon!\n\n"
            "Best regards,\n"
            "The Andys SeaBrew Team"
        )
        recipient_email = user.email  

        try:
            send_mail(
                subject,
                message,
                settings.DEFAULT_FROM_EMAIL,
                [recipient_email],
                fail_silently=False,
            )
            messages.success(request, "Email sent successfully!")
        except Exception as e:
            messages.error(request, f"Failed to send email: {str(e)}")

        return redirect('admin_order_view')  
class DeleteOrdersView(View):
    def get(self, request, user_id, *args, **kwargs):
        return render(request, 'confirm_delete.html', {'user_id': user_id})

    def post(self, request, user_id, *args, **kwargs):
        orders = Orders.objects.filter(user_id=user_id)

        orders.delete()

        bills = Bill.objects.filter(user_id=user_id)
        bills.delete()

        return redirect('admin_order_view')
