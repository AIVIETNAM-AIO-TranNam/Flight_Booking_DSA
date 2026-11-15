from src.models import SinglyLinkedList

class HistoryAndManagementModule:
    def __init__(self):
        self.history_list = SinglyLinkedList()

    def add_booking_to_history(self, username, ticket_info):
        record = {"username": username, "ticket": ticket_info}
        self.history_list.append(record)
        with open("data/bookings.txt", "a", encoding="utf-8") as f:
            f.write(f"{username},{ticket_info}\n")

    def view_user_bookings(self, username):
        user_bookings = []
        curr = self.history_list.head
        while curr:
            if curr.data["username"] == username:
                user_bookings.append(curr.data["ticket"])
            curr = curr.next
        return user_bookings