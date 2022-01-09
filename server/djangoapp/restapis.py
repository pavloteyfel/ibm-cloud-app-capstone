import requests

from requests import RequestException
from dataclasses import asdict, dataclass
from urllib.parse import urljoin
from ibm_watson import NaturalLanguageUnderstandingV1
from ibm_watson import ApiException
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibm_watson.natural_language_understanding_v1 import (
    Features,
    EntitiesOptions,
    KeywordsOptions,
    SentimentOptions,
)


URL = "https://673eb614.eu-gb.apigw.appdomain.cloud/api/"
HEADERS = {"Content-Type": "application/json"}
DEALERSHIPS_ENDPOINT = "dealership"
REVIEWS_ENDPOINT = "review"
NLU_API_KEY = ""
NLU_URL = "https://api.eu-gb.natural-language-understanding.watson.cloud.ibm.com/instances/0c163ee7-47ac-4c82-8c2d-a32c137bebd1"


@dataclass
class CarDealer:
    address: str = None
    city: str = None
    full_name: str = None
    id: int = None
    lat: float = None
    long: float = None
    short_name: str = None
    st: str = None
    state: str = None
    zip: str = None


@dataclass
class DearlerReview:
    id: int = None
    car_make: str = None
    car_model: str = None
    car_year: int = None
    dealership: int = None
    name: str = None
    purchase: bool = None
    purchase_date: str = None
    review: str = None
    sentiment: str = None


def get_request(url, params=None):
    try:
        response = requests.get(url, headers=HEADERS, params=params)
    except RequestException as error:
        print(error)
    return response.json()


def post_request(url, json):
    try:
        requests.post(url, json=json)
    except RequestException as error:
        print(error)


def get_dealers_from_cf():
    results = []
    dealerships_url = urljoin(URL, DEALERSHIPS_ENDPOINT)
    dealers_json_data = get_request(dealerships_url)
    if dealers_json_data.get("total") > 0:
        for dealer_data in dealers_json_data.get("dealerships"):
            results.append(CarDealer(**dealer_data))
    return results


def get_dealer_reviews_cf(dealer_id):
    results = []
    reviews_url = urljoin(URL, REVIEWS_ENDPOINT)
    dealers_review_json_data = get_request(reviews_url, params={"dealerId": dealer_id})
    if dealers_review_json_data.get("total") > 0:
        for dealer_review_data in dealers_review_json_data.get("reviews"):
            review = DearlerReview(**dealer_review_data)
            review.sentiment = analyze_sentiments(review.review)
            results.append(review)
    return results


def get_dealer_details(dealer_id):
    dealer = None
    dealerships_url = urljoin(URL, DEALERSHIPS_ENDPOINT)
    dealership_data = get_request(dealerships_url, params={"id": dealer_id})
    if dealership_data:
        dealer = CarDealer(**dealership_data)
    return dealer


def add_review(review):
    reviews_url = urljoin(URL, REVIEWS_ENDPOINT)
    review_data = {"review": {**review}}
    post_request(reviews_url, json=review_data)


def analyze_sentiments(text):
    sentiment_label = ""
    authenticator = IAMAuthenticator(NLU_API_KEY)
    natural_language_understanding = NaturalLanguageUnderstandingV1(
        version="2021-08-01", authenticator=authenticator
    )
    natural_language_understanding.set_service_url(NLU_URL)
    try:
        response = natural_language_understanding.analyze(
            text=text, features=Features(sentiment=SentimentOptions())
        )
        sentiment_label = response.result.get("sentiment").get("document").get("label")
    except ApiException as error:
        print(error)

    return sentiment_label


def to_dict(obj):
    return asdict(obj, dict_factory=lambda x: {k: v for (k, v) in x if v is not None})
