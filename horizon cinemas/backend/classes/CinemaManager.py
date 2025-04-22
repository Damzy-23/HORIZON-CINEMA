import json
from User import User
from Film import Film
from Screen import Screen
from Cinema import Cinema
from Booking import Booking

class CinemaManager:
    def __init__(self, filename='cinema_data.json'):
        self.filename = filename
        self.cinemas = []
        self.users = []
        self.bookings = []
        self.load_data()
        self.load_default_users()
        self.preload_movies_and_showings()

    def preload_movies_and_showings(self):
        import datetime
        from Film import Film
        from Screen import Screen

        # Create 7 films
        films = [
            Film("The Great Adventure", "An epic journey.", "Adventure", "PG-13", ["Actor A", "Actor B"]),
            Film("Romantic Escape", "A love story.", "Romance", "PG", ["Actor C", "Actor D"]),
            Film("Mystery Manor", "A thrilling mystery.", "Mystery", "PG-13", ["Actor E", "Actor F"]),
            Film("Sci-Fi Saga", "A space odyssey.", "Sci-Fi", "PG-13", ["Actor G", "Actor H"]),
            Film("Comedy Nights", "Laugh out loud.", "Comedy", "PG", ["Actor I", "Actor J"]),
            Film("Horror House", "Spooky tales.", "Horror", "R", ["Actor K", "Actor L"]),
            Film("Animated Fun", "Family animation.", "Animation", "G", ["Actor M", "Actor N"]),
        ]

        # Create a cinema and screen if none exist
        if not self.cinemas:
            cinema = Cinema("Horizon Cinema", "Your City")
            screen1 = Screen(1, 100)
            cinema.add_screen(screen1)
            self.cinemas.append(cinema)
        else:
            cinema = self.cinemas[0]
            if not cinema.screens:
                screen1 = Screen(1, 100)
                cinema.add_screen(screen1)
            else:
                screen1 = cinema.screens[0]

        # Add films with show times from today to end of May
        today = datetime.date.today()
        end_date = datetime.date(today.year, 5, 31)
        delta = datetime.timedelta(days=1)

        current_date = today
        film_index = 0
        while current_date <= end_date:
            show_time = current_date.strftime("%Y-%m-%d") + " 19:00"
            film = films[film_index % len(films)]
            screen1.add_showing(film, show_time)
            current_date += delta
            film_index += 1
        self.save_data()

    def load_data(self):
        try:
            with open(self.filename, 'r') as file:
                data = json.load(file)
                for cinema_data in data.get('cinemas', []):
                    cinema = Cinema(cinema_data['name'], cinema_data['city'])
                    for screen_data in cinema_data.get('screens', []):
                        screen = Screen(screen_data['screen_number'], screen_data['seating_capacity'])
                        cinema.add_screen(screen)
                    self.cinemas.append(cinema)

                # Load users from data
                self.users = []
                for user_data in data.get('users', []):
                    user = User.from_dict(user_data)
                    self.users.append(user)
        except FileNotFoundError:
            self.cinemas = []
            self.users = []

    def save_data(self):
        data = {'cinemas': [], 'users': []}
        for cinema in self.cinemas:
            cinema_data = {
                'name': cinema.name,
                'city': cinema.city,
                'screens': [{'screen_number': screen.screen_number, 'seating_capacity': screen.seating_capacity} for screen in cinema.screens]
            }
            data['cinemas'].append(cinema_data)

        # Save users to data
        for user in self.users:
            data['users'].append(user.to_dict())

        with open(self.filename, 'w') as file:
            json.dump(data, file, indent=4)

    def load_default_users(self):
        self.users.append(User("admin", "adminpass", "Admin"))
        self.users.append(User("manager", "managerpass", "Manager"))
        self.users.append(User("staff", "staffpass", "Booking Staff"))

    def authenticate_user(self, username, password):
        for user in self.users:
            if user.username == username and user.check_password(password):
                return user
        return None

    def add_user(self, username, password, role="User"):
        # Check if username already exists
        if any(user.username == username for user in self.users):
            return False
        new_user = User(username, password, role)
        self.users.append(new_user)
        self.save_data()
        return True

    def add_cinema(self, cinema_name, city):
        new_cinema = Cinema(cinema_name, city)
        self.cinemas.append(new_cinema)
        self.save_data()

    def remove_cinema(self, cinema_name):
        self.cinemas = [cinema for cinema in self.cinemas if cinema.name != cinema_name]
        self.save_data()

    def add_film(self, cinema_name, film):
        for cinema in self.cinemas:
            if cinema.name == cinema_name:
                for screen in cinema.screens:
                    screen.add_showing(film, None)
                self.save_data()
                return True
        return False

    def remove_film(self, cinema_name, film_title):
        for cinema in self.cinemas:
            if cinema.name == cinema_name:
                for screen in cinema.screens:
                    screen.remove_showing(film_title, None)
                self.save_data()
                return True
        return False

    def add_showing_to_screen(self, cinema_name, screen_number, film_title, show_time):
        for cinema in self.cinemas:
            if cinema.name == cinema_name:
                for screen in cinema.screens:
                    if screen.screen_number == int(screen_number):
                        film_to_show = None
                        for showing_film, _ in screen.showings:
                            if showing_film.title == film_title:
                                film_to_show = showing_film
                                break
                        if not film_to_show:
                            film_to_show = Film(film_title, "Description needed", "Genre needed", "Rating needed", [])
                        screen.add_showing(film_to_show, show_time)
                        self.save_data()
                        return True
                return False
        return False

    def remove_showing_from_screen(self, cinema_name, screen_number, film_title, show_time):
        for cinema in self.cinemas:
            if cinema.name == cinema_name:
                for screen in cinema.screens:
                    if screen.screen_number == int(screen_number):
                        screen.remove_showing(film_title, show_time)
                        self.save_data()
                        return True
                return False
        return False

    def add_booking(self, booking):
        self.bookings.append(booking)

    def generate_film_booking_report(self):
        film_booking_counts = {}
        for booking in self.bookings:
            film_title = booking.film.title
            film_booking_counts[film_title] = film_booking_counts.get(film_title, 0) + 1
        return film_booking_counts
