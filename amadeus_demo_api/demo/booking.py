import re
from datetime import datetime

class Booking:
    def __init__(self, booking_data):
        self.booking_data = booking_data

    def construct_booking(self):
        booking = {}
        
        # Extract flight details for booked flight
        try:
            flight_offer = self.booking_data["flightOffers"][0]
            segment = flight_offer["itineraries"][0]["segments"][0]
            
            # Extract all necessary details for the boarding pass
            booking["flights"] = [{
                "carrier_code": segment["carrierCode"],
                "number": segment["number"],
                "departure_date": self.format_date(segment["departure"]["at"]),
                "departure_time": self.format_time(segment["departure"]["at"]),
                "departure_code": segment["departure"]["iataCode"],
                "departure_city": self.get_city_name(segment["departure"]["iataCode"]),
                "arrival_time": self.format_time(segment["arrival"]["at"]),
                "arrival_code": segment["arrival"]["iataCode"],
                "arrival_city": self.get_city_name(segment["arrival"]["iataCode"]),
            }]
            
            # Add price info
            booking["total_price"] = float(flight_offer["price"]["total"])
            booking["currency"] = flight_offer["price"]["currency"]
            
        except (KeyError, IndexError):
            # Handle missing data
            booking["flights"] = []
            
        return booking
        
    def format_date(self, date_string):
        # Convert "2025-04-25T08:30:00" to "25 April 2025"
        try:
            from datetime import datetime
            dt = datetime.fromisoformat(date_string.replace('Z', '+00:00'))
            return dt.strftime('%d %B %Y')
        except:
            return date_string
            
    def format_time(self, date_string):
        # Convert "2025-04-25T08:30:00" to "08:30"
        try:
            from datetime import datetime
            dt = datetime.fromisoformat(date_string.replace('Z', '+00:00'))
            return dt.strftime('%H:%M')
        except:
            return date_string
            
    def get_city_name(self, iata_code):
        # Same implementation as in Flight class
        if iata_code == "DEL":
            return "New Delhi"
        elif iata_code == "BOM":
            return "Mumbai"
        return iata_code


def get_airline_logo(carrier_code):
    return "https://s1.apideeplink.com/images/airlines/" + carrier_code + ".png"


def get_hour(date_time):
    return datetime.strptime(date_time[0:19], "%Y-%m-%dT%H:%M:%S").strftime("%H:%M")


def get_stoptime(total_duration, first_flight_duration, second_flight_duration):
    if re.search('PT(.*)H', total_duration) is None:
        total_duration_hours = 0
    else:
        total_duration_hours = int(re.search('PT(.*)H', total_duration).group(1))
    if re.search('H(.*)M', total_duration) is None:
        total_duration_minutes = 0
    else:
        total_duration_minutes = int(re.search('H(.*)M', total_duration).group(1))

    if re.search('PT(.*)H', first_flight_duration) is None:
        first_flight_hours = 0
    else:
        first_flight_hours = int(re.search('PT(.*)H', first_flight_duration).group(1))
    if re.search('H(.*)M', first_flight_duration) is None:
        first_flight_minutes = 0
    else:
        first_flight_minutes = int(re.search('H(.*)M', first_flight_duration).group(1))

    if re.search('PT(.*)H', second_flight_duration) is None:
        second_flight_hours = 0
    else:
        second_flight_hours = int(re.search('PT(.*)H', second_flight_duration).group(1))
    if re.search('H(.*)M', second_flight_duration) is None:
        second_flight_minutes = 0
    else:
        second_flight_minutes = int(re.search('H(.*)M', second_flight_duration).group(1))

    connection_minutes = (total_duration_hours*60+total_duration_minutes) - (first_flight_hours*60 + first_flight_minutes + second_flight_hours*60 + second_flight_minutes)
    hours = connection_minutes // 60
    minutes = connection_minutes % 60
    return str(hours)+':'+str(minutes)


def keep_date_remove_time(datetime):
    return datetime.split('T', 1)[0]
