# my_amts/management/commands/load_bus_data.py
from django.core.management.base import BaseCommand
from my_amts.models import Bus

class Command(BaseCommand):
    help = 'Load initial bus data'

    def handle(self, *args, **kwargs):
        # Real AMTS bus routes data
        buses = [
            {
                'bus_number': '33',
                'stops': [
                    {'name': 'Gokul Park', 'coordinates': [23.03145, 72.65191]},
                    {'name': 'Gandhi Park', 'coordinates': [23.02777, 72.64104]},
                    {'name': 'Khodiyar Nagar', 'coordinates': [23.03268, 72.63918]},
                    {'name': 'Bapu Nagar', 'coordinates': [23.03388, 72.63406]},
                    {'name': 'Bapu Nagar Char Rasta', 'coordinates': [23.03495, 72.62937]},
                    {'name': 'Bombay Housing', 'coordinates': [23.03504, 72.61747]},
                    {'name': 'Sharda Ben', 'coordinates': [23.03180, 72.61150]},
                    {'name': 'Kalupur', 'coordinates': [23.03017, 72.60041]},
                    {'name': 'Sarangpur', 'coordinates': [23.02396, 72.59961]},
                    {'name': 'Raipur', 'coordinates': [23.01696, 72.59397]},
                    {'name': 'MNC', 'coordinates': [23.01971, 72.58615]},
                    {'name': 'Lal Darwaja', 'coordinates': [23.02458, 72.57865]}
                ]
            },
            {
                'bus_number': '58',
                'stops': [
                    
                    # 
                    {'name': 'Thakkar Nagar', 'coordinates': [23.03910, 72.63885]},
                    {'name': 'India Colony', 'coordinates': [23.03869, 72.63423]},
                    {'name': 'Vijay Chowk', 'coordinates': [23.03863, 72.63121]},
                    {'name': 'Bapu Nagar Char Rasta', 'coordinates': [23.03495, 72.62937]},
                    {'name': 'Bombay Housing', 'coordinates': [23.03504, 72.61747]},
                    {'name': 'Sharda Ben', 'coordinates': [23.03180, 72.61150]},
                    {'name': 'Kalupur', 'coordinates': [23.03017, 72.60041]},
                    {'name': 'Sarangpur', 'coordinates': [23.02396, 72.59961]},
                    {'name': 'Raipur', 'coordinates': [23.01696, 72.59397]},
                    {'name': 'Gita Mandir', 'coordinates': [23.01483, 72.59125]},
                    {'name': 'Jamalpur', 'coordinates': [23.01063, 72.57777]},
                    {'name': 'Paldi', 'coordinates': [23.01370, 72.56476]}
                ]
            },
            {
                'bus_number': '56',
                'stops': [
                    {'name': 'Naroda', 'coordinates': [23.06424, 72.64280]},
                    {'name': 'Krishna Nagar', 'coordinates': [23.05705, 72.64326]},
                    {'name': 'Bajrang Ashram', 'coordinates': [23.04768, 72.64113]},
                    {'name': 'Thakkar Nagar', 'coordinates': [23.03910, 72.63885]},
                    {'name': 'Bapu Nagar Char Rasta', 'coordinates': [23.03495, 72.62937]},
                    {'name': 'Bombay Housing', 'coordinates': [23.03504, 72.61747]},
                    {'name': 'Sharda Ben', 'coordinates': [23.03180, 72.61150]},
                    {'name': 'Kalupur', 'coordinates': [23.03017, 72.60041]},
                    {'name': 'Sarangpur', 'coordinates': [23.02396, 72.59961]},
                    {'name': 'Raipur', 'coordinates': [23.01696, 72.59397]},
                    {'name': 'Lal Darwaja', 'coordinates': [23.02458, 72.57865]}
                ]
            },
            {
        "bus_number": "31_5",
        "stops": [
            {"name": "Lal Darwaja","coordinates": [23.02458, 72.57865]},
            {"name": "VS Hospital","coordinates": [23.02163, 72.57138]},
            {"name": "Anjali Char Rasta","coordinates": [23.00315, 72.55187]},
            {"name": "Vasna","coordinates": [23.00180, 72.54801]},
            {"name": "Vishala","coordinates": [22.99528, 72.53205]},
            {"name": "Khursid Park","coordinates": [22.99112, 72.51860]},
            {"name": "Ambar Tower","coordinates": [22.98896, 72.51259]},
            {"name": "Sarkhej","coordinates": [22.98752, 72.50353]},
            {"name": "Ujala","coordinates": [22.98042, 72.49255]},
            {"name": "Sanand Chowkdi","coordinates": [22.98701, 72.49388]},
            {"name": "LJ College","coordinates": [22.98712, 72.48893]}
        ]
            }
    ,
    {
        "bus_number": "130",
        "stops": [
            {"name": "Naroda","coordinates": [23.06424, 72.64280]},
            {"name": "Krishna Nagar","coordinates": [23.05705, 72.64326]},
            {"name": "Vijay Park","coordinates": [23.05123, 72.64201]},
            {"name": "Bajrang Ashram","coordinates": [23.04768, 72.64113]},
            {"name": "Khodiyar Nagar","coordinates": [23.03268, 72.63918]},
            {"name": "Soni ni Chali","coordinates": [23.02203, 72.63830]},
            {"name": "Rabari Colony","coordinates": [23.00433, 72.63713]},
            {"name": "Purvadeep Society","coordinates": [22.99605, 72.63437]},
            {"name": "Jashoda Nagar","coordinates": [22.98375, 72.62412]},
            {"name": "Ghodasar","coordinates": [22.97839, 72.61015]},
            {"name": "Isanpur","coordinates": [22.97552, 72.60076]},
            {"name": "Narol","coordinates": [22.97288, 72.58951]},
            {"name": "Chandola","coordinates": [22.98203, 72.58568]},
            {"name": "Danilimda","coordinates": [22.99608, 72.57912]},
            {"name": "Chadra Nagar","coordinates": [22.99980, 72.55804]},
            {"name": "Anjali Char Rasta","coordinates": [23.00315, 72.55187]}
        ]
    }

        ]

        # Add validation before creating buses
        for bus_data in buses:
            # Validate bus number
            if not isinstance(bus_data['bus_number'], str):
                raise ValueError(f"Invalid bus number format: {bus_data['bus_number']}")
            
            # Validate stops
            for stop in bus_data['stops']:
                if not isinstance(stop['name'], str):
                    raise ValueError(f"Invalid stop name in bus {bus_data['bus_number']}")
                if not len(stop['coordinates']) == 2:
                    raise ValueError(f"Invalid coordinates for stop {stop['name']}")
                lat, lon = stop['coordinates']
                if not (22.9 <= lat <= 23.2 and 72.4 <= lon <= 72.7):
                    raise ValueError(f"Coordinates out of Ahmedabad range for stop {stop['name']}")

        # Clear existing buses
        Bus.objects.all().delete()

        # Create new buses
        for bus_data in buses:
            Bus.objects.create(
                bus_number=bus_data['bus_number'],
                stops=bus_data['stops']
            )
            self.stdout.write(
                self.style.SUCCESS(f'Successfully created bus {bus_data["bus_number"]}')
            )