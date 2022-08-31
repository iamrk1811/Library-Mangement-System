from django.db import models
from .constants import BookIssuedStatus
from django.conf import settings


class Author(models.Model):
    name = models.CharField(max_length=100, blank=True, null=True)
    email = models.CharField(max_length=100, blank=True, null=True)


class Book(models.Model):
    BOOK_ISSUED_STATUS_CHOICES = (
        (BookIssuedStatus.BORROWED, 'Borrowed'),
        (BookIssuedStatus.AVAILABLE, 'Available'),
    )
    title = models.CharField(max_length=100, blank=True, null=True)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    year = models.DateField(blank=True, null=True)
    publisher = models.CharField(max_length=100, blank=True, null=True)
    isbn = models.CharField(max_length=100, blank=True, null=True)
    issue_status = models.IntegerField(choices=BOOK_ISSUED_STATUS_CHOICES, blank=True, null=True, default=BookIssuedStatus.AVAILABLE)
    borrowed_by = models.ForeignKey(settings.AUTH_USER_MODEL, default=None, on_delete=models.PROTECT, null=True, blank=True)


class AvailableBookInSystem(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
