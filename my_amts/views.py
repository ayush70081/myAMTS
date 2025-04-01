from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt  # Temporary for testing
from .models import Bus, ActiveBus, Booking, Ticket, SearchHistory
from .route_finder import RouteFinder
from datetime import datetime, timedelta
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User
from .forms import UserRegistrationForm
import json
from math import radians, sin, cos, sqrt, atan2

def home(request):
    context = {'buses': Bus.objects.all()[:6]}  # Keep the buses for popular routes
    if request.user.is_authenticated:
        try:
            # Get last 3 searches, ordered by most recent first
            recent_searches = SearchHistory.objects.filter(
                user=request.user
            ).order_by('-search_time')[:3]
            
            # Add debug logging
            print(f"Found {recent_searches.count()} recent searches for user {request.user.username}")
            for search in recent_searches:
                print(f"Search: {search.from_stop} to {search.to_stop} at {search.search_time}")
            
            context['recent_searches'] = recent_searches
        except Exception as e:
            print(f"Error fetching recent searches: {str(e)}")
            context['recent_searches'] = []
    return render(request, 'my_amts/home.html', context)

def login_view(request):
    if request.user.is_authenticated:
        if request.user.is_staff:
            return redirect('admin:index')
        return redirect('home')
        
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        if not username or not password:
            messages.error(request, 'Please enter both username and password.')
            return render(request, 'my_amts/login.html')
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            # Staff users should use admin login
            if user.is_staff:
                messages.error(request, 'Please use the admin login page.')
                return render(request, 'my_amts/login.html')
                
            login(request, user)
            messages.success(request, f'Welcome back, {user.username}!')
            
            # Redirect to the page they came from, or home
            next_page = request.GET.get('next', 'home')
            return redirect(next_page)
        else:
            messages.error(request, 'Invalid username or password.')
    
    return render(request, 'my_amts/login.html')

def register_view(request):
    if request.user.is_authenticated:
        return redirect('home')
        
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Registration successful! Please login to continue.')
            return redirect('login')
    else:
        form = UserRegistrationForm()
        
    return render(request, 'my_amts/register.html', {'form': form})

def logout_view(request):
    logout(request)
    messages.success(request, 'You have been successfully logged out.')
    return redirect('home')

@login_required
def search_view(request):
    if not request.user.is_authenticated:
        messages.warning(request, 'Please login to access the search page.')
        return redirect('login')
    return render(request, 'my_amts/search_results.html')

@login_required
@csrf_exempt
def search_buses(request):
    if request.method == 'POST':
        try:
            from_location = request.POST.get('from')
            to_location = request.POST.get('to')
            
            print(f"Search request - From: {from_location}, To: {to_location}")  # Debug log
            
            # Handle get_stops request
            if from_location == 'get_stops':
                all_stops = set()
                buses = Bus.objects.all()
                print(f"Found {buses.count()} buses")  # Debug log
                
                for bus in buses:
                    for stop in bus.stops:
                        all_stops.add(stop['name'])
                
                print(f"Found {len(all_stops)} unique stops")  # Debug log
                return JsonResponse({
                    'status': 'success',
                    'stops': list(all_stops)
                })
            
            # Handle live tracking request
            if to_location == 'track':
                bus = Bus.objects.filter(bus_number=from_location).first()
                if bus:
                    print(f"Found bus {bus.bus_number} for tracking")  # Debug log
                    return JsonResponse({
                        'status': 'success',
                        'routes': [{
                            'transfers': 0,
                            'route_parts': [{
                                'bus_number': bus.bus_number,
                                'stops': bus.stops,
                                'total_stops': len(bus.stops)
                            }]
                        }]
                    })
                else:
                    print(f"Bus not found: {from_location}")  # Debug log
                    return JsonResponse({
                        'status': 'error',
                        'message': 'Bus not found'
                    }, status=404)
            
            # Check if locations exist
            if not from_location or not to_location:
                return JsonResponse({
                    'status': 'error',
                    'message': 'Both from and to locations are required'
                })
            
            # Normal route search
            route_finder = RouteFinder()
            routes = route_finder.find_all_routes(from_location, to_location)
            
            print(f"Found {len(routes)} routes")  # Debug log
            
            if not routes:
                return JsonResponse({
                    'status': 'error',
                    'message': 'No routes found between these stops'
                })
            
            # Save search history only if it's a user-initiated search (not from booking)
            if request.user.is_authenticated and request.POST.get('purpose') != 'fare':
                try:
                    # Check for recent identical searches (within last 5 minutes)
                    five_minutes_ago = datetime.now() - timedelta(minutes=5)
                    recent_identical_search = SearchHistory.objects.filter(
                        user=request.user,
                        from_stop=from_location,
                        to_stop=to_location,
                        search_time__gte=five_minutes_ago
                    ).exists()

                    print(f"Checking search history for {request.user.username}")
                    print(f"From: {from_location}, To: {to_location}")
                    print(f"Recent identical search exists: {recent_identical_search}")

                    # Only create new search history if no identical search in last 5 minutes
                    if not recent_identical_search:
                        search_history = SearchHistory.objects.create(
                            user=request.user,
                            from_stop=from_location,
                            to_stop=to_location
                        )
                        print(f"Created new search history: {search_history}")
                except Exception as e:
                    print(f"Error saving search history: {str(e)}")
                    # If there's an error saving search history, just continue
                    pass
            
            return JsonResponse({
                'status': 'success',
                'routes': routes
            })
            
        except Exception as e:
            print(f"Error in search_buses: {str(e)}")
            return JsonResponse({
                'status': 'error',
                'message': str(e)
            }, status=500)
    
    return JsonResponse({
        'status': 'error',
        'message': 'Invalid request method'
    }, status=400)

@login_required
@csrf_exempt
def get_active_buses(request, bus_number):
    try:
        from_location = request.GET.get('from')
        to_location = request.GET.get('to')
        
        # Get the bus route to determine direction
        bus = Bus.objects.filter(bus_number=bus_number).first()
        if not bus:
            return JsonResponse({
                'status': 'error',
                'message': 'Bus route not found'
            }, status=404)

        stops = bus.stops
        stop_names = [stop['name'] for stop in stops]
        
        try:
            from_index = stop_names.index(from_location)
            to_index = stop_names.index(to_location)
            
            # Determine if user wants forward or reverse direction
            is_forward_journey = from_index < to_index
            
            # Create 4 buses - 2 forward and 2 reverse
            active_buses = []
            
            if is_forward_journey:
                # Show forward direction buses
                active_buses = [
                    {
                        "id": f"{bus_number}-F1",
                        "current_location": stops[len(stops)//4]['name'],
                        "status": "ON_TIME",
                        "direction": "forward",
                        "last_updated": (datetime.now() - timedelta(minutes=2)).strftime("%I:%M %p")
                    },
                    {
                        "id": f"{bus_number}-F2",
                        "current_location": stops[len(stops)//2]['name'],
                        "status": "DELAYED",
                        "direction": "forward",
                        "last_updated": (datetime.now() - timedelta(minutes=5)).strftime("%I:%M %p")
                    }
                ]
            else:
                # Show reverse direction buses
                active_buses = [
                    {
                        "id": f"{bus_number}-R1",
                        "current_location": stops[len(stops)-len(stops)//4]['name'],
                        "status": "ON_TIME",
                        "direction": "reverse",
                        "last_updated": (datetime.now() - timedelta(minutes=3)).strftime("%I:%M %p")
                    },
                    {
                        "id": f"{bus_number}-R2",
                        "current_location": stops[len(stops)-len(stops)//2]['name'],
                        "status": "ON_TIME",
                        "direction": "reverse",
                        "last_updated": (datetime.now() - timedelta(minutes=7)).strftime("%I:%M %p")
                    }
                ]

            return JsonResponse({
                "status": "success",
                "buses": active_buses
            })
            
        except ValueError:
            return JsonResponse({
                'status': 'error',
                'message': 'Stop not found on route'
            }, status=404)
            
    except Exception as e:
        return JsonResponse({
            "status": "error",
            "message": str(e)
        }, status=500)

@csrf_exempt
@login_required
def create_booking(request):
    if request.method == 'POST':
        try:
            # Validate card details
            card_number = request.POST.get('cardNumber', '').replace(' ', '')
            card_expiry = request.POST.get('cardExpiry')
            card_cvv = request.POST.get('cardCvv')
            card_name = request.POST.get('cardName')

            if not all([card_number, card_expiry, card_cvv, card_name]):
                return JsonResponse({
                    'status': 'error',
                    'message': 'Please fill in all card details'
                })

            # Simple card validation
            if not (len(card_number) == 16 and card_number.isdigit()):
                return JsonResponse({
                    'status': 'error',
                    'message': 'Invalid card number'
                })

            if not (len(card_cvv) == 3 and card_cvv.isdigit()):
                return JsonResponse({
                    'status': 'error',
                    'message': 'Invalid CVV'
                })

            # Get the total amount from the form data
            total_amount = request.POST.get('totalAmount')
            if not total_amount:
                return JsonResponse({
                    'status': 'error',
                    'message': 'Total amount is required'
                })

            # Remove the ₹ symbol and convert to float
            total_amount = float(total_amount.replace('₹', '').strip())

            # Create booking
            booking = Booking.objects.create(
                user=request.user,
                bus_number=request.POST.get('bookingBusNumber'),
                from_stop=request.POST.get('bookingFromStop'),
                to_stop=request.POST.get('bookingToStop'),
                total_amount=total_amount
            )

            # Create tickets for the number of passengers
            tickets = []
            passenger_count = int(request.POST.get('passengerCount', 1))
            for i in range(passenger_count):
                ticket = Ticket.objects.create(
                    booking=booking
                )
                tickets.append({
                    'ticket_id': str(ticket.ticket_id),
                    'bus_number': booking.bus_number,
                    'from_stop': booking.from_stop,
                    'to_stop': booking.to_stop,
                    'date': booking.booking_date.strftime('%Y-%m-%d %H:%M'),
                    'qr_code': ticket.qr_code.url if ticket.qr_code else None
                })

            return JsonResponse({
                'status': 'success',
                'booking_id': str(booking.booking_id),
                'tickets': tickets
            })

        except Exception as e:
            print(f"Error in booking creation: {str(e)}")
            return JsonResponse({
                'status': 'error',
                'message': str(e)
            })

    return JsonResponse({
        'status': 'error',
        'message': 'Invalid request method'
    })

@login_required
def my_bookings(request):
    bookings = Booking.objects.filter(user=request.user).order_by('-booking_date')
    return render(request, 'my_amts/my_bookings.html', {'bookings': bookings})

def calculate_distance(lat1, lon1, lat2, lon2):
    """Calculate the Haversine distance between two points"""
    R = 6371  # Earth's radius in kilometers

    lat1, lon1, lat2, lon2 = map(radians, [float(lat1), float(lon1), float(lat2), float(lon2)])
    
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    
    # Haversine formula
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * atan2(sqrt(a), sqrt(1-a))
    distance = R * c

    return round(distance, 2)

@login_required
def get_nearby_stops(request):
    try:
        user_lat = float(request.GET.get('lat'))
        user_lng = float(request.GET.get('lng'))
        
        print(f"User location: {user_lat}, {user_lng}")  # Debug log
        
        # Increase search radius slightly to ensure we don't miss any stops
        SEARCH_RADIUS = 1.2  # kilometers
        
        all_stops = {}  # Dictionary to store unique stops and their buses
        
        # First, collect all unique stops and their distances
        for bus in Bus.objects.all():
            for stop in bus.stops:
                stop_name = stop['name']
                stop_lat = float(stop['coordinates'][0])
                stop_lng = float(stop['coordinates'][1])
                
                distance = calculate_distance(user_lat, user_lng, stop_lat, stop_lng)
                
                if distance <= SEARCH_RADIUS:
                    if stop_name not in all_stops:
                        all_stops[stop_name] = {
                            'name': stop_name,
                            'distance': distance,
                            'coordinates': stop['coordinates'],
                            'buses': []
                        }
        
        # Then, for each nearby stop, find all buses that pass through it
        for bus in Bus.objects.all():
            bus_stops = [s['name'] for s in bus.stops]
            for stop_name in all_stops:
                if stop_name in bus_stops:
                    # Find the direction by looking at stop position
                    stop_index = bus_stops.index(stop_name)
                    
                    # Get terminus stops for this direction
                    if stop_index < len(bus_stops) // 2:
                        # Forward direction
                        route = f"{bus_stops[0]} → {bus_stops[-1]}"
                    else:
                        # Reverse direction
                        route = f"{bus_stops[-1]} → {bus_stops[0]}"
                    
                    bus_info = {
                        'number': bus.bus_number,
                        'route': route
                    }
                    
                    # Add bus only if it's not already added
                    if not any(b['number'] == bus.bus_number for b in all_stops[stop_name]['buses']):
                        all_stops[stop_name]['buses'].append(bus_info)
        
        # Convert to list and sort by distance
        nearby_stops = list(all_stops.values())
        nearby_stops.sort(key=lambda x: x['distance'])
        
        # Debug logging
        print(f"Found {len(nearby_stops)} nearby stops:")
        for stop in nearby_stops:
            print(f"- {stop['name']}: {stop['distance']}km away")
            print(f"  Coordinates: {stop['coordinates']}")
            for bus in stop['buses']:
                print(f"  * Bus {bus['number']}: {bus['route']}")
        
        return JsonResponse({
            'status': 'success',
            'stops': nearby_stops[:10]  # Limit to 10 nearest stops for better UI
        })
        
    except Exception as e:
        print(f"Error in get_nearby_stops: {str(e)}")
        import traceback
        traceback.print_exc()
        return JsonResponse({
            'status': 'error',
            'message': str(e)
        }, status=500)

@csrf_exempt
def bus_details(request):
    bus_number = request.GET.get('bus_number')
    
    try:
        bus = Bus.objects.get(bus_number=bus_number)
        stops = bus.stops  # Get stops directly from JSONField
        
        data = {
            'bus_number': bus.bus_number,
            'route': f"{stops[0]['name']} ↔ {stops[-1]['name']}",
            'total_stops': len(stops),
            'stops': [stop['name'] for stop in stops]
        }
        return JsonResponse(data)
    except Bus.DoesNotExist:
        return JsonResponse({'error': 'Bus not found'}, status=404)

@csrf_exempt
def get_available_buses(request):
    try:
        buses = Bus.objects.all().values_list('bus_number', flat=True)
        return JsonResponse({
            'status': 'success',
            'buses': list(buses)
        })
    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': str(e)
        }, status=500)

@login_required
def profile_view(request):
    # Get user statistics
    total_bookings = Booking.objects.filter(user=request.user).count()
    active_tickets = Ticket.objects.filter(
        booking__user=request.user
    ).count()
    recent_searches = SearchHistory.objects.filter(
        user=request.user
    ).count()

    # Get recent bookings
    recent_bookings = Booking.objects.filter(
        user=request.user
    ).order_by('-booking_date')[:5]

    # Get recent searches
    recent_search_history = SearchHistory.objects.filter(
        user=request.user
    ).order_by('-search_time')[:5]

    context = {
        'total_bookings': total_bookings,
        'active_tickets': active_tickets,
        'recent_searches': recent_searches,
        'recent_bookings': recent_bookings,
        'recent_search_history': recent_search_history,
    }
    
    return render(request, 'my_amts/profile.html', context)

class CustomUserChangeForm(UserChangeForm):
    password = None  # Remove the password field from the form
    
    class Meta:
        model = User
        fields = ('username', 'email')
        
@login_required
def edit_profile_view(request):
    if request.method == 'POST':
        form = CustomUserChangeForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your profile has been updated successfully!')
            return redirect('profile')
    else:
        form = CustomUserChangeForm(instance=request.user)
    
    return render(request, 'my_amts/edit_profile.html', {'form': form})