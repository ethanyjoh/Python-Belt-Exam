# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
import bcrypt


class UserManager(models.Manager):
    def register(self, datafromhtml):
        errors = []

        if(len(datafromhtml['name']) < 2):
            errors.append("Your name should be at least 2 characters")
        if(len(datafromhtml['alias']) < 2):
            errors.append("Your alias should be at least 2 characters")
        if(len(datafromhtml['password']) < 8):
            errors.append("Your password should be at least 8 characters")
        if(datafromhtml['password'] != datafromhtml['password_confirm']):
            errors.append("Your password and you password confirmation must match")
        if(len(datafromhtml['bday']) < 8):
            errors.append("Please check your date of birth")

        try:
            validate_email(datafromhtml['email'])
        except ValidationError as e:
            errors.append("your email must be in a valid format")

        if errors:
            return {'err_messages': errors}
        else:
            hash_password = bcrypt.hashpw(datafromhtml['password'].encode(), bcrypt.gensalt())
            user = User.objects.create(name=datafromhtml['name'], alias=datafromhtml['alias'], email=datafromhtml['email'], password=hash_password, dob=datafromhtml['bday'])
            return {'new_user': user}

    def login(self, datafromhtml):
        try:
            user = User.objects.get(email=datafromhtml['email'])
            if bcrypt.checkpw(datafromhtml['password'].encode(), user.password.encode()):
                return {'logged_user': user}
            else:
                return {'err_messages': ['Email/Password invalid. Please try again']}
        except:
            return {'err_messages': ['Email you have entered does not exists. Please register your email']}


class QuoteManager(models.Manager):
    def add_quote(self, datafromhtml, user_id):
        errors = []

        if(len(datafromhtml['quote']) < 10):
            errors.append("Quote should be at least 10 characters")

        if errors:
            return {'err_messages': errors}
        else:
            user = User.objects.get(id=user_id)
            new_quote = Quote.objects.create(quote=datafromhtml['quote'], user=user)
            return {'new_quote': new_quote}


class User(models.Model):
    name = models.CharField(max_length=255)
    alias = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    dob = models.DateField(max_length=8)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = UserManager()


class Quote(models.Model):
    quote = models.TextField()
    user = models.ForeignKey(User, related_name='quotes')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = QuoteManager()


class Favorite(models.Model):
    user = models.ForeignKey(User, related_name='favorites_by')
    qoute = models.ForeignKey(Quote, related_name='favorites_to')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
