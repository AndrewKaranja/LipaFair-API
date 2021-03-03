class CleanPhoneNumber(object):
    def __init__(self, phone_number):
        self.phone_number = phone_number

    def sanitize_phone_number(self):
        phone_number = self.phone_number
        phone = list(phone_number)
        prefix = phone[0]
        length = len(phone_number)

        if prefix == '0' and length == 10:
            phone[0] = '254'
            return "".join(phone)

        elif prefix == '2' and length == 12:
            return str(phone_number)

        elif length < 10:
            return ''

        else:
            return ''

    def phone_number_with_plus(self):
        phone_number = self.phone_number
        phone = list(phone_number)
        prefix = phone[0]
        length = len(phone_number)

        if prefix == '0' and length == 10:
            phone[0] = '+254'
            return "".join(phone)

        elif prefix == '2' and length == 12:
            phone[0] = '+'
            return "".join(phone)

        elif prefix == '+' and length == 13:
            return str(phone_number)

        elif length < 10:
            return ''

        else:
            return ''
