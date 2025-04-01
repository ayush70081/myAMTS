# MyAMTS - Ahmedabad Municipal Transport Service App

MyAMTS is a Django web application that provides a digital platform for the Ahmedabad Municipal Transport Service, allowing users to search for bus routes, track buses in real-time, book tickets online, and more.

## Features

- **Bus Route Search**: Find direct routes and routes with transfers between any two stops
- **Real-time Bus Tracking**: Track the current location and status of buses
- **Online Ticket Booking**: Book bus tickets online with secure payment processing
- **QR Code Tickets**: Generate and display QR code tickets for easy verification
- **User Profile Management**: Register, login, and manage user profiles
- **Search History**: View recent search history for faster access to frequent routes
- **Nearby Stops**: Find bus stops near your current location using geolocation

## Technical Stack

- **Backend**: Django (Python web framework)
- **Database**: Compatible with SQLite (development) and PostgreSQL (production)
- **Frontend**: HTML, CSS, JavaScript
- **Maps Integration**: Geolocation services for finding nearby stops
- **Authentication**: Django's built-in authentication system

## Project Structure

- `myAMTS/`: Django project settings
- `my_amts/`: Main application package
  - `models.py`: Data models for Bus, ActiveBus, Booking, Ticket, etc.
  - `views.py`: View functions for handling HTTP requests
  - `route_finder.py`: Algorithm for finding routes between stops
  - `urls.py`: URL routing configuration
  - `ticket_utils.py`: Utilities for ticket generation and management
  - `templates/`: HTML templates
  - `static/`: Static files (CSS, JS, images)

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/myAMTS.git
   cd myAMTS
   ```

2. Create a virtual environment and activate it:
   ```
   python -m venv venv
   # On Windows
   venv\Scripts\activate
   # On macOS/Linux
   source venv/bin/activate
   ```

3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

4. Apply database migrations:
   ```
   python manage.py migrate
   ```

5. Create a superuser for admin access:
   ```
   python manage.py createsuperuser
   ```

6. Run the development server:
   ```
   python manage.py runserver
   ```

7. Access the application at http://127.0.0.1:8000/

## Usage

1. Register a new user account or login with existing credentials
2. Use the search form to find bus routes between stops
3. View available routes and select one to book
4. Complete the booking process and receive a QR code ticket
5. Access your tickets and booking history from your profile

## Admin Interface

The admin interface is available at http://127.0.0.1:8000/admin/ and provides:

- Bus management (add/edit bus routes and stops)
- Active bus status management
- User management
- Booking and ticket management

## License

[license information]

## Contributors

[Ayush Patel](https://github.com/ayush70081)

