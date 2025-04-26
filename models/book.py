class Book:
    def __init__(self, title, author, year, pages, quantity):
        self.title = title
        self.author = author
        self.year = year
        self.pages = pages
        self.quantity = quantity

    def __str__(self):
        return f"{self.title} - {self.author}, {self.year}, stron: {self.pages}, dostępnych: {self.quantity}"