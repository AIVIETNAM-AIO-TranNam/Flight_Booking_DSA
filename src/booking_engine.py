from src.models import Queue, PriorityQueue

class BookingEngineModule:
    def __init__(self):
        self.booking_queue = Queue()
        self.waitlist_pq = PriorityQueue()

    def select_seats(self, flight_id, seat_numbers, username):
        if not seat_numbers: 
            raise ValueError("Phải chọn ít nhất 1 ghế")
        if len(seat_numbers) != len(set(seat_numbers)):
            raise ValueError("Chỗ ngồi bị trùng")
        booking_request = {
            "flight_id": flight_id,
            "seat_numbers": seat_numbers,
            "quantity": len(seat_numbers),
            "username": username,
            "status": "Pending"
        }
        self.booking_queue.enqueue(booking_request)
        return booking_request

    def add_to_waitlist(self, username, flight_id, priority_score):
        self.waitlist_pq.enqueue_with_priority({"username": username, "flight_id": flight_id}, priority_score)

    def process_booking_queue(self):
        processed = []
        while not self.booking_queue.is_empty():
            req = self.booking_queue.dequeue()
            req["status"] = "Confirmed"
            processed.append(req)
        return processed