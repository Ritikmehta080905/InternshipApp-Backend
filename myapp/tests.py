import json
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Book

# ------------------------------
# Model Tests
# ------------------------------
class BookModelTests(TestCase):

    def setUp(self):
        self.book = Book.objects.create(
            title="Test Book",
            author="Test Author",
            description="Test Description",
            publish_year=2024,
            cover_image="https://example.com/cover.jpg"
        )

    def test_book_creation(self):
        self.assertEqual(self.book.title, "Test Book")
        self.assertEqual(self.book.author, "Test Author")
        self.assertEqual(self.book.publish_year, 2024)

    def test_book_str_representation(self):
        self.assertEqual(str(self.book), "Test Book by Test Author")

    def test_book_fields_optional(self):
        book = Book.objects.create(
            title="Minimal Book",
            author="Minimal Author"
        )
        self.assertIsNone(book.description)
        self.assertIsNone(book.publish_year)
        self.assertIsNone(book.cover_image)

# ------------------------------
# GraphQL Tests
# ------------------------------
class GraphQLTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass123')
        self.book = Book.objects.create(
            title="GraphQL Test Book",
            author="GraphQL Author",
            publish_year=2024
        )

    def post_query(self, query):
        self.client.force_login(self.user)
        return self.client.post(
            reverse('graphql'),
            data=json.dumps({'query': query}),
            content_type='application/json'
        )

    def test_all_books_query(self):
        query = '''
        {
            allBooks {
                id
                title
                author
            }
        }
        '''
        response = self.post_query(query)
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEqual(len(data['data']['allBooks']), 1)
        self.assertEqual(data['data']['allBooks'][0]['title'], "GraphQL Test Book")

    def test_single_book_query(self):
        query = f'''
        {{
            book(id: {self.book.id}) {{
                title
                author
                publishYear
            }}
        }}
        '''
        response = self.post_query(query)
        data = json.loads(response.content)
        self.assertEqual(data['data']['book']['title'], "GraphQL Test Book")

    def test_create_book_mutation(self):
        mutation = '''
        mutation {
            createBook(
                title: "New Book",
                author: "New Author",
                publishYear: 2025
            ) {
                book {
                    id
                    title
                    author
                }
            }
        }
        '''
        response = self.post_query(mutation)
        data = json.loads(response.content)
        self.assertEqual(data['data']['createBook']['book']['title'], "New Book")
        self.assertEqual(Book.objects.count(), 2)

# ------------------------------
# Authentication Tests
# ------------------------------
class AuthenticationTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='authuser', password='testpass123')
        self.book = Book.objects.create(title="Auth Book", author="Auth Author")

    def post_query(self, query, login=False):
        if login:
            self.client.force_login(self.user)
        return self.client.post(
            reverse('graphql'),
            data=json.dumps({'query': query}),
            content_type='application/json'
        )

    def test_graphql_requires_login(self):
        query = '''
        {
            allBooks {
                title
            }
        }
        '''
        # Without login
        response = self.post_query(query, login=False)
        self.assertIn(response.status_code, [302, 403])

        # With login
        response = self.post_query(query, login=True)
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEqual(len(data['data']['allBooks']), 1)
