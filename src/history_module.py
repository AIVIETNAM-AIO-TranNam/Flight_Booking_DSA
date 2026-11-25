import csv
from src.models import SinglyLinkedList

class HistoryAndManagementModule:
    def __init__(self):
        self.history_list = SinglyLinkedList()

    def add_booking_to_history(self, username, ticket_info):
        record = {"username": username, "ticket": ticket_info}
        self.history_list.append(record)
        try:
            with open("data/bookings.csv", "r", encoding="utf-8", newline="") as f:
                reader = csv.reader(f)
                for row in reader:
                    if not row:
                        continue
                    if row == ["username", "ticket"]:
                        continue
                    if len(row) == 2:
                        booking = {
                            "username": row[0],
                            "ticket": row[1]
                        }
                        self.history_list.append(booking)
        except FileNotFoundError:
            pass

    def view_user_bookings(self, username):
        user_bookings = []
        curr = self.history_list.head
        while curr:
            if curr.data["username"] == username:
                user_bookings.append(curr.data["ticket"])
            curr = curr.next
        return user_bookings