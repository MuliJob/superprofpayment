# Generated by Django 5.2.2 on 2025-06-23 13:21

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('superprof', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='paymentrequest',
            options={'ordering': ['-created_at'], 'verbose_name': 'Payment Request', 'verbose_name_plural': 'Payment Requests'},
        ),
        migrations.AlterField(
            model_name='paymentrequest',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, help_text='When the payment request was created'),
        ),
        migrations.AlterField(
            model_name='paymentrequest',
            name='payment_amount',
            field=models.DecimalField(decimal_places=2, default=100.0, help_text='Amount to be paid', max_digits=10),
        ),
        migrations.AlterField(
            model_name='paymentrequest',
            name='processed',
            field=models.BooleanField(default=False, help_text='Whether the payment has been processed'),
        ),
        migrations.AlterField(
            model_name='paymentrequest',
            name='processed_at',
            field=models.DateTimeField(blank=True, help_text='When the payment was processed', null=True),
        ),
        migrations.AlterField(
            model_name='paymentrequest',
            name='recipient_name',
            field=models.CharField(default='customer', help_text='Name of the person receiving the payment', max_length=100),
        ),
        migrations.AlterField(
            model_name='paymentrequest',
            name='request_id',
            field=models.UUIDField(default=uuid.uuid4, editable=False, help_text='Unique identifier for this payment request', unique=True),
        ),
        migrations.AlterField(
            model_name='paymentrequest',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, help_text='When the payment request was last updated'),
        ),
        migrations.AlterModelTable(
            name='paymentrequest',
            table='payment_requests',
        ),
    ]
