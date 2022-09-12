from django.db import models
from django.contrib.auth.models import User


class Family(models.Model):
    name = models.CharField(max_length=200)
    creation_date = models.DateTimeField("creation date", auto_now_add=True)
    users = models.ManyToManyField(User, related_name='users', blank=True)

    def __str__(self):
        return self.name


class Budget(models.Model):
    name = models.CharField(max_length=200)
    creation_date = models.DateTimeField("creation date", auto_now_add=True)
    last_update = models.DateTimeField("last update", auto_now=True)
    owner = models.CharField(max_length=200)
    family = models.ForeignKey(Family, on_delete=models.CASCADE, related_name='family')
    users = models.ManyToManyField(User, related_name='budget_users', blank=True)

    def __str__(self):
        return self.name


class IncomeTransaction(models.Model):
    class IncomeCategories(models.TextChoices):
        OTHER = "Other"
        SALARY = "Salary"
        GIFT = "Gift"
        PAYBACK = "Payback"

    category = models.CharField(
        max_length=20,
        choices=IncomeCategories.choices,
        default=IncomeCategories.OTHER
    )
    amount = models.FloatField()
    budget = models.ForeignKey(
        Budget,
        on_delete=models.CASCADE,
        related_name='income'
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    creation_date = models.DateTimeField("creation date", auto_now_add=True)


class ExpenseTransaction(models.Model):

    class ExpenseCategories(models.TextChoices):
        OTHER = 'Other'
        FOOD = "Food"
        HOUSING = "Housing"
        TRANSPORTATION = "Transportation"
        UTILITIES = "Utilities"
        HEALTHCARE = "Heathcare"
        CHILD = "Child"
        PERSONAL = "Personal"
        ENTERTAINMENT = "Entertainment"
        HOLIDAYS = "Holidays"
        GIFTS = "Gifts"
        SAVINGS = "Savings"

    category = models.CharField(
        max_length=20,
        choices=ExpenseCategories.choices,
        default=ExpenseCategories.OTHER
    )
    amount = models.FloatField()
    budget = models.ForeignKey(
        Budget,
        on_delete=models.CASCADE,
        related_name='expense',
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    creation_date = models.DateTimeField("creation date", auto_now_add=True)



