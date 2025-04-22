from Screen import Screen

class Cinema:
    def __init__(self, name, city):
        self.name = name
        self.city = city
        self.screens = []  # List of Screen objects

    def add_screen(self, screen):
        if isinstance(screen, Screen):
            self.screens.append(screen)
        else:
            raise TypeError("Expected a Screen instance")

    def remove_screen(self, screen_number):
        self.screens = [screen for screen in self.screens if screen.screen_number != screen_number]

    def get_screens(self):
        return self.screens

    def __repr__(self):
        return f"Cinema(name={self.name}, city={self.city}, screens={len(self.screens)})"
