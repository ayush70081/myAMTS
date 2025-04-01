# my_amts/urls.py
from django.urls import path, include
from . import views
from . import ticket_views

urlpatterns = [
    path('', views.home, name='home'),  # This will be the landing page
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),
    path('search/', views.search_view, name='search'),
    path('api/search/', views.search_buses, name='search_buses'),
    path('api/buses/<str:bus_number>/active/', views.get_active_buses, name='active_buses'),
    path('book-ticket/', ticket_views.book_ticket, name='book_ticket'),
    path('tickets/', ticket_views.ticket_list, name='ticket_list'),
    path('ticket/<uuid:ticket_id>/', ticket_views.ticket_detail, name='ticket_detail'),
    path('verify-ticket/<uuid:ticket_id>/', ticket_views.verify_ticket, name='verify_ticket'),
    path('api/create-booking/', views.create_booking, name='create_booking'),
    path('my-bookings/', views.my_bookings, name='my_bookings'),
    path('api/nearby-stops/', views.get_nearby_stops, name='nearby_stops'),
    path('bus-details/', views.bus_details, name='bus_details'),
    path('available-buses/', views.get_available_buses, name='available_buses'),
    path('profile/', views.profile_view, name='profile'),
    path('profile/edit/', views.edit_profile_view, name='edit_profile'),
]