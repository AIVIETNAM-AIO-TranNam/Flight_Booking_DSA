import random

class PaymentAndTicketModule:
    def process_payment(self, booking_info, amount):
        #cần bổ sung thêm cụ thể booking_info gồm những thông tin gì
        if amount > 0:
            ticket_code = self.generate_ticket_code()
            return True, ticket_code
        return False, "Payment failed!"

    def generate_ticket_code(self):
        code = "TKT-" #TicKeT
        for _ in range(6):
            code += random.choice("ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789")
        return code
# payment = PaymentAndTicketModule()
# for i in range(5):
#     code = payment.generate_ticket_code()
#     print(code)
