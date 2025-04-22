class Screen:
    def __init__(self, screen_number, seating_capacity):
        self.screen_number = screen_number
        self.seating_capacity = seating_capacity
        self.showings = []  # List of tuples (Film, show_time)

    def add_showing(self, film, show_time):
        self.showings.append((film, show_time))

    def remove_showing(self, film_title, show_time):
        self.showings = [
            (film, time) for (film, time) in self.showings
            if not (film.title == film_title and time == show_time)
        ]

    def get_showings(self):
        return self.showings

    def __repr__(self):
        return f"Screen(number={self.screen_number}, capacity={self.seating_capacity})"
