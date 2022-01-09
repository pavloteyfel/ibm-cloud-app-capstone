from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render, redirect

# from .models import related models
# from .restapis import related methods
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from datetime import datetime
import restapis
import logging
import json

# Get an instance of a logger
logger = logging.getLogger(__name__)


def about(request):
    return render(request, "djangoapp/about.html")


def contact(request):
    return render(request, "djangoapp/contact.html")


def login_request(request):
    context = {}

    if request.method != "POST":
        return render(request, "djangoapp/login.html", context)

    user = authenticate(
        username=request.POST["username"], password=request.POST["password"]
    )

    if not user:
        context["message"] = "Invalid username or password."
        return render(request, "djangoapp/login.html", context)

    login(request, user)
    return redirect("djangoapp:index")


def logout_request(request):
    logout(request)
    return redirect("djangoapp:index")


def user_exists(username):
    exists = True
    try:
        User.objects.get(username=username)
    except User.DoesNotExist:
        exists = False
    return exists


def registration_request(request):
    context = {}

    if request.method == "GET":
        return render(request, "djangoapp/registration.html", context)

    if request.method == "POST":

        if user_exists(request.POST["username"]):
            context["message"] = "User already exists."
            logger.error("User already exists")
            return render(request, "djangoapp/registration.html", context)

        user = User.objects.create_user(
            username=request.POST["username"],
            first_name=request.POST["firstname"],
            last_name=request.POST["lastname"],
            password=request.POST["password"],
        )

        login(request, user)
        return redirect("djangoapp:index")


def get_dealerships(request):
    return HttpResponse()


def get_dealer_details(request, dealer_id):
    return HttpResponse()


def add_review(request, dealer_id):
    return HttpResponse()
