import sys

from src.user_manager import UserManagerModule
from src.flight_manager import FlightManagementModule
from src.booking_engine import BookingEngineModule
from src.payment_module import PaymentAndTicketModule
from src.history_module import HistoryAndManagementModule

def main():
    user_mgr = UserManagerModule()
    flight_mgr = FlightManagementModule()
    booking_eng = BookingEngineModule()
    payment_mod = PaymentAndTicketModule()
    history_mgr = HistoryAndManagementModule()

    user_mgr.load_users_from_file()
    flight_mgr.load_flights_from_file()

    print("=== FLIGHT TICKET BOOKING SYSTEM (TERMINAL CLI) ===")
    
    while True:
        print("\n1. Register\n2. Login\n3. Exit")
        choice = input("Select option: ")
        
        if choice == "1":
            u = input("Username: ")
            p = input("Password: ")
            success, msg = user_mgr.register_user(u, p)
            print(msg)
        elif choice == "2":
            u = input("Username: ")
            p = input("Password: ")
            success, msg = user_mgr.authenticate_user(u, p)
            print(msg)
            if success:
                user_menu(user_mgr, flight_mgr, booking_eng, payment_mod, history_mgr)
        elif choice == "3":
            print("Goodbye!")
            break
        else:
            print("Invalid option!")
def user_menu(user_mgr, flight_mgr, booking_eng, payment_mod, history_mgr):
    while True:
        print(f"\n--- USER MENU ({user_mgr.current_user['username']}) ---")
        print("1. Search Flights")
        print("2. Book Flight & Select Seat")
        print("3. View My Bookings")
        print("4. Logout")
        choice = input("Select option: ")

        if choice == "1":
            orig = input("Origin: ")
            dest = input("Destination: ")
            date = input("Date (YYYY-MM-DD): ")
            flights = flight_mgr.search_flights(orig, dest, date)
            sorted_flights = flight_mgr.sort_flights_by_price(flights)
            print(f"Found {len(sorted_flights)} flights (sorted by price):")
            for f in sorted_flights:
                print(f"Code: {f['flight_id']} | {f['origin']} -> {f['destination']} | Time: {f['depart_time']} | Price: {f['price']} VND | Seats: {f['available_seats']}")
        elif choice == "2":
            f_code  = input("Enter Flight Code: ")
            flight = flight_mgr.get_flight_by_id(f_code)
            if flight is None :
                print("Flight not found!")
                continue
            available = flight["available_seats"]
            if available <= 0:
                print("This flight is fully booked")
                continue
            print(f"Available seats:{available}")
            try:
                quantity=int(input("Enter ticket quantity: "))
                if quantity<=0:
                    print("Quantity must be greater than 0!")
                    continue
                if quantity>available:
                    print("Not enough available seats!")
                    continue
            except ValueError:
                print("Please enter a valid number!")
                continue
            seat_numbers=[]
            for i in range (quantity):
                seat=input(f"Enter seat number {i+1}: ")
                seat_numbers.append(seat)
            try:
                req = booking_eng.select_seats(
                    f_code,
                    seat_numbers,
                    user_mgr.current_user["username"]
                )
            except ValueError as e:
                print(e)
                continue
            processed = booking_eng.process_booking_queue()
            amount = flight["price"]*quantity
            success, ticket_codes = payment_mod.process_payment(
                processed[0],
                amount
            )
            if success:
                flight["available_seats"] -= quantity
                booking_info={
                    "flight_id":f_code,
                    "tickets":[
                        {
                            "seat":seat,
                            "ticket_code":ticket_codes[i]
                        }
                        for i,  seat in enumerate(seat_numbers)
                    ],
                    "quantity":quantity,
                    "total_amount":amount
                }
                history_mgr.add_booking_to_history(
                    user_mgr.current_user["username"],
                    booking_info
                )
                print("Booking successful!")
                print(f"Quantity: {quantity}")
                print(f"Total amount: {amount} VND")
                for ticket in booking_info["tickets"]:
                    print(f"Seat: {ticket['seat']} | Ticket Code: {ticket['ticket_code']}")



        elif choice == "3":
            bookings = history_mgr.view_user_bookings(user_mgr.current_user["username"])
            print("My Bookings:", bookings)
        elif choice == "4":
            user_mgr.current_user = None
            break


def run_demo():
    flight_mgr = FlightManagementModule()
    booking_eng = BookingEngineModule()
    payment_mod = PaymentAndTicketModule()

    flight_mgr.load_flights_from_file()

    curr = flight_mgr.flights_list.head
    flight = None
    while curr:
        if curr.data["available_seats"] > 0:
            flight = curr.data
            break
        curr = curr.next

    if flight is None:
        raise RuntimeError("No flights with available seats were found.")

    request = booking_eng.select_seat(
        flight["flight_id"], "DEMO-1", "demo_user"
    )
    processed = booking_eng.process_booking_queue()
    if not processed:
        raise RuntimeError("The booking request was not processed.")

    success, ticket = payment_mod.process_payment(
        processed[-1], flight["price"]
    )
    if not success:
        raise RuntimeError(f"Demo payment failed: {ticket}")

    print("Demo booking successful!")
    print(f"Flight: {flight['flight_id']}")
    print(f"Seat: {request['seat_number']}")
    print(f"Amount: {flight['price']} VND")
    print(f"Ticket: {ticket}")


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--demo":
        run_demo()
    else:
        main()