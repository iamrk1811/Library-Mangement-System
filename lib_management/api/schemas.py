from rest_framework.schemas import AutoSchema
import coreapi
import coreschema


class MemberSchema(AutoSchema):
    def get_manual_fields(self, path, method):
        extra_fields = []
        if method.lower() == 'get':
            extra_fields = []
        elif method.lower() == 'post':
            extra_fields = [
               coreapi.Field(
                   "email",
                   required=True,
                   schema=coreschema.String()
               ),
               coreapi.Field(
                   "password",
                   required=True,
                   schema=coreschema.String()
               ),
                coreapi.Field(
                   "first_name",
                   required=True,
                   schema=coreschema.String()
                ),
                coreapi.Field(
                    "last_name",
                    required=True,
                    schema=coreschema.String()
                ),
                coreapi.Field(
                    "user_type",
                    required=True,
                    schema=coreschema.Integer()
                ),

            ]
        elif method.lower() == 'put':
            extra_fields = [
                coreapi.Field(
                    "first_name",
                    required=True,
                    schema=coreschema.String()
                ),
                coreapi.Field(
                    "last_name",
                    required=True,
                    schema=coreschema.String()
                ),
                coreapi.Field(
                    "email",
                    required=True,
                    schema=coreschema.String()
                ),
                coreapi.Field(
                    "password",
                    required=True,
                    schema=coreschema.String()
                ),
                coreapi.Field(
                    "user_type",
                    required=True,
                    schema=coreschema.Integer()
                ),
            ]

        manual_fields = super().get_manual_fields(path, method)
        return manual_fields + extra_fields

    def get_description(self, path, method):
        if path == '/api/member/{id}/' and method.lower() == 'get':
            return "View a single Member, Allowed access Librarian"
        elif method.lower() == 'get':
            return "List down all the available Member, Allowed access Librarian"
        elif method.lower() == 'post':
            return "Takes users credentials and create a user.  Allowed access Librarian. \n User type: \n1 for - Librarian \n 2 for - Member, "
        elif method.lower() == 'put':
            return "Update s single Member, Allowed access Librarian"
        elif method.lower() == 'delete':
            return "Delete a Member with given ID, Allowed access Librarian"


class BookSchema(AutoSchema):
    def get_manual_fields(self, path, method):
        extra_fields = []
        if path == '/api/book/borrow/' and method.lower() == 'post':
            extra_fields = [
                coreapi.Field(
                    "id",
                    required=True,
                    schema=coreschema.Integer()
                ),
            ]
        elif path == '/api/book/return_book/' and method.lower() == 'post':
            extra_fields = [
                coreapi.Field(
                    "id",
                    required=True,
                    schema=coreschema.Integer()
                ),
            ]
        elif method.lower() == 'get':
            extra_fields = []
        elif method.lower() == 'post':
            extra_fields = [
                coreapi.Field(
                    "title",
                    required=True,
                    schema=coreschema.String()
                ),
                coreapi.Field(
                    "author_id",
                    required=True,
                    schema=coreschema.Integer()
                ),
                coreapi.Field(
                    "publisher",
                    required=True,
                    schema=coreschema.String()
                ),
                coreapi.Field(
                    "isbn",
                    required=True,
                    schema=coreschema.String()
                ),
            ]
        elif method.lower() == 'put':
            extra_fields = [
                coreapi.Field(
                    "title",
                    required=True,
                    schema=coreschema.String()
                ),
                coreapi.Field(
                    "author_id",
                    required=True,
                    schema=coreschema.Integer()
                ),
                coreapi.Field(
                    "publisher",
                    required=True,
                    schema=coreschema.String()
                ),
                coreapi.Field(
                    "isbn",
                    required=True,
                    schema=coreschema.String()
                ),
            ]

        manual_fields = super().get_manual_fields(path, method)
        return manual_fields + extra_fields

    def get_description(self, path, method):
        if path == '/api/book/{id}/' and method.lower() == 'get':
            return "View a single book, Allowed all logged in users"
        elif path == '/api/book/return_book/' and method.lower() == 'post':
            return "Return borrowed book"
        elif path == '/api/book/borrow/' and method.lower() == 'post':
            return "Borrow a book, Allowed Member access."
        elif method.lower() == 'get':
            return "List down all the available books, Allowed access Librarian"
        elif method.lower() == 'post':
            return "Takes book information and create a book, Allowed access Librarian"
        elif method.lower() == 'put':
            return "Update s single Book, Allowed access Librarian"
        elif method.lower() == 'delete':
            return "Delete a book with given ID, Allowed access Librarian"
