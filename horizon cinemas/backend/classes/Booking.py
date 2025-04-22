import random

class Booking:
    def __init__(self, film, screen, show_time, num_tickets, seat_numbers):
        self.film = film
        self.screen = screen
        self.show_time = show_time
        self.num_tickets = num_tickets
        self.seat_numbers = seat_numbers
        self.booking_reference = self.generate_reference()

    def generate_reference(self):
        return f"REF{random.randint(1000, 9999)}"

    def __repr__(self):
        return (f"Booking(ref={self.booking_reference}, film={self.film.title}, "
                f"screen={self.screen.screen_number}, show_time={self.show_time}, "
                f"tickets={self.num_tickets})")
