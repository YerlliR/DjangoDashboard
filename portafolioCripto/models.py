from django.db import models
from django.contrib.auth.models import User

class Crypto(models.Model):
    name = models.CharField(max_length=100)
    symbol = models.CharField(max_length=100)
    logo = models.CharField(max_length=100)
    deprecated = models.BooleanField()

    def __str__(self):
        return self.name

class Crypto_price(models.Model):
    crypto = models.ForeignKey(Crypto, on_delete=models.CASCADE)
    date = models.DateField()
    price = models.FloatField()
    market_cap = models.FloatField(null=True, blank=True)

    def __str__(self):
        return f"{self.crypto.name} - {self.date}"

class Wallet(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Transaction(models.Model):
    wallet = models.ForeignKey(Wallet, on_delete=models.CASCADE)
    crypto = models.ForeignKey(Crypto, on_delete=models.CASCADE)
    date = models.DateField()
    amount = models.FloatField()

    def __str__(self):
        return f"{self.wallet.user.username} - {self.wallet.name} - {self.crypto.name}"
