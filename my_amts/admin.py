from django.contrib import admin
from .models import Bus, ActiveBus, Booking, Ticket

# Register models with the default admin site
admin.site.register(Bus)
admin.site.register(ActiveBus)
admin.site.register(Booking)
admin.site.register(Ticket)
