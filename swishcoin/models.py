from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

MAX_SUPPLY = 1000000  # Maximum total supply of SwishCoins


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)  # SwishCoin Balance

    @staticmethod
    def total_supply():
        """Returns the total circulating supply of SwishCoins."""
        return sum(profile.balance for profile in UserProfile.objects.all())

    @staticmethod
    def can_create_new_coins(amount):
        """Checks if new coins can be created without exceeding MAX_SUPPLY."""
        return UserProfile.total_supply() + amount <= MAX_SUPPLY

    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            UserProfile.objects.create(user=instance)

    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance, **kwargs):
        instance.profile.save()


class Question(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField()
    bounty = models.DecimalField(default=0, max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)


class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name="answers")
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    votes = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)


class Transaction(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name="sent_transactions", null=True, blank=True)
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name="received_transactions")
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    timestamp = models.DateTimeField(auto_now_add=True)
    transaction_type = models.CharField(
        max_length=20,
        choices=[("transfer", "Transfer"), ("mining", "Mining"), ("reward", "Reward")],
        default="transfer"  # ✅ Set default to prevent migration errors
    )

    def __str__(self):
        return f"{self.sender} -> {self.receiver}: {self.amount}"


class Block(models.Model):  # Renamed from Blockchain
    previous_hash = models.CharField(max_length=64)
    timestamp = models.DateTimeField(auto_now_add=True)
    nonce = models.IntegerField()
    hash = models.CharField(max_length=64)
