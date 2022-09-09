# Hosted URL and Swagger
## https://infinite-castle-77770.herokuapp.com/

## Dependencies

This project relies mainly on Django. Mainly:

- Python 3.8+

- Django 3+ 

- Django Rest Framework 
  

### Scenario

The are two roles in the system; `LIBRARIAN` and `MEMBER`

  

### As a User

- I can signup either as `LIBRARIAN` and `MEMBER` using username and password

- I can login using username/password and get JWT access token

  

#### As a Librarian

- I can add, update, and remove Books from the system

- I can add, update, view, and remove Member from the system

#### As a Member

- I can view, borrow, and return available Books

- Once a book is borrowed, its status will change to `BORROWED`

- Once a book is returned, its status will change to `AVAILABLE`

- I can delete my own account