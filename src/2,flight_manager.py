from src.models import SinglyLinkedList

class FlightManagementModule:
    def __init__(self):
        self.flights_list = SinglyLinkedList()

    def load_flights_from_file(self, filepath="data/flights.txt"):
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                for line in f:
                    parts = line.strip().split(",")
                    if len(parts) == 6:
                        flight = {
                            "flight_code": parts[0],
                            "origin": parts[1],
                            "destination": parts[2],
                            "departure_time": parts[3],
                            "price": float(parts[4]),
                            "available_seats": int(parts[5])
                        }
                        self.flights_list.append(flight)
        except FileNotFoundError:
            pass

    def search_flights(self, origin, destination, date):
        results = []
        curr = self.flights_list.head
        while curr:
            f = curr.data
            if f["origin"].lower() == origin.lower() and f["destination"].lower() == destination.lower() and date in f["departure_time"]:
                results.append(f)
            curr = curr.next
        return results

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