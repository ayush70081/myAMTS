from datetime import datetime, timedelta
from decimal import Decimal

def calculate_ticket_price(from_stop, to_stop, bus):
    """Calculate ticket price based on number of stops"""
    stops = bus.stops
    stop_names = [stop['name'] for stop in stops]
    
    try:
        start_idx = stop_names.index(from_stop)
        end_idx = stop_names.index(to_stop)
        num_stops = abs(end_idx - start_idx)
        
        # Base price
        base_price = Decimal('10.00')
        
        # Add price per stop
        price_per_stop = Decimal('2.00')
        total_price = base_price + (price_per_stop * num_stops)
        
        # Maximum price cap
        max_price = Decimal('50.00')
        return min(total_price, max_price)
        
    except ValueError:
        return None

def generate_ticket_validity():
    """Generate ticket validity period (24 hours from purchase)"""
    return datetime.now() + timedelta(hours=24) 