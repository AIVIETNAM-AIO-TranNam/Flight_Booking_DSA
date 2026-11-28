from src.models import Queue, PriorityQueue

class BookingEngineModule:
    PRIORITY_MAP = {
        "promotional": 10,
        "economy": 20,
        "flexible": 30,
        "business": 40
    }

    def __init__(self):
        self.booking_queue = Queue()
        self.waitlist_pq = PriorityQueue()

    def select_seat(self, flight_id, seat_number, username, ticket_class="economy", trip_type="one-way"):
        booking_request = {
            "flight_id": flight_id,
            "seat_number": seat_number,
            "username": username,
            "ticket_class": ticket_class.lower(),
            "trip_type": trip_type,
            "status": "Pending"
        }
        self.booking_queue.enqueue(booking_request)
        return booking_request

    def select_round_trip(self, out_flight_id, out_seat, in_flight_id, in_seat, username, ticket_class="economy"):
        req_out = self.select_seat(out_flight_id, out_seat, username, ticket_class, trip_type="round-trip-outbound")
        req_in = self.select_seat(in_flight_id, in_seat, username, ticket_class, trip_type="round-trip-inbound")
        return req_out, req_in

    def add_to_waitlist(self, username, flight_id, ticket_class="economy", priority_score=None):
        score = priority_score if priority_score is not None else self.PRIORITY_MAP.get(ticket_class.lower(), 10)
        self.waitlist_pq.enqueue_with_priority(
            {"username": username, "flight_id": flight_id, "ticket_class": ticket_class.lower()},
            score
        )

    def process_booking_queue(self):
        processed = []
        while not self.booking_queue.is_empty():
            req = self.booking_queue.dequeue()
            req["status"] = "Confirmed"
            processed.append(req)
        return processed