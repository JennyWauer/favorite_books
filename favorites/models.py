from django.db import models

from django.db import models

import re

# Create your models here.
class UserManager(models.Manager):
    def basic_validator(self, postData):
        errors = {}
        email_check = re.compile(
            r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        password = postData['password']
        conf_password = postData['conf_password']
        if len(postData['first_name']) < 2:
            errors["first_name"] = "Your first name should be at least 2 characters"
        if len(postData['last_name']) < 2:
            errors["last_name"] = "You last name should be at least 3 characters"
        if not email_check.match(postData['email']):
            errors["email"] = "Your email should be a valid email"
        email_exist = self.filter(email=postData['email'])
        if email_exist:
            errors['email'] = "Email already in use"
        if len(postData['password']) < 8:
            errors["password_len"] = "Your password should be at least 8 characters"
        if not password == conf_password:
            errors["password"] = "Your passwords do not match"
        return errors

    def login_validator(self, postData):
        login_errors = {}
        login_pass = postData['login_pass']
        login_email = postData['login_email']
        if len(User.objects.filter(email=login_email)) < 0:
            errors["login_email"] = "User email not found"
        if len(User.objects.filter(email=login_email)) > 0:
            user = User.objects.get(email=login_email)
            if not user.password == login_pass:
                errors["login_password"] = "Password does not match user email"
        return login_errors


class BookManager(models.Manager):
    def book_validator(self, postData):
        book_errors = {}
        if len(postData['title']) < 1:
            book_errors["title"] = "Book title is required"
        if len(postData['desc']) < 5:
            book_errors["desc"] = "Book description must be at least 5 characters"

class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField()
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()

class Book(models.Model):
    title = models.CharField(max_length=255)
    desc = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    uploaded_by = models.ForeignKey(User, related_name="books", on_delete=models.CASCADE)
    users_who_like = models.ManyToManyField(User, related_name="liked_books")
    objects = BookManager()