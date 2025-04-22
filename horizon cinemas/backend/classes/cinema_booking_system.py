import json

class User:
    def __init__(self, username, password, role):
        self.username = username
        self.password = password
        self.role = role

class Film:
    def __init__(self, title, description, genre, rating, actors):
        self.title = title
        self.description = description
        self.genre = genre
        self.rating = rating
        self.actors = actors

class Screen:
    def __init__(self, screen_number, seating_capacity):
        self.screen_number = screen_number
        self.seating_capacity = seating_capacity
        self.showings = []

    def add_showing(self, film, show_time):
        self.showings.append((film, show_time))

class Cinema:
    def __init__(self, name, city):
        self.name = name
        self.city = city
        self.screens = []

    def add_screen(self, screen):
        self.screens.append(screen)

class Booking:
    def __init__(self, film, screen, show_time, num_tickets, seat_numbers):
        self.film = film
        self.screen = screen
        self.show_time = show_time
        self.num_tickets = num_tickets
        self.seat_numbers = seat_numbers
        self.booking_reference = self.generate_reference()

    def generate_reference(self):
        import random
        return f"REF{random.randint(1000, 9999)}"

class CinemaManager:
    def __init__(self, filename='cinema_data.json'):
        self.filename = filename
        self.cinemas = []
        self.users = []  # List to hold user accounts
        self.bookings = [] # List to hold all bookings
        self.load_data()

    def load_data(self):
        try:
            with open(self.filename, 'r') as file:
                data = json.load(file)
                for cinema_data in data['cinemas']:
                    cinema = Cinema(cinema_data['name'], cinema_data['city'])
                    for screen_data in cinema_data['screens']:
                        screen = Screen(screen_data['screen_number'], screen_data['seating_capacity'])
                        cinema.add_screen(screen)
                    self.cinemas.append(cinema)
        except FileNotFoundError:
            self.cinemas = []

        # Load users (for demonstration purposes, hardcoded users)
        self.users.append(User("admin", "adminpass", "Admin"))
        self.users.append(User("manager", "managerpass", "Manager"))
        self.users.append(User("staff", "staffpass", "Booking Staff"))

    def save_data(self):
        data = {'cinemas': []}
        for cinema in self.cinemas:
            cinema_data = {
                'name': cinema.name,
                'city': cinema.city,
                'screens': [{'screen_number': screen.screen_number, 'seating_capacity': screen.seating_capacity} for screen in cinema.screens]
            }
            data['cinemas'].append(cinema_data)
        with open(self.filename, 'w') as file:
            json.dump(data, file)

    def authenticate_user(self, username, password):
        for user in self.users:
            if user.username == username and user.password == password:
                return user
        return None

    def add_film(self, cinema_name, film):
        for cinema in self.cinemas:
            if cinema.name == cinema_name:
                for screen in cinema.screens:
                    screen.showings.append((film, None))  # Add film to the screen without a specific show time
                self.save_data()
                return True
        return False

    def remove_film(self, cinema_name, film_title):
        for cinema in self.cinemas:
            if cinema.name == cinema_name:
                for screen in cinema.screens:
                    screen.showings = [show for show in screen.showings if show[0].title != film_title]
                self.save_data()
                return True
        return False

    def add_cinema(self, cinema_name, city):
        new_cinema = Cinema(cinema_name, city)
        self.cinemas.append(new_cinema)
        self.save_data()

    def remove_cinema(self, cinema_name):
        self.cinemas = [cinema for cinema in self.cinemas if cinema.name != cinema_name]
        self.save_data()

    def add_showing_to_screen(self, cinema_name, screen_number, film_title, show_time):
        for cinema in self.cinemas:
            if cinema.name == cinema_name:
                for screen in cinema.screens:
                    if screen.screen_number == int(screen_number):
                        film_to_show = None
                        for showing_film, _ in screen.showings: # check if film already exists in showings
                            if showing_film.title == film_title:
                                film_to_show = showing_film
                                break
                        if not film_to_show: # if film not in showings, find from available films (assuming films are managed elsewhere or pre-populated)
                            film_to_show = Film(film_title, "Description needed", "Genre needed", "Rating needed", []) # create a placeholder film if not found. In real app, film list should be managed properly.

                        screen.add_showing(film_to_show, show_time)
                        self.save_data()
                        return True
                return False # Screen not found
        return False # Cinema not found

    def remove_showing_from_screen(self, cinema_name, screen_number, film_title, show_time):
        for cinema in self.cinemas:
            if cinema.name == cinema_name:
                for screen in cinema.screens:
                    if screen.screen_number == int(screen_number):
                        screen.showings = [
                            showing for showing in screen.showings
                            if not (showing[0].title == film_title and showing[1] == show_time)
                        ]
                        self.save_data()
                        return True
                return False # Screen not found
        return False # Cinema not found

    def generate_film_booking_report(self):
        film_booking_counts = {}
        for booking in self.bookings:
            film_title = booking.film.title
            film_booking_counts[film_title] = film_booking_counts.get(film_title, 0) + 1
        return film_booking_counts

    def add_booking(self, booking): # Method to add booking to CinemaManager's bookings list
        self.bookings.append(booking)