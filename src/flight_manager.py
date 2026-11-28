import csv
from src.models import SinglyLinkedList, HashTable

class FlightManagementModule:
    TICKET_MULTIPLIERS = {
        "promotional": 0.8,
        "economy": 1.0,
        "flexible": 1.3,
        "business": 2.0
    }

    def __init__(self, filepath="data/flights.csv", airports_filepath="data/airports.csv"):
        self.flights_list = SinglyLinkedList()
        self.airports_map = HashTable()
        self.filepath = filepath
        self.airports_filepath = airports_filepath

    def load_airports_from_file(self, filepath=None):
        target_path = filepath or self.airports_filepath
        try:
            with open(target_path, "r", encoding="utf-8", newline="") as f:
                reader = csv.reader(f)
                for row in reader:
                    if not row or row[0].lower() in ("airport_code", "code", "iata"):
                        continue
                    if len(row) >= 2:
                        self.airports_map.insert(row[0].strip().upper(), row[1].strip())
        except FileNotFoundError:
            pass

    def get_airport_name(self, code):
        full_name = self.airports_map.get(code.upper())
        return f"{code} ({full_name})" if full_name else code

    def _build_seat_classes(self, total_avail, base_price):
        promo = int(total_avail * 0.2)
        econ = int(total_avail * 0.4)
        flex = int(total_avail * 0.25)
        biz = total_avail - (promo + econ + flex)
        return {
            "promotional": {"seats": promo, "price": round(base_price * 0.8, 2)},
            "economy": {"seats": econ, "price": round(base_price * 1.0, 2)},
            "flexible": {"seats": flex, "price": round(base_price * 1.3, 2)},
            "business": {"seats": biz, "price": round(base_price * 2.0, 2)},
        }

    def load_flights_from_file(self, filepath=None):
        target_path = filepath or self.filepath
        with open(target_path, "r", encoding="utf-8", newline="") as f:
            reader = csv.reader(f)
            for row in reader:
                if not row or row[0] == "flight_id":
                    continue
                if len(row) not in (7, 8):
                    raise ValueError(
                        f"Unexpected flight row with {len(row)} columns: {row}"
                    )

                base_price = float(row[5])
                avail_seats = int(row[6])
                flight = {
                    "flight_id": row[0],
                    "origin": row[1],
                    "destination": row[2],
                    "depart_time": row[3],
                    "arrive_time": row[4],
                    "price": base_price,
                    "available_seats": avail_seats,
                    "seat_classes": self._build_seat_classes(avail_seats, base_price)
                }
                if len(row) == 8:
                    flight["total_seats"] = int(row[7])
                self.flights_list.append(flight)

    def search_flights(self, origin, destination, date):
        results = []
        curr = self.flights_list.head
        while curr:
            f = curr.data
            if (f["origin"].lower() == origin.lower() and 
                f["destination"].lower() == destination.lower() and 
                date in f["depart_time"]):
                results.append(f)
            curr = curr.next
        return results

    def search_round_trip(self, origin, destination, depart_date, return_date):
        outbound_flights = self.search_flights(origin, destination, depart_date)
        inbound_flights = self.search_flights(destination, origin, return_date)

        if depart_date == return_date and outbound_flights:
            earliest_arrive = min(f["arrive_time"] for f in outbound_flights)
            inbound_flights = [
                f for f in inbound_flights if f["depart_time"] > earliest_arrive
            ]

        return {
            "outbound": self.sort_flights_by_price(outbound_flights),
            "inbound": self.sort_flights_by_price(inbound_flights)
        }

    def get_flight_by_id(self, flight_id):
        curr = self.flights_list.head
        while curr:
            if curr.data["flight_id"] == flight_id:
                return curr.data
            curr = curr.next
        return None

    def book_seat_by_class(self, flight_id, ticket_class):
        flight = self.get_flight_by_id(flight_id)
        t_class = ticket_class.lower()
        if not flight or t_class not in flight["seat_classes"]:
            return False, 0.0
        if flight["seat_classes"][t_class]["seats"] <= 0:
            return False, flight["seat_classes"][t_class]["price"]

        flight["seat_classes"][t_class]["seats"] -= 1
        flight["available_seats"] -= 1
        return True, flight["seat_classes"][t_class]["price"]

    def sort_flights_by_price(self, flights):
        if len(flights) <= 1:
            return flights
        mid = len(flights) // 2
        left = self.sort_flights_by_price(flights[:mid])
        right = self.sort_flights_by_price(flights[mid:])
        return self._merge_price(left, right)

    def _merge_price(self, left, right):
        sorted_list = []
        i = j = 0
        while i < len(left) and j < len(right):
            if left[i]["price"] <= right[j]["price"]:
                sorted_list.append(left[i])
                i += 1
            else:
                sorted_list.append(right[j])
                j += 1
        sorted_list.extend(left[i:])
        sorted_list.extend(right[j:])
        return sorted_list