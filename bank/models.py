from django.db import models
from django.conf import settings
from django.urls import reverse

# Create your models here.

class Account(models.Model):
    name = models.CharField(max_length=50, default="Account")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    balance = models.IntegerField(default=0, null=False)

    def get_delete_url(self):
        kwargs = {
            "id": self.id
        }

        return reverse("delete-account", kwargs=kwargs)
    def __str__(self):
        return f"{self.user.username}"
    
    def get_transaction_url(self):
        kwargs = {
            "id": self.id
        }
        return reverse("new-transaction", kwargs=kwargs)

class Transaction(models.Model):
    from_account = models.ForeignKey("Account", on_delete=models.CASCADE, related_name="+")
    to_account = models.ForeignKey("Account", on_delete=models.CASCADE, related_name="+")
    amount = models.PositiveIntegerField(null=False, default=0,)
    date = models.DateTimeField(auto_now_add=True)
    type = models.CharField(max_length=100)

