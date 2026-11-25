import csv
from src.models import SinglyLinkedList

class FlightManagementModule:
    def __init__(self, filepath="data/flights.csv"):
        self.flights_list = SinglyLinkedList()
        self.filepath = filepath

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

                flight = {
                    "flight_id": row[0],
                    "origin": row[1],
                    "destination": row[2],
                    "depart_time": row[3],
                    "arrive_time": row[4],
                    "price": float(row[5]),
                    "available_seats": int(row[6]),
                }
                if len(row) == 8:
                    flight["total_seats"] = int(row[7])
                self.flights_list.append(flight)

    def search_flights(self, origin, destination, date):
        results = []
        curr = self.flights_list.head
        while curr:
            f = curr.data
            if f["origin"].lower() == origin.lower() and f["destination"].lower() == destination.lower() and date in f["depart_time"]:
                results.append(f)
            curr = curr.next
        return results
    def get_flight_by_id(self, flight_id):
        curr = self.flights_list.head
        while curr:
            if curr.data["flight_id"] == flight_id:
                return curr.data
            curr = curr.next
        return None
    def sort_flights_by_price(self, flights):
        if len(flights) <= 1:
            return flights
        mid = len(flights) // 2
        left = self.sort_flights_by_price(flights[:mid]) #recursion
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