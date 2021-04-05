import datetime

from api.models import Discount


class CouponManager(object):
    def __init__(self, discount_id=None):
        self.discount_id = discount_id

    def redeem_coupon(self):
        try:
            discount = Discount.objects.get(id=self.discount_id)
            discount.applied = True
            discount.date_applied = datetime.datetime.now()
            discount.coupon.times_redeemed +=1
            discount.save()
            return True
        except Discount.DoesNotExist as e:
            print(e)
            return False

