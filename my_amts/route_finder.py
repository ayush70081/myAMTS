# # my_amts/route_finder.py

from .models import Bus

class RouteFinder:
    def __init__(self):
        self.buses = Bus.objects.all()
        self.routes = []
        self.all_stops = self._get_all_stops()
        print(f"Initialized RouteFinder with {self.buses.count()} buses and {len(self.all_stops)} stops")

    def _get_all_stops(self):
        stops = set()
        for bus in self.buses:
            for stop in bus.stops:
                stops.add(stop['name'])
        return stops

    def find_all_routes(self, from_stop, to_stop):
        print(f"Searching for routes from {from_stop} to {to_stop}")
        
        if from_stop not in self.all_stops:
            print(f"Start stop '{from_stop}' not found in available stops")
            return []
            
        if to_stop not in self.all_stops:
            print(f"End stop '{to_stop}' not found in available stops")
            return []

        direct_routes = self._find_direct_routes(from_stop, to_stop)
        print(f"Found {len(direct_routes)} direct routes")
        
        transfer_routes = self._find_transfer_routes(from_stop, to_stop)
        print(f"Found {len(transfer_routes)} transfer routes")
        
        all_routes = direct_routes + transfer_routes
        print(f"Total routes found: {len(all_routes)}")
        
        return all_routes

    def _find_direct_routes(self, from_stop, to_stop):
        direct_routes = []
        for bus in self.buses:
            route = self._check_direct_route(bus, from_stop, to_stop)
            if route:
                print(f"Found direct route on bus {bus.bus_number}")
                direct_routes.append({
                    'transfers': 0,
                    'route_parts': [route]
                })
        return direct_routes

    def _check_direct_route(self, bus, from_stop, to_stop):
        try:
            stops = bus.stops
            stop_names = [stop['name'] for stop in stops]
            from_index = stop_names.index(from_stop)
            to_index = stop_names.index(to_stop)
            
            if from_index == to_index:
                return None
                
            if from_index < to_index:
                route_stops = stops[from_index:to_index + 1]
            else:
                route_stops = list(reversed(stops[to_index:from_index + 1]))
            
            return {
                'bus_number': bus.bus_number,
                'stops': route_stops,
                'total_stops': len(route_stops)
            }
        except ValueError:
            return None

    def _find_transfer_routes(self, from_stop, to_stop):
        transfer_routes = []
        for intermediate_stop in self.all_stops:
            if intermediate_stop != from_stop and intermediate_stop != to_stop:
                first_leg = self._find_direct_routes(from_stop, intermediate_stop)
                second_leg = self._find_direct_routes(intermediate_stop, to_stop)
                
                if first_leg and second_leg:
                    for route1 in first_leg:
                        for route2 in second_leg:
                            if route1['route_parts'][0]['bus_number'] != route2['route_parts'][0]['bus_number']:
                                transfer_routes.append({
                                    'transfers': 1,
                                    'route_parts': [
                                        route1['route_parts'][0],
                                        route2['route_parts'][0]
                                    ]
                                })
        return transfer_routes