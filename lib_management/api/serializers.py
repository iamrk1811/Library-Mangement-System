from rest_framework import serializers
from .models import Book, Author


class BookSerializer(serializers.ModelSerializer):
    author = serializers.CharField(source='author.name', required=False)
    author_id = serializers.IntegerField(required=True)
    status = serializers.SerializerMethodField(required=False)

    def get_status(self, book):
        try:
            return book.get_issue_status_display()
        except Exception:
            return ""

    def create(self, validated_data):
        author_id = validated_data.pop('author_id', None)
        if not author_id:
            raise Exception("Author ID required")
        author = Author.objects.filter(id=author_id).first()
        if not author:
            raise Exception("Invalid author")
        book = self.Meta.model(**validated_data)
        book.author = author
        book.save()
        return book

    class Meta:
        model = Book
        fields = ['id', 'title', 'author', 'author_id', 'publisher', 'isbn', 'status']
