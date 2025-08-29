import graphene
from graphene_django import DjangoObjectType
from .models import Book, Favorite
from django.db.models import Q
from django.core.paginator import Paginator

class BookType(DjangoObjectType):
    class Meta:
        model = Book
        fields = ("id", "title", "author", "description", "publish_year", "cover_image")

class BookPaginationType(graphene.ObjectType):
    books = graphene.List(BookType)
    total_count = graphene.Int()
    page = graphene.Int()
    page_size = graphene.Int()
    total_pages = graphene.Int()
    has_next = graphene.Boolean()
    has_previous = graphene.Boolean()

class Query(graphene.ObjectType):
    all_books = graphene.List(BookType, search=graphene.String())
    books_paginated = graphene.Field(
        BookPaginationType,
        search=graphene.String(),
        page=graphene.Int(default_value=1),
        page_size=graphene.Int(default_value=10)
    )
    book = graphene.Field(BookType, id=graphene.Int(required=True))

    def resolve_all_books(root, info, search=None):
        qs = Book.objects.all()
        if search:
            qs = qs.filter(Q(title__icontains=search) | Q(author__icontains=search))
        return qs

    def resolve_books_paginated(root, info, search=None, page=1, page_size=10):
        qs = Book.objects.all()
        if search:
            qs = qs.filter(Q(title__icontains=search) | Q(author__icontains=search))
        
        paginator = Paginator(qs, page_size)
        books_page = paginator.get_page(page)
        
        return BookPaginationType(
            books=books_page.object_list,
            total_count=paginator.count,
            page=page,
            page_size=page_size,
            total_pages=paginator.num_pages,
            has_next=books_page.has_next(),
            has_previous=books_page.has_previous()
        )

    def resolve_book(root, info, id):
        try:
            return Book.objects.get(pk=id)
        except Book.DoesNotExist:
            return None

class CreateBook(graphene.Mutation):
    class Arguments:
        title = graphene.String(required=True)
        author = graphene.String(required=True)
        description = graphene.String()
        publish_year = graphene.Int()
        cover_image = graphene.String()

    book = graphene.Field(BookType)

    @classmethod
    def mutate(cls, root, info, title, author, description=None, publish_year=None, cover_image=None):
        book = Book.objects.create(
            title=title,
            author=author,
            description=description,
            publish_year=publish_year,
            cover_image=cover_image
        )
        return CreateBook(book=book)

class UpdateBook(graphene.Mutation):
    class Arguments:
        id = graphene.Int(required=True)
        title = graphene.String()
        author = graphene.String()
        description = graphene.String()
        publish_year = graphene.Int()
        cover_image = graphene.String()

    book = graphene.Field(BookType)

    @classmethod
    def mutate(cls, root, info, id, **kwargs):
        try:
            book = Book.objects.get(pk=id)
        except Book.DoesNotExist:
            return None
        for key, value in kwargs.items():
            setattr(book, key, value)
        book.save()
        return UpdateBook(book=book)

class DeleteBook(graphene.Mutation):
    class Arguments:
        id = graphene.Int(required=True)

    ok = graphene.Boolean()

    @classmethod
    def mutate(cls, root, info, id):
        try:
            book = Book.objects.get(pk=id)
            book.delete()
            return DeleteBook(ok=True)
        except Book.DoesNotExist:
            return DeleteBook(ok=False)

class ToggleFavorite(graphene.Mutation):
    class Arguments:
        book_id = graphene.Int(required=True)
        add = graphene.Boolean(required=True)

    success = graphene.Boolean()
    book = graphene.Field(BookType)

    @classmethod
    def mutate(cls, root, info, book_id, add):  # ← FIXED parameter name to match
        user = info.context.user
        if user.is_anonymous:
            return ToggleFavorite(success=False, book=None)
        try:
            book = Book.objects.get(pk=book_id)  # ← Use book_id here
        except Book.DoesNotExist:
            return ToggleFavorite(success=False, book=None)

        if add:
            Favorite.objects.get_or_create(user=user, book=book)
        else:
            Favorite.objects.filter(user=user, book=book).delete()

        return ToggleFavorite(success=True, book=book)

class Mutation(graphene.ObjectType):
    create_book = CreateBook.Field()
    update_book = UpdateBook.Field()
    delete_book = DeleteBook.Field()
    toggle_favorite = ToggleFavorite.Field()

# ADD THESE LINES TO EXPORT THE CLASSES
__all__ = ['Query', 'Mutation']