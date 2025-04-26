class Student:
    def __init__(self, name):
        self.name = name
        self.borrowed_books = []

    def __str__(self):
        return f"{self.name} (wypożyczonych książek: {len(self.borrowed_books)})"

    def has_max_books(self, max_books=5):
        return len(self.borrowed_books) >= max_books