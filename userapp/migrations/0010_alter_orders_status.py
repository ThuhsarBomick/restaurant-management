# Generated by Django 5.1.6 on 2025-03-10 08:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userapp', '0009_alter_orders_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orders',
            name='status',
            field=models.CharField(choices=[('order-placed', 'order-placed'), ('cancelled', 'cancelled'), ('preparing', 'preparing'), ('Order-Prepared', 'Order-Preparedpyu')], default='order-placed', max_length=100),
        ),
    ]
