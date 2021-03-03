from django.dispatch import Signal

stk_payment_completed = Signal(providing_args=['transaction'])
b2c_payment_completed = Signal(providing_args=['transaction'])

