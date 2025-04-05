import datetime

class Book:
    def __init__(self, title, author, year, pages, quantity):
        self.title = title
        self.author = author
        self.year = year
        self.pages = pages
        self.quantity = quantity


class Student:
    def __init__(self, name):
        self.name = name
        self.borrowed_books = []


class Library:
    def __init__(self):
        self.books = []
        self.students = []

    def add_book(self, book):
        self.books.append(book)

    def edit_book(self, index, title=None, author=None, year=None, pages=None, quantity=None):
        if title:
            self.books[index].title = title
        if author:
            self.books[index].author = author
        if year:
            self.books[index].year = year
        if pages:
            self.books[index].pages = pages
        if quantity:
            self.books[index].quantity = quantity

    def remove_book(self, index):
        del self.books[index]

    def add_student(self, student):
        self.students.append(student)

    def borrow_book(self, student_name, book_title):
        student = next((s for s in self.students if s.name == student_name), None)
        book = next((b for b in self.books if b.title == book_title), None)
        if student and book and book.quantity > 0 and len(student.borrowed_books) < 5:
            student.borrowed_books.append((book, datetime.datetime.now()))
            book.quantity -= 1
            return True
        return False

    def return_book(self, student_name, book_title):
        student = next((s for s in self.students if s.name == student_name), None)
        if student:
            for i, (book, _) in enumerate(student.borrowed_books):
                if book.title == book_title:
                    student.borrowed_books.pop(i)
                    book.quantity += 1
                    return True
        return False

    def reminder(self):
        reminders_count = 0
        for student in self.students:
            for book, borrow_date in student.borrowed_books:
                if (datetime.datetime.now() - borrow_date).days > 30:
                    print(f"Przypomnienie: {student.name} powinien zwrócić '{book.title}'")
                    reminders_count += 1
        return reminders_count


    def borrow_book_with_date(self, student_name, book_title, borrow_date):
        student = next((s for s in self.students if s.name == student_name), None)
        book = next((b for b in self.books if b.title == book_title), None)
        if student and book and book.quantity > 0 and len(student.borrowed_books) < 5:
            student.borrowed_books.append((book, borrow_date))
            book.quantity -= 1
            return True
        return False


def main():
    library = Library()

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

    while True:
        print("\n==== SYSTEM BIBLIOTECZNY ====")
        print("1. Wyświetl wszystkie książki")
        print("2. Dodaj książkę")
        print("3. Edytuj książkę")
        print("4. Usuń książkę")
        print("5. Wypożycz książkę")
        print("6. Zwróć książkę")
        print("7. Sprawdź przypomnienia")
        print("8. Wyjście")

        choice = input("Wybierz opcję: ")

        if choice == "1":
            print("\n--- Lista książek ---")
            if not library.books:
                print("Brak książek w bibliotece")
            else:
                for i, book in enumerate(library.books):
                    print(
                        f"{i}. {book.title} - {book.author}, {book.year}, Strony: {book.pages}, Ilość: {book.quantity}")

        elif choice == "2":
            print("\n--- Dodawanie nowej książki ---")
            title = input("Podaj tytuł książki: ")
            author = input("Podaj autora: ")

            while True:
                try:
                    year = int(input("Podaj rok wydania: "))
                    break
                except ValueError:
                    print("Rok musi być liczbą całkowitą. Spróbuj ponownie.")

            while True:
                try:
                    pages = int(input("Podaj liczbę stron: "))
                    break
                except ValueError:
                    print("Liczba stron musi być liczbą całkowitą. Spróbuj ponownie.")

            while True:
                try:
                    quantity = int(input("Podaj ilość egzemplarzy: "))
                    break
                except ValueError:
                    print("Ilość egzemplarzy musi być liczbą całkowitą. Spróbuj ponownie.")

            new_book = Book(title, author, year, pages, quantity)
            library.add_book(new_book)
            print(f"Dodano książkę: {title}")

        elif choice == "3":
            print("\n--- Edycja książki ---")
            if not library.books:
                print("Brak książek do edycji")
            else:
                for i, book in enumerate(library.books):
                    print(f"{i}. {book.title} - {book.author}")

                try:
                    index = int(input("Podaj indeks książki do edycji: "))
                    if 0 <= index < len(library.books):
                        print(f"Edytuj książkę: {library.books[index].title}")

                        title = input(f"Nowy tytuł [{library.books[index].title}] (puste aby pozostawić bez zmian): ")
                        author = input(f"Nowy autor [{library.books[index].author}] (puste aby pozostawić bez zmian): ")

                        try:
                            year_input = input(
                                f"Nowy rok wydania [{library.books[index].year}] (puste aby pozostawić bez zmian): ")
                            year = int(year_input) if year_input else None
                        except ValueError:
                            print("Niepoprawny format roku. Pozostawiono bez zmian.")
                            year = None

                        try:
                            pages_input = input(
                                f"Nowa liczba stron [{library.books[index].pages}] (puste aby pozostawić bez zmian): ")
                            pages = int(pages_input) if pages_input else None
                        except ValueError:
                            print("Niepoprawny format liczby stron. Pozostawiono bez zmian.")
                            pages = None

                        try:
                            quantity_input = input(
                                f"Nowa ilość egzemplarzy [{library.books[index].quantity}] (puste aby pozostawić bez zmian): ")
                            quantity = int(quantity_input) if quantity_input else None
                        except ValueError:
                            print("Niepoprawny format ilości. Pozostawiono bez zmian.")
                            quantity = None

                        library.edit_book(index, title, author, year, pages, quantity)
                        print("Książka została zaktualizowana")
                    else:
                        print("Niepoprawny indeks")
                except ValueError:
                    print("Indeks musi być liczbą")

        elif choice == "4":
            print("\n--- Usuwanie książki ---")
            if not library.books:
                print("Brak książek do usunięcia")
            else:
                for i, book in enumerate(library.books):
                    print(f"{i}. {book.title} - {book.author}")

                try:
                    index = int(input("Podaj indeks książki do usunięcia: "))
                    if 0 <= index < len(library.books):
                        confirm = input(f"Czy na pewno chcesz usunąć '{library.books[index].title}'? (t/n): ")
                        if confirm.lower() == 't':
                            title = library.books[index].title
                            library.remove_book(index)
                            print(f"Książka '{title}' została usunięta")
                    else:
                        print("Niepoprawny indeks")
                except ValueError:
                    print("Indeks musi być liczbą")

        elif choice == "5":
            print("\n--- Wypożyczenie książki ---")
            print("Lista studentów:")
            for i, student in enumerate(library.students):
                print(f"{i}. {student.name} (wypożyczone książki: {len(student.borrowed_books)})")

            try:
                student_index = int(input("Wybierz studenta (podaj indeks): "))
                if 0 <= student_index < len(library.students):
                    student = library.students[student_index]

                    if len(student.borrowed_books) >= 5:
                        print(f"Student {student.name} ma już wypożyczone 5 książek. Nie może wypożyczyć więcej.")
                    else:
                        print("\nDostępne książki:")
                        available_books = [(i, book) for i, book in enumerate(library.books) if book.quantity > 0]
                        if not available_books:
                            print("Brak dostępnych książek")
                        else:
                            for i, book in available_books:
                                print(f"{i}. {book.title} - {book.author} (dostępne: {book.quantity})")

                            try:
                                book_index = int(input("Wybierz książkę do wypożyczenia (podaj indeks): "))
                                if 0 <= book_index < len(library.books) and library.books[book_index].quantity > 0:
                                    if library.borrow_book(student.name, library.books[book_index].title):
                                        print(
                                            f"Książka '{library.books[book_index].title}' została wypożyczona przez {student.name}")
                                    else:
                                        print("Nie udało się wypożyczyć książki")
                                else:
                                    print("Niepoprawny indeks lub książka niedostępna")
                            except ValueError:
                                print("Indeks musi być liczbą")
                else:
                    print("Niepoprawny indeks studenta")
            except ValueError:
                print("Indeks musi być liczbą")

        elif choice == "6":
            print("\n--- Zwrot książki ---")
            print("Lista studentów:")
            students_with_books = [(i, student) for i, student in enumerate(library.students) if student.borrowed_books]
            if not students_with_books:
                print("Żaden student nie ma wypożyczonych książek")
            else:
                for i, student in students_with_books:
                    print(f"{i}. {student.name} (wypożyczone książki: {len(student.borrowed_books)})")

                try:
                    student_index = int(input("Wybierz studenta (podaj indeks): "))
                    if 0 <= student_index < len(library.students) and library.students[student_index].borrowed_books:
                        student = library.students[student_index]

                        print("\nWypożyczone książki:")
                        for i, (book, date) in enumerate(student.borrowed_books):
                            days = (datetime.datetime.now() - date).days
                            print(f"{i}. {book.title} - wypożyczona {days} dni temu")

                        try:
                            book_index = int(input("Wybierz książkę do zwrotu (podaj indeks): "))
                            if 0 <= book_index < len(student.borrowed_books):
                                book_title = student.borrowed_books[book_index][0].title
                                if library.return_book(student.name, book_title):
                                    print(f"Książka '{book_title}' została zwrócona")
                                else:
                                    print("Nie udało się zwrócić książki")
                            else:
                                print("Niepoprawny indeks książki")
                        except ValueError:
                            print("Indeks musi być liczbą")
                    else:
                        print("Niepoprawny indeks studenta lub student nie ma wypożyczonych książek")
                except ValueError:
                    print("Indeks musi być liczbą")

        elif choice == "7":
            print("\n--- Przypomnienia o zwrocie książek ---")
            reminders = library.reminder()
            if not reminders:
                print("Brak przypomnień o zwrocie książek")

        elif choice == "8":
            print("\nDziękujemy za skorzystanie z systemu bibliotecznego. Do widzenia!")
            break

        else:
            print("Niepoprawna opcja. Wybierz ponownie.")

        input("\nNaciśnij Enter, aby kontynuować...")


if __name__ == "__main__":
    main()
