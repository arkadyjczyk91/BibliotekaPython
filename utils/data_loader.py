import datetime
from models.book import Book
from models.student import Student

def load_sample_data(library):
    # Dodaj przykładowe książki
    for i in range(25):
        library.add_book(Book(f"Książka {i + 1}", f"Autor {i + 1}", 2000 + i, 100 + i, 5))

    # Dodaj przykładowych studentów
    for i in range(15):
        library.add_student(Student(f"Student {i + 1}"))

    # Dodaj kilka wypożyczeń do testowania przypomnień
    # Książki wypożyczone ponad 30 dni temu (wyzwolą przypomnienia)
    library.borrow_book_with_date("Student 1", "Książka 1", datetime.datetime.now() - datetime.timedelta(days=35))
    library.borrow_book_with_date("Student 2", "Książka 2", datetime.datetime.now() - datetime.timedelta(days=40))
    library.borrow_book_with_date("Student 3", "Książka 3", datetime.datetime.now() - datetime.timedelta(days=60))

    # Książki wypożyczone niedawno (nie wyzwolą przypomnień)
    library.borrow_book_with_date("Student 4", "Książka 4", datetime.datetime.now() - datetime.timedelta(days=10))
    library.borrow_book_with_date("Student 5", "Książka 5", datetime.datetime.now() - datetime.timedelta(days=5))