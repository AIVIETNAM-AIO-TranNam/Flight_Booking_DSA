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
    flight_mgr.load_airports_from_file()

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
def display_flight_details(flights, flight_mgr):
    for f in flights:
        sc = f["seat_classes"]
        orig_name = flight_mgr.get_airport_name(f["origin"])
        dest_name = flight_mgr.get_airport_name(f["destination"])
        print(f"ID: {f['flight_id']} | {orig_name} -> {dest_name} | Depart: {f['depart_time']} | Arrive: {f['arrive_time']}")
        print(
            f"   Classes -> Promotional: {sc['promotional']['seats']} (${sc['promotional']['price']}) | "
            f"Economy: {sc['economy']['seats']} (${sc['economy']['price']}) | "
            f"Flexible: {sc['flexible']['seats']} (${sc['flexible']['price']}) | "
            f"Business: {sc['business']['seats']} (${sc['business']['price']})"
        )

def user_menu(user_mgr, flight_mgr, booking_eng, payment_mod, history_mgr):
    while True:
        print(f"\n--- USER MENU ({user_mgr.current_user['username']}) ---")
        print("1. Search Flights (One-Way)")
        print("2. Search Flights (Round-Trip)")
        print("3. Book Flight (One-Way)")
        print("4. Book Flight (Round-Trip)")
        print("5. View My Bookings")
        print("6. Logout")
        choice = input("Select option: ").strip()

        if choice == "1":
            orig = input("Origin: ").strip()
            dest = input("Destination: ").strip()
            date = input("Date (YYYY-MM-DD): ").strip()
            flights = flight_mgr.search_flights(orig, dest, date)
            sorted_flights = flight_mgr.sort_flights_by_price(flights)
            print(f"\nFound {len(sorted_flights)} flights:")
            display_flight_details(sorted_flights, flight_mgr)

        elif choice == "2":
            orig = input("Origin: ").strip()
            dest = input("Destination: ").strip()
            dep_date = input("Depart Date (YYYY-MM-DD): ").strip()
            ret_date = input("Return Date (YYYY-MM-DD): ").strip()
            rt_flights = flight_mgr.search_round_trip(orig, dest, dep_date, ret_date)
            print(f"\n--- OUTBOUND FLIGHTS ({len(rt_flights['outbound'])}) ---")
            display_flight_details(rt_flights["outbound"], flight_mgr)
            print(f"\n--- INBOUND FLIGHTS ({len(rt_flights['inbound'])}) ---")
            display_flight_details(rt_flights["inbound"], flight_mgr)

        elif choice == "3":
            f_id = input("Enter Flight ID: ").strip()
            t_class = input("Ticket Class (promotional/economy/flexible/business): ").strip().lower()
            seat = input("Enter Seat Number (e.g., 12A): ").strip()

            ok, price = flight_mgr.book_seat_by_class(f_id, t_class)
            if not ok:
                print(f"No {t_class} seats available or invalid Flight ID!")
                if flight_mgr.get_flight_by_id(f_id):
                    booking_eng.add_to_waitlist(user_mgr.current_user["username"], f_id, t_class)
                    print("You have been added to the priority waitlist.")
                continue

            booking_eng.select_seat(f_id, seat, user_mgr.current_user["username"], t_class)
            processed = booking_eng.process_booking_queue()
            success, ticket = payment_mod.process_payment(processed[0], price)
            if success:
                history_mgr.add_booking_to_history(
                    user_mgr.current_user["username"],
                    f"{ticket} | {f_id} | {t_class} | Seat {seat} | ${price}"
                )
                print(f"Booking successful! Ticket Code: {ticket} | Total: ${price}")

        elif choice == "4":
            out_id = input("Outbound Flight ID: ").strip()
            out_seat = input("Outbound Seat (e.g., 12A): ").strip()
            in_id = input("Inbound Flight ID: ").strip()
            in_seat = input("Inbound Seat (e.g., 14B): ").strip()
            t_class = input("Ticket Class (promotional/economy/flexible/business): ").strip().lower()

            ok_out, price_out = flight_mgr.book_seat_by_class(out_id, t_class)
            ok_in, price_in = flight_mgr.book_seat_by_class(in_id, t_class)

            if not (ok_out and ok_in):
                print("One or both flights do not have enough seats in this class!")
                continue

            booking_eng.select_round_trip(out_id, out_seat, in_id, in_seat, user_mgr.current_user["username"], t_class)
            processed = booking_eng.process_booking_queue()
            total_price = round((price_out + price_in) * 0.95, 2)

            success_out, tkt_out = payment_mod.process_payment(processed[0], price_out)
            success_in, tkt_in = payment_mod.process_payment(processed[1], price_in)

            if success_out and success_in:
                username = user_mgr.current_user["username"]
                history_mgr.add_booking_to_history(username, f"{tkt_out} (Outbound) | {out_id} | {t_class} | Seat {out_seat}")
                history_mgr.add_booking_to_history(username, f"{tkt_in} (Inbound) | {in_id} | {t_class} | Seat {in_seat}")
                print(f"Round-trip booking successful! Total paid (5% off): ${total_price}")
                print(f"Outbound Ticket: {tkt_out} | Inbound Ticket: {tkt_in}")

        elif choice == "5":
            bookings = history_mgr.view_user_bookings(user_mgr.current_user["username"])
            print("My Bookings:", bookings)

        elif choice == "6":
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