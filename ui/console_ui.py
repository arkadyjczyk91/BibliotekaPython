import datetime

class ConsoleUI:
    def __init__(self, library):
        self.library = library

    def get_int_input(self, prompt, min_value=None, max_value=None):
        while True:
            try:
                value = input(prompt)
                if not value.strip():  # Pusty ciąg znaków
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

    def display_menu(self):
        print("\n==== SYSTEM BIBLIOTECZNY ====")
        print("1. Wyświetl wszystkie książki")
        print("2. Dodaj książkę")
        print("3. Edytuj książkę")
        print("4. Usuń książkę")
        print("5. Wypożycz książkę")
        print("6. Zwróć książkę")
        print("7. Sprawdź przypomnienia")
        print("8. Wyjście")

        return self.get_int_input("Wybierz opcję: ", 1, 8)

    def display_books(self):
        print("\n--- Lista książek ---")
        if not self.library.books:
            print("Brak książek w bibliotece")
        else:
            for i, book in enumerate(self.library.books):
                print(f"{i}. {book}")

    def add_book_ui(self):
        print("\n--- Dodawanie nowej książki ---")
        title = input("Podaj tytuł książki: ")
        author = input("Podaj autora: ")
        year = self.get_int_input("Podaj rok wydania: ")
        pages = self.get_int_input("Podaj liczbę stron: ", min_value=1)
        quantity = self.get_int_input("Podaj ilość egzemplarzy: ", min_value=0)

        if not title or not author or not year or not pages or quantity is None:
            print("Nie podano wszystkich wymaganych danych")
            return

        from models.book import Book
        new_book = Book(title, author, year, pages, quantity)
        if self.library.add_book(new_book):
            print(f"Dodano książkę: {title}")

    def edit_book_ui(self):
        print("\n--- Edycja książki ---")
        if not self.library.books:
            print("Brak książek do edycji")
            return

        self.display_books()
        index = self.get_int_input("Podaj indeks książki do edycji: ", 0, len(self.library.books) - 1)

        if index is None:
            return

        book = self.library.books[index]
        print(f"Edytuj książkę: {book.title}")

        title = input(f"Nowy tytuł [{book.title}] (puste aby pozostawić bez zmian): ")
        author = input(f"Nowy autor [{book.author}] (puste aby pozostawić bez zmian): ")
        year = self.get_int_input(f"Nowy rok wydania [{book.year}] (puste aby pozostawić bez zmian): ")
        pages = self.get_int_input(f"Nowa liczba stron [{book.pages}] (puste aby pozostawić bez zmian): ", min_value=1)
        quantity = self.get_int_input(f"Nowa ilość egzemplarzy [{book.quantity}] (puste aby pozostawić bez zmian): ", min_value=0)

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
        index = self.get_int_input("Podaj indeks książki do usunięcia: ", 0, len(self.library.books) - 1)

        if index is None:
            return

        confirm = input(f"Czy na pewno chcesz usunąć '{self.library.books[index].title}'? (t/n): ")
        if confirm.lower() == 't':
            title = self.library.books[index].title
            if self.library.remove_book(index):
                print(f"Książka '{title}' została usunięta")
            else:
                print("Nie udało się usunąć książki")

    def borrow_book_ui(self):
        print("\n--- Wypożyczenie książki ---")
        print("Lista studentów:")
        for i, student in enumerate(self.library.students):
            print(f"{i}. {student}")

        student_index = self.get_int_input("Wybierz studenta (podaj indeks): ", 0, len(self.library.students) - 1)
        if student_index is None:
            return

        student = self.library.students[student_index]
        if student.has_max_books(self.library.MAX_BOOKS_PER_STUDENT):
            print(f"Student {student.name} ma już wypożyczone {self.library.MAX_BOOKS_PER_STUDENT} książek. "
                  f"Nie może wypożyczyć więcej.")
            return

        available_books = self.library.get_available_books()
        if not available_books:
            print("Brak dostępnych książek")
            return

        print("\nDostępne książki:")
        for i, book in enumerate(available_books):
            print(f"{i}. {book}")

        book_index = self.get_int_input("Wybierz książkę do wypożyczenia (podaj indeks): ",
                                        0, len(available_books) - 1)
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

        if not students_with_books:
            print("Żaden student nie ma wypożyczonych książek")
            return

        print("Lista studentów z wypożyczonymi książkami:")
        for i, student in enumerate(students_with_books):
            print(f"{i}. {student}")

        student_index = self.get_int_input("Wybierz studenta (podaj indeks): ",
                                          0, len(students_with_books) - 1)
        if student_index is None:
            return

        student = students_with_books[student_index]
        print("\nWypożyczone książki:")

        for i, (book, date) in enumerate(student.borrowed_books):
            days = (datetime.datetime.now() - date).days
            print(f"{i}. {book.title} - wypożyczona {days} dni temu")

        book_index = self.get_int_input("Wybierz książkę do zwrotu (podaj indeks): ",
                                       0, len(student.borrowed_books) - 1)
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
        while True:
            choice = self.display_menu()

            if choice == 1:
                self.display_books()
            elif choice == 2:
                self.add_book_ui()
            elif choice == 3:
                self.edit_book_ui()
            elif choice == 4:
                self.remove_book_ui()
            elif choice == 5:
                self.borrow_book_ui()
            elif choice == 6:
                self.return_book_ui()
            elif choice == 7:
                self.check_reminders_ui()
            elif choice == 8:
                print("\nDziękujemy za skorzystanie z systemu bibliotecznego. Do widzenia!")
                break

            input("\nNaciśnij Enter, aby kontynuować...")