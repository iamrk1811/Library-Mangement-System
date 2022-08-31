from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import get_user_model
from .schemas import BookSchema, MemberSchema
from .serializers import BookSerializer
from .models import Book
from accounts.decorators import librarian_access, login_required, member_access, super_user_access
from api.models import Author
from api.constants import BookIssuedStatus
from accounts.serializers import UserSerializer
from accounts.constants import UserType
import copy
from rest_framework.decorators import action
from lib_management.utils import get_user_from_cookies
from rest_framework.schemas import ManualSchema
import coreapi
import coreschema

User = get_user_model()


class BookViewSet(viewsets.ViewSet):
    schema = BookSchema()

    @librarian_access
    def list(self, request):
        books = Book.objects.all()
        serializer = BookSerializer(books, many=True)
        return Response(status=status.HTTP_200_OK, data=serializer.data)

    @librarian_access
    def create(self, request):
        serializer = BookSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=status.HTTP_201_CREATED, data=serializer.data)

    @librarian_access
    def update(self, request, pk=None):
        book = Book.objects.filter(id=pk).first()
        if not book:
            return Response(status-status.HTTP_404_NOT_FOUND, data="Book not found")
        author_id = request.data.get('author_id', None)
        if author_id is not None:
            author = Author.objects.filter(id=author_id).first()
            if not author:
                return Response(status =status.HTTP_404_NOT_FOUND, data="Author not found")

        if author_id and author:
            book.author = author
        book.title = request.data.get('title', book.title)
        book.publisher = request.data.get('publisher', book.publisher)
        book.isbn = request.data.get('isbn', book.isbn)
        book.save()

        serializer = BookSerializer(book)
        return Response(status=status.HTTP_200_OK, data=serializer.data)

    @login_required
    def retrieve(self, request, pk=None):
        book = Book.objects.filter(id=pk).first()
        if not book:
            return Response(status =status.HTTP_404_NOT_FOUND, data="Book not found")
        serializer = BookSerializer(book)
        return Response(status=status.HTTP_200_OK, data=serializer.data)

    @librarian_access
    def destroy(self, request, pk=None):
        book = Book.objects.filter(id=pk).first()
        if not book:
            return Response(status =status.HTTP_404_NOT_FOUND, data="Book not found")
        deleted_book = copy.deepcopy(book)
        serializer = BookSerializer(deleted_book)
        book.delete()
        return Response(status=status.HTTP_200_OK, data=serializer.data)

    @member_access
    @action(detail=False, methods=['POST'], name='Borrow Book')
    def borrow(self, request):
        user = get_user_from_cookies(request.COOKIES)
        if not user:
            return Response(status =status.HTTP_404_NOT_FOUND, data="Invalid Member")
        book_id = request.data.get('id', None)
        if not book_id:
            return Response(status =status.HTTP_404_NOT_FOUND, data="Book ID not found")
        book = Book.objects.filter(id=book_id, issue_status=BookIssuedStatus.AVAILABLE).first()
        if not book:
            return Response(status =status.HTTP_404_NOT_FOUND, data="No available book found with this given ID")
        book.issue_status = BookIssuedStatus.BORROWED
        book.borrowed_by = user
        book.save()
        serializer = BookSerializer(book)
        return Response(status=status.HTTP_200_OK, data=serializer.data)

    @member_access
    @action(detail=False, methods=['POST'], name='Return Book')
    def return_book(self, request):
        user = get_user_from_cookies(request.COOKIES)
        if not user:
            return Response(status =status.HTTP_404_NOT_FOUND, data="Invalid Member")
        book_id = request.data.get('id', None)
        if not book_id:
            return Response(status =status.HTTP_404_NOT_FOUND, data="Book ID not found")
        book = Book.objects.filter(id=book_id, borrowed_by=user, issue_status=BookIssuedStatus.BORROWED).first()
        if not book:
            return Response(status =status.HTTP_404_NOT_FOUND, data="No borrowed book found")

        book.issue_status = BookIssuedStatus.AVAILABLE
        book.borrowed_by = None
        book.save()
        serializer = BookSerializer(book)
        return Response(status=status.HTTP_200_OK, data=serializer.data)


class MemberViewSet(viewsets.ViewSet):
    schema = MemberSchema()

    @librarian_access
    def list(self, request):
        member_users = User.objects.filter(user_type=UserType.MEMBER)
        serializer = UserSerializer(member_users, many=True)
        return Response(status=status.HTTP_200_OK, data=serializer.data)

    @librarian_access
    def create(self, request):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        user.user_type = UserType.MEMBER
        user.save()

        serializer = UserSerializer(user)
        return Response(status=status.HTTP_201_CREATED, data=serializer.data)

    @librarian_access
    def retrieve(self, request, pk=None):
        user = User.objects.filter(id=pk, user_type=UserType.MEMBER).first()
        if not user:
            return Response(status =status.HTTP_404_NOT_FOUND, data="Member not found")
        serializer = UserSerializer(user)
        return Response(status=status.HTTP_200_OK, data=serializer.data)

    @librarian_access
    def update(self, request, pk=None):
        user = User.objects.filter(id=pk, user_type=UserType.MEMBER).first()
        if not user:
            return Response(status =status.HTTP_404_NOT_FOUND, data="Member not found")

        user.email = request.data.get('email', user.email)
        user.first_name = request.data.get('first_name', user.first_name)
        user.last_name = request.data.get('last_name', user.last_name)

        password = request.data.get('password', None)
        if password is not None:
            user.set_password(password)
        user.user_type = request.data.get('user_type', user.user_type)
        user.save()

        serializer = UserSerializer(user)
        return Response(status=status.HTTP_200_OK, data=serializer.data)

    @librarian_access
    def destroy(self, request, pk=None):
        user = User.objects.filter(id=pk, user_type=UserType.MEMBER).first()
        if not user:
            return Response(status =status.HTTP_404_NOT_FOUND, data="Member not found")
        deleted_user = copy.deepcopy(user)
        serializer = UserSerializer(deleted_user)
        user.delete()
        return Response(status=status.HTTP_200_OK, data=serializer.data)


class SuperUserView(viewsets.ViewSet):
    schema = ManualSchema(fields=[],
        description="List down all users. Allowed access to only Super User."
    )
    @super_user_access
    @action(detail=False, methods=['GET'], name='Retrieve all users')
    def retrieve_all_users(self, request):
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(status=status.HTTP_200_OK, data=serializer.data)
