import datetime
from models.book import Book

def get_int_input(prompt, min_value=None, max_value=None):
    while True:
        try:
            value = input(prompt)
            if not value.strip():
                return None
            value = int(value)

            if min_value is not None and value < min_value:
                print(f"Wartość musi być większa lub równa {min_value}")
                continue

            if max_value is not None and value > max_value:
                print(f"Wartość musi być mniejsza lub równa {max_value}")
                continue

            return value
        except ValueError:
            print("Wprowadź poprawną liczbę całkowitą")


class ConsoleUI:
    def __init__(self, library):
        self.library = library

    def display_menu(self):
        menu_options = [
            "Wyświetl wszystkie książki",
            "Dodaj książkę",
            "Edytuj książkę",
            "Usuń książkę",
            "Wypożycz książkę",
            "Zwróć książkę",
            "Sprawdź przypomnienia",
            "Wyjście"
        ]

        print("\n==== SYSTEM BIBLIOTECZNY ====")
        for i, option in enumerate(menu_options, 1):
            print(f"{i}. {option}")

        return get_int_input("Wybierz opcję: ", 1, len(menu_options))

    def display_books(self):
        print("\n--- Lista książek ---")
        if not self.library.books:
            print("Brak książek w bibliotece")
            return

        for i, book in enumerate(self.library.books):
            print(f"{i}. {book}")

    def add_book_ui(self):
        print("\n--- Dodawanie nowej książki ---")
        title = input("Podaj tytuł książki: ")
        author = input("Podaj autora: ")
        year = get_int_input("Podaj rok wydania: ")
        pages = get_int_input("Podaj liczbę stron: ", min_value=1)
        quantity = get_int_input("Podaj ilość egzemplarzy: ", min_value=0)

        if not title or not author or not year or not pages or quantity is None:
            print("Nie podano wszystkich wymaganych danych")
            return

        if self.library.create_and_add_book(title, author, year, pages, quantity):
            print(f"Dodano książkę: {title}")

    def edit_book_ui(self):
        print("\n--- Edycja książki ---")
        if not self.library.books:
            print("Brak książek do edycji")
            return

        self.display_books()
        index = get_int_input("Podaj indeks książki do edycji: ", 0, len(self.library.books) - 1)
        if index is None:
            return

        book = self.library.books[index]
        print(f"Edytuj książkę: {book.title}")

        title = input(f"Nowy tytuł [{book.title}] (puste aby pozostawić bez zmian): ")
        author = input(f"Nowy autor [{book.author}] (puste aby pozostawić bez zmian): ")
        year = get_int_input(f"Nowy rok wydania [{book.year}] (puste aby pozostawić bez zmian): ")
        pages = get_int_input(f"Nowa liczba stron [{book.pages}] (puste aby pozostawić bez zmian): ", min_value=1)
        quantity = get_int_input(f"Nowa ilość egzemplarzy [{book.quantity}] (puste aby pozostawić bez zmian): ",
                                      min_value=0)

        if self.library.edit_book(index, title, author, year, pages, quantity):
            print("Książka została zaktualizowana")
        else:
            print("Nie udało się zaktualizować książki")

    def remove_book_ui(self):
        print("\n--- Usuwanie książki ---")
        if not self.library.books:
            print("Brak książek do usunięcia")
            return

        self.display_books()
        index = get_int_input("Podaj indeks książki do usunięcia: ", 0, len(self.library.books) - 1)
        if index is None:
            return

        confirm = input(f"Czy na pewno chcesz usunąć '{self.library.books[index].title}'? (t/n): ")
        if confirm.lower() == 't':
            title = self.library.books[index].title
            if self.library.remove_book(index):
                print(f"Książka '{title}' została usunięta")
            else:
                print("Nie udało się usunąć książki")

    def _display_items_with_index(self, items, header, empty_msg):
        print(header)
        if not items:
            print(empty_msg)
            return False

        for i, item in enumerate(items):
            print(f"{i}. {item}")
        return True

    def borrow_book_ui(self):
        print("\n--- Wypożyczenie książki ---")

        if not self._display_items_with_index(self.library.students, "Lista studentów:", "Brak studentów"):
            return

        student_index = get_int_input("Wybierz studenta (podaj indeks): ", 0, len(self.library.students) - 1)
        if student_index is None:
            return

        student = self.library.students[student_index]
        if student.has_max_books(self.library.MAX_BOOKS_PER_STUDENT):
            print(f"Student {student.name} ma już wypożyczone {self.library.MAX_BOOKS_PER_STUDENT} książek. "
                  f"Nie może wypożyczyć więcej.")
            return

        available_books = self.library.get_available_books()
        if not self._display_items_with_index(available_books, "\nDostępne książki:", "Brak dostępnych książek"):
            return

        book_index = get_int_input("Wybierz książkę do wypożyczenia (podaj indeks): ", 0, len(available_books) - 1)
        if book_index is None:
            return

        selected_book = available_books[book_index]
        if self.library.borrow_book(student.name, selected_book.title):
            print(f"Książka '{selected_book.title}' została wypożyczona przez {student.name}")
        else:
            print("Nie udało się wypożyczyć książki")

    def return_book_ui(self):
        print("\n--- Zwrot książki ---")
        students_with_books = self.library.get_students_with_books()

        if not self._display_items_with_index(students_with_books,
                                              "Lista studentów z wypożyczonymi książkami:",
                                              "Żaden student nie ma wypożyczonych książek"):
            return

        student_index = get_int_input("Wybierz studenta (podaj indeks): ", 0, len(students_with_books) - 1)
        if student_index is None:
            return

        student = students_with_books[student_index]
        print("\nWypożyczone książki:")

        for i, (book, date) in enumerate(student.borrowed_books):
            days = (datetime.datetime.now() - date).days
            print(f"{i}. {book.title} - wypożyczona {days} dni temu")

        book_index = get_int_input("Wybierz książkę do zwrotu (podaj indeks): ", 0,
                                        len(student.borrowed_books) - 1)
        if book_index is None:
            return

        book_title = student.borrowed_books[book_index][0].title
        if self.library.return_book(student.name, book_title):
            print(f"Książka '{book_title}' została zwrócona")
        else:
            print("Nie udało się zwrócić książki")

    def check_reminders_ui(self):
        print("\n--- Przypomnienia o zwrocie książek ---")
        reminders = self.library.print_reminders()
        if not reminders:
            print("Brak przypomnień o zwrocie książek")

    def run(self):
        menu_handlers = {
            1: self.display_books,
            2: self.add_book_ui,
            3: self.edit_book_ui,
            4: self.remove_book_ui,
            5: self.borrow_book_ui,
            6: self.return_book_ui,
            7: self.check_reminders_ui
        }

        while True:
            choice = self.display_menu()

            if choice == 8:
                print("\nDziękujemy za skorzystanie z systemu bibliotecznego. Do widzenia!")
                break

            handler = menu_handlers.get(choice)
            if handler:
                handler()

            input("\nNaciśnij Enter, aby kontynuować...")