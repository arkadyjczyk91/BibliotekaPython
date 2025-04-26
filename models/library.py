import datetime
from models.book import Book
from models.student import Student


class Library:
    def __init__(self):
        self.books = []
        self.students = []
        self.MAX_BOOKS_PER_STUDENT = 5
        self.REMINDER_DAYS = 30

    def add_book(self, book):
        self.books.append(book)
        return True

    def edit_book(self, index, title=None, author=None, year=None, pages=None, quantity=None):
        if not 0 <= index < len(self.books):
            return False

        if title:
            self.books[index].title = title
        if author:
            self.books[index].author = author
        if year:
            self.books[index].year = year
        if pages:
            self.books[index].pages = pages
        if quantity is not None:
            self.books[index].quantity = quantity
        return True

    def remove_book(self, index):
        if not 0 <= index < len(self.books):
            return False
        del self.books[index]
        return True

    def add_student(self, student):
        self.students.append(student)
        return True

    def get_student_by_name(self, student_name):
        return next((s for s in self.students if s.name == student_name), None)

    def get_book_by_title(self, book_title):
        return next((b for b in self.books if b.title == book_title), None)

    def borrow_book(self, student_name, book_title):
        return self.borrow_book_with_date(student_name, book_title, datetime.datetime.now())

    def borrow_book_with_date(self, student_name, book_title, borrow_date):
        student = self.get_student_by_name(student_name)
        book = self.get_book_by_title(book_title)

        if not student or not book:
            return False

        if book.quantity <= 0:
            return False

        if student.has_max_books(self.MAX_BOOKS_PER_STUDENT):
            return False

        student.borrowed_books.append((book, borrow_date))
        book.quantity -= 1
        return True

    def return_book(self, student_name, book_title):
        student = self.get_student_by_name(student_name)
        if not student:
            return False

        for i, (book, _) in enumerate(student.borrowed_books):
            if book.title == book_title:
                student.borrowed_books.pop(i)
                book.quantity += 1
                return True
        return False

    def get_reminders(self):
        today = datetime.datetime.now()
        reminders = []

        for student in self.students:
            for book, borrow_date in student.borrowed_books:
                days_borrowed = (today - borrow_date).days
                if days_borrowed > self.REMINDER_DAYS:
                    reminders.append({
                        "student": student,
                        "book": book,
                        "days": days_borrowed
                    })
        return reminders

    def print_reminders(self):
        reminders = self.get_reminders()
        for reminder in reminders:
            print(f"Przypomnienie: {reminder['student'].name} powinien zwrócić "
                  f"'{reminder['book'].title}' (wypożyczone {reminder['days']} dni temu)")
        return len(reminders)

    def get_available_books(self):
        return [book for book in self.books if book.quantity > 0]

    def get_students_with_books(self):
        return [student for student in self.students if student.borrowed_books]