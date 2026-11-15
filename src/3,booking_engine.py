from src.models import Queue, PriorityQueue

class BookingEngineModule:
    def __init__(self):
        self.booking_queue = Queue()
        self.waitlist_pq = PriorityQueue()

    def select_seat(self, flight_code, seat_number, username):
        booking_request = {
            "flight_code": flight_code,
            "seat_number": seat_number,
            "username": username,
            "status": "Pending"
        }
        self.booking_queue.enqueue(booking_request)
        return booking_request

    def add_to_waitlist(self, username, flight_code, priority_score):
        self.waitlist_pq.enqueue_with_priority({"username": username, "flight_code": flight_code}, priority_score)

    def process_booking_queue(self):
        processed = []
        while not self.booking_queue.is_empty():
            req = self.booking_queue.dequeue()
            req["status"] = "Confirmed"
            processed.append(req)
        return processed