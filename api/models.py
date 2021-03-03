from django.db import models

# Create your models here.
class Wallet(models.Model):
    #same as docKey
    wallet_id = models.CharField(max_length=128,)
    user_id = models.CharField(max_length=128,)
    current_balance = models.DecimalField(max_digits=9, decimal_places=2)
    last_updated = models.DateTimeField(auto_now_add=True)