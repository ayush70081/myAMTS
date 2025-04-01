from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import Booking, Ticket
from .forms import BookingForm, TicketForm
from django.views.decorators.csrf import csrf_exempt
import json

@login_required
@csrf_exempt
def book_ticket(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body) if request.body else request.POST

            # Create booking
            booking_data = {
                'bus_number': data.get('bus_number'),
                'from_stop': data.get('from_stop'),
                'to_stop': data.get('to_stop'),
                'total_amount': float(data.get('total_amount', 0)),
                'user': request.user  # Add the user to the booking
            }
            
            booking = Booking.objects.create(**booking_data)
            
            # Create single ticket without passenger info
            ticket = Ticket.objects.create(booking=booking)
            
            return JsonResponse({
                'status': 'success',
                'booking_id': str(booking.booking_id),
                'message': 'Booking created successfully'
            })
                
        except Exception as e:
            return JsonResponse({
                'status': 'error',
                'message': str(e)
            })
    
    return JsonResponse({
        'status': 'error',
        'message': 'Invalid request method'
    })

@login_required
def ticket_list(request):
    # Get all bookings for the current user
    bookings = Booking.objects.all().order_by('-booking_date')
    return render(request, 'my_amts/ticket_list.html', {'bookings': bookings})

@login_required
def ticket_detail(request, ticket_id):
    # Get the ticket and verify it belongs to the current user
    ticket = get_object_or_404(Ticket, ticket_id=ticket_id, booking__user=request.user)
    return render(request, 'my_amts/ticket_detail.html', {'ticket': ticket})

@login_required
def verify_ticket(request, ticket_id):
    ticket = get_object_or_404(Ticket, ticket_id=ticket_id)
    is_valid = ticket.booking.payment_status == 'COMPLETED'
    
    return JsonResponse({
        'status': 'success',
        'is_valid': is_valid,
        'ticket': {
            'ticket_id': str(ticket.ticket_id),
            'bus_number': ticket.booking.bus_number,
            'from_stop': ticket.booking.from_stop,
            'to_stop': ticket.booking.to_stop,
            'booking_date': ticket.booking.booking_date.strftime('%Y-%m-%d %H:%M'),
            'payment_status': ticket.booking.payment_status
        }
    }) 