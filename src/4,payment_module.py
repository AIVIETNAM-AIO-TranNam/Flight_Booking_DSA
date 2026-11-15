import random

class PaymentAndTicketModule:
    def process_payment(self, booking_info, amount):
        if amount > 0:
            ticket_code = self.generate_ticket_code()
            return True, ticket_code
        return False, "Payment failed!"

    def generate_ticket_code(self):
        code = "TKT-"
        for _ in range(6):
            code += random.choice("ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789")
        return code