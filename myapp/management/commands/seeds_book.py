from django.core.management.base import BaseCommand
from myapp.models import Book

class Command(BaseCommand):
    help = 'Adds sample books to the database'

    def handle(self, *args, **options):
        sample_books = [
            {
                'title': 'The Great Gatsby',
                'author': 'F. Scott Fitzgerald',
                'description': 'A classic American novel set in the Jazz Age',
                'publish_year': 1925,
                'cover_image': 'https://images.unsplash.com/photo-1544947950-fa07a98d237f'
            },
            {
                'title': 'To Kill a Mockingbird', 
                'author': 'Harper Lee',
                'description': 'A story about racial injustice and moral growth',
                'publish_year': 1960,
                'cover_image': 'https://images.unsplash.com/photo-1481627834876-b7833e8f5570'
            },
            {
                'title': '1984',
                'author': 'George Orwell',
                'description': 'Dystopian novel about totalitarianism and surveillance',
                'publish_year': 1949,
                'cover_image': 'https://images.unsplash.com/photo-1532012197267-da84d127e765'
            },
            {
                'title': 'Pride and Prejudice',
                'author': 'Jane Austen',
                'description': 'Romantic novel about Elizabeth Bennet and Mr. Darcy',
                'publish_year': 1813,
                'cover_image': 'https://images.unsplash.com/photo-1541963463532-d68292c34b19'
            },
            {
                'title': 'The Hobbit',
                'author': 'J.R.R. Tolkien',
                'description': 'Fantasy novel about Bilbo Baggins adventure',
                'publish_year': 1937,
                'cover_image': 'https://images.unsplash.com/photo-1543002588-bfa74002ed7e'
            },
            {
                'title': 'Harry Potter and the Philosopher\'s Stone',
                'author': 'J.K. Rowling',
                'description': 'First book in the Harry Potter series',
                'publish_year': 1997,
                'cover_image': 'https://images.unsplash.com/photo-1621447504864-d8686e12698c'
            },
            {
                'title': 'The Catcher in the Rye',
                'author': 'J.D. Salinger',
                'description': 'Story about teenage rebellion and alienation',
                'publish_year': 1951,
                'cover_image': 'https://images.unsplash.com/photo-1553729459-efe14ef6055d'
            },
            {
                'title': 'The Lord of the Rings',
                'author': 'J.R.R. Tolkien',
                'description': 'Epic fantasy trilogy',
                'publish_year': 1954,
                'cover_image': 'https://images.unsplash.com/photo-1544716278-ca5e3f4abd8c'
            },
            {
                'title': 'The Alchemist',
                'author': 'Paulo Coelho',
                'description': 'Philosophical novel about following your dreams',
                'publish_year': 1988,
                'cover_image': 'https://images.unsplash.com/photo-1589829545856-d10d557cf95f'
            },
            {
                'title': 'The Da Vinci Code',
                'author': 'Dan Brown',
                'description': 'Mystery thriller novel',
                'publish_year': 2003,
                'cover_image': 'https://images.unsplash.com/photo-1544947950-fa07a98d237f'
            }
        ]

        # Create books
        books_created = 0
        for book_data in sample_books:
            book, created = Book.objects.get_or_create(
                title=book_data['title'],
                defaults=book_data
            )
            if created:
                books_created += 1

        self.stdout.write(
            self.style.SUCCESS(f'Successfully added {books_created} sample books!')
        )