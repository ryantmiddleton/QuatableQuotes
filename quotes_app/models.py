from django.db import models
import re
from datetime import date, datetime

# Create your models here.
class UserManager(models.Manager):
    def validate_registration(self, postData):
        errors = {}
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        PASSWORD_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        # SpecialSym =['$', '@', '#', '%']
        if len(postData['first_name_txt']) < 2:
             errors["first_name"] = "First name should be at least 2 characters long."
        if len(postData['last_name_txt']) < 2:
             errors["last_name"] = "Last name should be at least 2 characters long."
        if not EMAIL_REGEX.match(postData['email_txt']):
            errors['email'] = ("Invalid email address!")
        elif User.objects.filter(email=postData['email_txt']):
            errors["email"] = "It looks like '" + postData['email_txt'] + "' has already registered. Try logging in."  
        if postData['password_txt'] != postData['conf_password_txt']:
            errors['conf_password'] = "Your password is different than your confirmed password. Please make sure they are the same."
        if len(postData['password_txt']) < 8:
                errors['password'] = "Your password should be at least 8 characters long."
        else:
            if not any(char.isdigit() for char in postData['password_txt']):
                errors['password'] = "Your password should contain at least one number."
            elif not any(char.islower() for char in postData['password_txt']):
                errors['password'] = "Your password should contain at least one lowercase letter."
            elif not any(char.isupper() for char in postData['password_txt']):
                errors['password'] = "Your password should contain at least one uppercase letter."
            # elif not any(char in SpecialSym for char in postData['password_txt']): 
            #     errors['password'] = "Your password should have at least one of the symbols $@#')."
        return errors

    def validate_update(self, request):
        errors = {}
        postData = request.POST
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if len(postData['first_name_txt']) < 2:
             errors["first_name"] = "First name should be at least 2 characters long."
        if len(postData['last_name_txt']) < 2:
             errors["last_name"] = "Last name should be at least 2 characters long."
        if len(postData['email_txt']) == 0:
            errors['email'] = "Email field must be filled in."
        elif not EMAIL_REGEX.match(postData['email_txt']):
            errors['email'] = "Invalid email address!"
        elif User.objects.filter(email=postData['email_txt']):
            updating_user = User.objects.filter(email=postData['email_txt'])[0]
            if updating_user.id != request.session['user_id']:
                errors["email"] = "It looks like '" + postData['email_txt'] + "' has already been registered."  
        return errors

class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    #quotes_posted - a list of all quotes that have been posted by the user
    #likes - a list of likes the user has created
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()
            

class QuoteManager(models.Manager):
    def validate_data(self, postData):
        errors={}
        if len(postData['author_txt']) < 3:
             errors["author_txt"] = "The author must have at least 3 characters."
        if len(postData['content_txt']) < 10:
             errors["content_txt"] = "The quote must have at least 10 characters."
        return errors

class Quote(models.Model):
    content = models.TextField()
    quoted_by = models.CharField(max_length=255)
    posted_by = models.ForeignKey(User, related_name="quotes_posted", on_delete = models.CASCADE)
    #likes - a list of likes for the quote
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = QuoteManager()

class LikeManager(models.Manager):
    def validate_like(self, request, quote_id):
        errors={}
        if Like.objects.filter(user__id=request.session['user_id'], quote__id=quote_id):
            errors['like']="User has already liked this quote"
        return errors

class Like(models.Model):
    user = models.ForeignKey(User, related_name="likes", on_delete = models.CASCADE)
    quote = models.ForeignKey(Quote, related_name="likes", on_delete = models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects=LikeManager()

