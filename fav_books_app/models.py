from django.db import models
from django.db.models.deletion import CASCADE
import re
import bcrypt
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

# Create your models here.
class UserManager(models.Manager):
    def validate(self, postData):
        #first_name/last_name validation
        errors = {}
        if len(postData['first_name']) < 2:
            errors['first_name'] = 'First name must be atleast 2 characters long'
        
        if len(postData['last_name']) < 2:
            errors['last_name'] = 'last name must be atleast 2 characters long'

        #check for password
        if len(postData['password']) < 8:
            errors['password'] = 'password must be at least 8 characters'
        
        if postData['password'] != postData['pw_confirm']:
            errors['password'] = 'passwords do not match'

        #duplicate email
        email_check = User.objects.filter(email=postData['email'])
        if email_check:
            errors['duplicate']='Email address already taken'

        #pattern validation
        if not EMAIL_REGEX.match(postData['email']):
            errors['email']='Invalid email address'
        return errors

    def register(self, postData):
        pw = bcrypt.hashpw(postData['password'].encode(), bcrypt.gensalt()).decode()
        return User.objects.create(first_name = postData['first_name'], last_name = postData['last_name'], email = postData['email'], password = pw)

    def authenticate(self, email, password):
        #filter user based given on email
        users = User.objects.filter(email=email)
        if users:
            user=users[0]
        #decrypt password and match to given password
            if bcrypt.checkpw(password.encode(), user.password.encode()):
                return True
            else:
                return False
        return False
    


class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()

class BookManager(models.Manager):
    def bookValidate(self, postData):
        #first_name/last_name validation
        errors = {}
        if len(postData['title']) < 2:
            errors['title'] = 'title must be atleast 2 characters long'
        
        if len(postData['description']) < 4:
            errors['description'] = 'description must be atleast 2 characters long'
        return errors


class Book(models.Model):
    title = models.CharField(max_length=45)
    description = models.CharField(max_length=255)
    uploaded_by = models.ForeignKey(User, related_name = 'books_uploaded', on_delete=models.CASCADE)
    users_who_like = models.ManyToManyField(User, related_name = 'liked_books')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = BookManager()

