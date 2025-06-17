class Book:
    def __init__(self, book_id, title, author):
        self.book_id = book_id
        self.title = title
        self.author = author
        self.is_available = True

class User:
    def __init__(self, user_id, name):
        self.user_id = user_id
        self.name = name
        self.borrowed_books = []

class Library:
    def __init__(self):
        self.books = {}  # book_id -> Book
        self.users = {}  # user_id -> User

    def search_books(self, title):
        return [book for book in self.books.values() if title.lower() in book.title.lower()]

    def borrow_book(self, user_id, book_id):
        if book_id not in self.books or user_id not in self.users:
            return "Invalid request"
        book = self.books[book_id]
        user = self.users[user_id]
        if not book.is_available:
            return "Book not available"
        book.is_available = False
        user.borrowed_books.append(book_id)
        return "Borrowed successfully"

    def return_book(self, user_id, book_id):
        if book_id not in self.books or user_id not in self.users:
            return "Invalid request"
        book = self.books[book_id]
        user = self.users[user_id]
        if book_id not in user.borrowed_books:
            return "Book not borrowed by user"
        book.is_available = True
        user.borrowed_books.remove(book_id)
        return "Returned successfully"


