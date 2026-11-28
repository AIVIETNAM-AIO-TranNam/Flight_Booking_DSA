import random

class PaymentAndTicketModule:

    def process_payment(self, booking_info, amount):
        if amount <= 0:
            return False, "Payment failed!"

        quantity = booking_info["quantity"]

        ticket_codes = []

        for _ in range(quantity):
            ticket_codes.append(self.generate_ticket_code())

        return True, ticket_codes

    
    def generate_ticket_code(self):
        code = "TKT-" #TicKeT
        for _ in range(6):
            code += random.choice("ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789")
        return code
# payment = PaymentAndTicketModule()
# for i in range(5):
#     code = payment.generate_ticket_code()
#     print(code)
