from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render,redirect
from django.urls import reverse
from django import forms

from .models import *

class Post(forms.Form):
    title = forms.CharField(label = 'Title')
    description = forms.CharField(label = 'Description')
    price = forms.FloatField()
    image = forms.ImageField(required=True)
    category = forms.ModelChoiceField(queryset = Category.objects.all())
    

def index(request):
    listings = Listing.objects.all()

    context = {'listings': listings}
    return render(request, "auctions/index.html", context)

def add_bid(request, id):
    if request.method == "POST":
        ''' Try and except great option for this'''
        try:
            if  Bid.objects.get(listing=id):
                old_bid = Bid.objects.get(listing= id)
                addbid = int(request.POST.get('bid'))
                if addbid > old_bid.bid:
                    old_bid.bid = addbid
                    old_bid.user = request.user
                    old_bid.save()
                    response = redirect('products', id=id)
                    response.set_cookie('errorgreen', 'bid successfully000!!!', max_age=3)
                    return response
                else:
                    response = redirect('products',id=id)
                    response.set_cookie('error','Bid should be greater than current price',max_age=3)
                    return response

        except:
            listing = Listing.objects.get(id=id)
            addbid = int(request.POST.get('bid'))
            if addbid > listing.starting_bid:
                update_bid = Bid(listing = listing,
                                bid = addbid,
                                user = request.user)
                update_bid.save()
                response = redirect('products', id=id)
                response.set_cookie('errorgreen', 'bid successfully!!!', max_age=3)
                return response
            else:
                response = redirect('products',id=id)
                response.set_cookie('error','Bid should be greater than current price',max_age=3)
                return response
                
    else:
        context = {}
        return redirect('index')

def add_comment(request, id):
    if request.method == "POST":
        listing = Listing.objects.get(id=id)
        addcomment = request.POST.get('comment')
        update_comment = Comment(listing = listing,
                        comment = addcomment,
                        user = request.user)
        update_comment.save()
        response = redirect('products', id=id)
        response.set_cookie('errorgreen', 'comment successfully!!!', max_age=3)
        return response
    else:
        context = {}
        return redirect('index')
    
def close_bid(request, id):
    if request.user.username:
        listing = Listing.objects.get(id=id)
        listing.is_active = False
        listing.save()
        response = redirect('products', id=id)
        response.set_cookie('errorgreen', 'Bid closed!!!', max_age=3)
        return response
    else:
        return redirect('index')

def watchlist(request):
    if request.user.is_authenticated:
        items = Watchlist.objects.filter(watcher = request.user)
    else:
        items = []
    context = {'items': items}
    return render(request, "auctions/watchlist.html", context)

def categories(request):
    items = Category.objects.all()
    context = {'items':items}
    return render(request, "auctions/categories.html", context)

def category_page(request, category):
    items = Listing.objects.filter(category=category)
    context = {'items': items}
    return render(request, "auctions/category_page.html", context)

def product(request, id):
    item = Listing.objects.get(id=id)
    comments = Comment.objects.filter(listing= item)
    
    try:
        if Bid.objects.get(listing = item):
            current_bid = Bid.objects.get(listing = item)
    except:
            current_bid = 0
    if request.user.is_authenticated:
        try:
            item = Listing.objects.get(id=id)
            if item.creator == request.user:
                owner = True
            else:
                owner = False
        except:
            owner = False
        try:
            if Watchlist.objects.get(watcher = request.user, item = id):
                added = True
        except:
            added = False
        try:
            if current_bid.user == request.user:
                winner = True
            else:
                winner = False
        except:
            winner = False
    else:
        owner= False
        winner = False
        added = False

    context = {'item': item,
                'owner': owner,
                'winner': winner,
                'current_bid': current_bid,
                'comments': comments,
                'added': added,
                "error":request.COOKIES.get('error'),
                "errorgreen":request.COOKIES.get('errorgreen')}
    return render(request, "auctions/product.html", context)

def create(request):
    if request.method == "POST":
        form = Post(request.POST, request.FILES)

        if form.is_valid():
            title = form.cleaned_data["title"]
            description = form.cleaned_data["description"]
            price = form.cleaned_data["price"]
            image1 = request.FILES["image"]
            category = form.cleaned_data['category']
            heh = Listing(
                title = title,
                description = description,
                starting_bid = price, 
                image = image1,
                creator = request.user,
                category = category)
            heh.save()
            return HttpResponseRedirect(reverse('index'))
        else:
            context = {"message": "You forget something dude!"}
            return render(request, "auctions/error.html", context)
        
    else:
        context = {"pos": Post(),}
        return render(request, "auctions/create.html", context)

def add_watchlist(request, id):
    if request.user.username:

        listing = Listing.objects.get(id=id)
        watches = Watchlist(
            watcher = request.user,
            item = listing)
        watches.save()
        return redirect('products', id=id)
    else:
        return redirect('index')

def remove_watchlist(request, id):
    if request.user.username:
        watches = Watchlist.objects.get(watcher = request.user, item = id)
        watches.delete()
        return redirect('products', id=id)
    else:
        return redirect('index')

def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")
