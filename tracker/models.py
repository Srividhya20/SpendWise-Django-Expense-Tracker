from django.conf import settings
from django.db import models
from django.utils import timezone

class Category(models.Model):
    name = models.CharField(max_length=50, unique=True)
    def __str__(self):
        return self.name

class Expense(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=120)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(Category, on_delete=models.PROTECT)
    date = models.DateField(default=timezone.localdate)
    note = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        ordering = ["-date", "-created_at"]
    def __str__(self):
        return f"{self.title} - {self.amount}"

class MonthlyBudget(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    month = models.DateField(help_text="Use the first day of the month")
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    class Meta:
        unique_together = ("user", "month")
        ordering = ["-month"]
    def __str__(self):
        return f"{self.user} - {self.month:%B %Y}"
