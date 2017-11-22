# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect
from .models import *
from django.contrib import messages


def index(request):
    return render(request, 'users/index.html')


def register(request):
    result = User.objects.register(request.POST)
    if 'err_messages' in result:
        for error in result['err_messages']:
            messages.error(request, error)
        return redirect('/main')
    else:
        request.session['user_id'] = result['new_user'].id
        print(request.session['user_id'])
        messages.success(request, "You have successfully registered. Please login now")
        return redirect('/main')


def login(request):
    result = User.objects.login(request.POST)
    if 'err_messages' in result:
        for error in result['err_messages']:
            messages.error(request, error)
        return redirect('/main')
    else:
        request.session['user_id'] = result['logged_user'].id
        print(request.session['user_id'])
        return redirect('/quotes')


def logout(request):
    request.session.clear()
    return redirect('/main')


def quotes(request):
    logged_user = User.objects.get(id=request.session['user_id'])
    list_quote = Quote.objects.exclude(favorites_to__user=request.session['user_id']).order_by('-created_at')
    favorite_quotes = Favorite.objects.filter(user=request.session['user_id'])
    context = {
        'user': logged_user,
        'quotes': list_quote,
        "favorites_qs": favorite_quotes
    }
    return render(request, 'users/quotes.html', context)


def new(request):
    Quote.objects.add_quote(request.POST, request.session['user_id'])
    return redirect('/quotes')


def show_user(request, user_id):
    user = User.objects.get(id=user_id)
    context = {
        'user': user
    }
    return render(request, 'users/user.html', context)


def favorite(request, quote_id):
    user = User.objects.get(id=request.session['user_id'])
    qoute = Quote.objects.get(id=quote_id)
    Favorite.objects.create(user=user, qoute=qoute)
    return redirect('/quotes')


def remove(request, quote_id):
    user = User.objects.get(id=request.session['user_id'])
    quote = Quote.objects.get(id=quote_id)
    Favorite.objects.filter(user=user, qoute=quote).delete()
    return redirect('/quotes')
