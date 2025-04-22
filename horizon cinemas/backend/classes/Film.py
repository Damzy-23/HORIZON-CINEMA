class Film:
    def __init__(self, title, description, genre, rating, actors):
        self.title = title
        self.description = description
        self.genre = genre
        self.rating = rating
        self.actors = actors  # List of actor names

    def update_rating(self, new_rating):
        self.rating = new_rating

    def __repr__(self):
        return f"Film(title={self.title}, genre={self.genre}, rating={self.rating})"
