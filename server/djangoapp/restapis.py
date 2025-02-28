import requests
import json
# import related models here
from requests.auth import HTTPBasicAuth


# Create a `get_request` to make HTTP GET requests
# e.g., response = requests.get(url, params=params, headers={'Content-Type': 'application/json'},
#                                     auth=HTTPBasicAuth('apikey', api_key))
import requests
import json
from .models import CarDealer, DealerReview
from requests.auth import HTTPBasicAuth

def get_request(url, **kwargs):
    print(kwargs)
    print("GET from {} ".format(url))
    api_key = kwargs.get('api_key')

    try:
        # Call get method of requests library with URL and parameters
        if api_key:
            params = dict()
            params["text"] = kwargs["text"]
            params["version"] = kwargs["version"]
            params["features"] = kwargs["features"]
            params["return_analyzed_text"] = kwargs["return_analyzed_text"]
            response = requests.get(url, params=params, headers={'Content-Type': 'application/json'},
                                                auth=HTTPBasicAuth('apikey', api_key))
        else:
            response = requests.get(url, headers={'Content-Type': 'application/json'},
                                    params=kwargs)
    except:
        # If any error occurs
        print("Network exception occurred")
    
    status_code = response.status_code
    print("With status {} ".format(status_code))
    json_data = json.loads(response.text)
    return json_data

# Create a `post_request` to make HTTP POST requests
# e.g., response = requests.post(url, params=kwargs, json=payload)
def post_request(url, payload=None, **kwargs):
    try:
        response = requests.post(url, params=kwargs, json=payload)
        return response
    except requests.RequestException as e:
        print(f"An error occurred: {e}")
        return None


# Create a get_dealers_from_cf method to get dealers from a cloud function
# def get_dealers_from_cf(url, **kwargs):
# - Call get_request() with specified arguments
# - Parse JSON results into a CarDealer object list
def get_dealers_from_cf(url, **kwargs):
    results = []
    # Call get_request with a URL parameter
    json_result = get_request(url)
    if json_result:
        # Get the row list in JSON as dealers
        dealers = json_result
        # For each dealer object
        for dealer in dealers:
            # Get its content in `doc` object
            dealer_doc = dealer
            # Create a CarDealer object with values in `doc` object
            dealer_obj = CarDealer(address=dealer_doc["address"], city=dealer_doc["city"], full_name=dealer_doc["full_name"],
                                   id=dealer_doc["id"], lat=dealer_doc["lat"], long=dealer_doc["long"],
                                   short_name=dealer_doc["short_name"],
                                   st=dealer_doc["st"], zip=dealer_doc["zip"])
            results.append(dealer_obj)

    return results

# Create a get_dealer_reviews_from_cf method to get reviews by dealer id from a cloud function
def get_dealer_by_id_from_cf(url, dealerId):
    # - Call get_request() with specified arguments
    # - Parse JSON results into a DealerView object list
    results = []
    # Call get_request with a URL parameter
    json_result = get_request(f"{url}?id={dealerId}")
    print(f"{url}?id={dealerId}")

    if json_result:
        # Get the row list in JSON as dealers
        reviews = json_result
        # For each dealer object
        for review in reviews:
            # Get its content in `doc` object
            review_obj = DealerReview(
                dealership=review['dealership'],
                name=review['name'],
                purchase=review['purchase'],
                review=review['review'],
                purchase_date=review['purchase_date'],
                car_make=review['car_make'],
                car_model=review['car_model'],
                car_year=review['car_year'],
                sentiment=analyze_review_sentiments(review['review']),
                id=review['id']
            )
            results.append(review_obj)

    return results

# Create an `analyze_review_sentiments` method to call Watson NLU and analyze text
# def analyze_review_sentiments(text):
# - Call get_request() with specified arguments
# - Get the returned sentiment label such as Positive or Negative
def analyze_review_sentiments(dealerreview):
    api_key = "XsdNlbcNdqSFvKgvp791PYmXPkMpDadrUfyxzDaWTRpD"
    url = "https://api.au-syd.natural-language-understanding.watson.cloud.ibm.com/instances/0cb63745-2bda-4451-80d0-cf12e8946737"
    return get_request(url, api_key=api_key, text=dealerreview, version='2021-08-01', features={'entities': {}, 'keywords': {}}, return_analyzed_text=False)


