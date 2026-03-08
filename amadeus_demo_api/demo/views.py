import json
import ast
from amadeus import Client, ResponseError, Location
from django.shortcuts import render
from django.contrib import messages
from .flight import Flight
from .booking import Booking
from django.http import HttpResponse
from datetime import datetime
from random import choice, randint
import ast

# from .models import Booking as BookingModel
# from datetime import datetime

# def save_booking(request):
#     if request.method == "POST":
#         data = request.POST

#         customer_name = data.get('name')
#         email = data.get('email')
#         phone = data.get('phone')
#         passport_number = data.get('passport')
#         seat_number = data.get('seat')
#         class_name = data.get('class')
#         arrival_city = data.get('arrival_city')
#         destination_city = data.get('destination_city')
#         booking_date = data.get('booking_date')
#         arrival_time = data.get('arrival_time')
#         destination_time = data.get('destination_time')
#         ticket_price = data.get('price')
#         flight_number = data.get('flight_number')

#         BookingModel.objects.create(
#             customer_name=customer_name,
#             email=email,
#             phone=phone,
#             passport_number=passport_number,
#             seat_number=seat_number,
#             class_name=class_name,
#             arrival_city=arrival_city,
#             destination_city=destination_city,
#             booking_date=datetime.strptime(booking_date, '%d %B %Y').date(),
#             arrival_time=arrival_time,
#             destination_time=destination_time,
#             ticket_price=ticket_price,
#             flight_number=flight_number
#         )

#         return JsonResponse({"status": "success"})



amadeus = Client(
    client_id=' rQH4HxxapDH2AXPAvc8T0prTAnDYpvBC',
    client_secret='BpP4GM0ioqy6l5TL'
)



def get_iata_code(city_or_code):
    # If it's already a 3-letter code, assume it's an IATA code and try returning it directly
    if len(city_or_code) == 3 and city_or_code.isalpha():
        return city_or_code.upper()

    # Try CITY first
    try:
        response = amadeus.reference_data.locations.get(
            keyword=city_or_code,
            subType='CITY'
        )
        if response.data:
            return response.data[0]['iataCode']
    except ResponseError:
        pass

    # Try AIRPORT fallback
    try:
        response = amadeus.reference_data.locations.get(
            keyword=city_or_code,
            subType='AIRPORT'
        )
        if response.data:
            return response.data[0]['iataCode']
    except ResponseError:
        pass

    return None


def demo(request):
    if request.method == "POST":
        origin_city = request.POST.get("Origin")
        destination_city = request.POST.get("Destination")
        departure_date = request.POST.get("Departuredate")
        return_date = request.POST.get("Returndate")

        origin = get_iata_code(origin_city)
        destination = get_iata_code(destination_city)

        if not origin or not destination:
            messages.error(request, "Invalid city name. Please enter valid city names.")
            return render(request, "demo/home.html")

        kwargs = {
    "originLocationCode": origin,
    "destinationLocationCode": destination,
    "departureDate": departure_date,
    "adults": 1,
    "currencyCode": "INR",  
}


        tripPurpose = ""
        if return_date:
            kwargs["returnDate"] = return_date
            try:
                trip_purpose_response = amadeus.travel.predictions.trip_purpose.get(
                    originLocationCode=origin,
                    destinationLocationCode=destination,
                    departureDate=departure_date,
                    returnDate=return_date
                ).data
                tripPurpose = trip_purpose_response["result"]
            except ResponseError as error:
                messages.error(request, error.response.result["errors"][0]["detail"])
                return render(request, "demo/home.html")

        try:
            search_flights = amadeus.shopping.flight_offers_search.get(**kwargs)
            search_flights_returned = []
            for flight in search_flights.data:
                offer = Flight(flight).construct_flights()
                search_flights_returned.append(offer)
            response = zip(search_flights_returned, search_flights.data)
            return render(request, "demo/results.html", {
                "response": response,
                "origin": origin_city,
                "destination": destination_city,
                "departureDate": departure_date,
                "returnDate": return_date,
                "tripPurpose": tripPurpose,
            })
        except ResponseError as error:
            messages.error(request, error.response.result["errors"][0]["detail"])
            return render(request, "demo/home.html")

    # GET request - just show empty form
    return render(request, "demo/home.html")


def book_flight(request):
    if request.method == "POST":
        flight = request.POST.get("flight")
        actual_price = float(request.POST.get("actual_price", 0))  # get actual price from form

        traveler = {
            "id": "1",
            "dateOfBirth": "1990-01-01",
            "name": {"firstName": "John", "lastName": "Doe"},
            "gender": "MALE",
            "contact": {
                "emailAddress": "john.doe@example.com",
                "phones": [{"deviceType": "MOBILE", "countryCallingCode": "91", "number": "9999999999"}],
            },
            "documents": [{"documentType": "PASSPORT", "number": "000000000", "expiryDate": "2030-01-01", "issuanceCountry": "IN", "nationality": "IN", "holder": True}],
        }

        try:
            flight_price_confirmed = amadeus.shopping.flight_offers.pricing.post(
                ast.literal_eval(flight)
            ).data["flightOffers"]
        except (ResponseError, KeyError, AttributeError) as error:
            messages.add_message(request, messages.ERROR, error.response.body)
            return render(request, "demo/book_flight.html", {})

        try:
            order = amadeus.booking.flight_orders.post(
                flight_price_confirmed, traveler
            ).data
        except (ResponseError, KeyError, AttributeError) as error:
            messages.add_message(
                request, messages.ERROR, error.response.result["errors"][0]["detail"]
            )
            return render(request, "demo/book_flight.html", {})

        booking = Booking(order).construct_booking()

        # calculate cabin class prices based on actual flight price
        context = {
            "flight": booking["flights"][0],  # sending only first segment for now
            "gate": choice(["A1", "B2", "C3", "D4"]),
            "boarding_time": f"{randint(5, 8):02d}:{choice(['00', '15', '30', '45'])}",
            "price": round(actual_price, 2),
            "premium_price": round(actual_price * 1.10, 2),
            "business_price": round(actual_price * 1.23, 2),
            "first_price": round(actual_price * 1.35, 2),
        }


        return render(request, "demo/book_flight.html", context)


def origin_airport_search(request):
    if request.is_ajax():
        try:
            data = amadeus.reference_data.locations.get(
                keyword=request.GET.get("term", None), subType=Location.ANY
            ).data
        except (ResponseError, KeyError, AttributeError) as error:
            messages.add_message(
                request, messages.ERROR, error.response.result["errors"][0]["detail"]
            )
    return HttpResponse(get_city_airport_list(data), "application/json")


def destination_airport_search(request):
    if request.is_ajax():
        try:
            data = amadeus.reference_data.locations.get(
                keyword=request.GET.get("term", None), subType=Location.ANY
            ).data
        except (ResponseError, KeyError, AttributeError) as error:
            messages.add_message(
                request, messages.ERROR, error.response.result["errors"][0]["detail"]
            )
    return HttpResponse(get_city_airport_list(data), "application/json")


def get_city_airport_list(data):
    result = []
    for i, val in enumerate(data):
        result.append(data[i]["iataCode"] + ", " + data[i]["name"])
    result = list(dict.fromkeys(result))
    return json.dumps(result)
