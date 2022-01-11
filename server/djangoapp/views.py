from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render, redirect

from .models import CarModel
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from datetime import datetime

from . import restapis
import logging


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
    context = {}
    context["dealerships"] = restapis.get_dealers_from_cf()
    return render(request, "djangoapp/index.html", context)


def get_dealer_details(request, dealer_id):
    context = {}
    context["reviews"] = restapis.get_dealer_reviews_cf(dealer_id)
    context["dealer"] = restapis.get_dealer_details(dealer_id)
    return render(request, "djangoapp/dealer_details.html", context)


def add_review(request, dealer_id):
    if request.method == "GET":
        context = {}
        car_models = CarModel.objects.filter(dealerid=dealer_id)
        context["dealer"] = restapis.get_dealer_details(dealer_id)
        context["car_models"] = car_models
        return render(request, "djangoapp/add_review.html", context)

    if request.method == "POST":
        review_data = {
            k: v
            for k, v in request.POST.dict().items()
            if k in restapis.DearlerReview.__dataclass_fields__
        }

        if request.POST.get("purchase"):
            car_model = CarModel.objects.get(pk=request.POST["car"])
            review_data["purchase"] = True
            review_data["car_make"] = car_model.car_make.name
            review_data["car_model"] = car_model.name
            review_data["car_year"] = car_model.year

        review = restapis.DearlerReview(**review_data)
        review.dealership = dealer_id
        full_name = request.user.first_name + request.user.last_name
        review.name = full_name if full_name else request.user.username
        restapis.add_review(restapis.to_dict(review))
        return redirect("djangoapp:dealer_details", dealer_id=dealer_id)
