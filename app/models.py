from django.db import models
from django.utils import timezone

class Customer(models.Model):
    name = models.CharField(max_length=20)
    phone_number = models.CharField(max_length=10)
    password = models.CharField(max_length=128)
    email = models.EmailField()
    age = models.IntegerField()
    job_position = models.CharField(max_length=30)

    def __str__(self):
        return self.name


class Finacial_statements(models.Model):
    name = models.ForeignKey(Customer, on_delete=models.CASCADE)
    income = models.DecimalField(max_digits=12, decimal_places=2)
    expenses = models.DecimalField(max_digits=12, decimal_places=2)
    assets = models.DecimalField(max_digits=12, decimal_places=2)
    is_saving_enough = models.BooleanField(default=False)
    is_overspending = models.BooleanField(default=False)
    
    INVESTMENT_RISK_CHOICES = [
        ("low", "Low"),
        ("medium", "Medium"),
        ("high", "High"),
    ]
    investment_risk = models.CharField(max_length=10, choices=INVESTMENT_RISK_CHOICES)
    
    emergency_savings = models.DecimalField(max_digits=12, decimal_places=2)
    is_debt_hurting = models.BooleanField(default=False)
    
    date = models.DateField(default=timezone.now)  # Month of the statement

    def __str__(self):
        return f"{self.name} - {self.date}"


    

class Liability(models.Model):
    statement = models.ForeignKey(Finacial_statements, on_delete=models.CASCADE, related_name="liability_items")

    LIABILITY_TYPES = [
        ("bank", "Bank Loan"),
        ("credit", "Credit Card"),
        ("personal", "Personal Loan"),
        ("mortgage", "Mortgage"),
        ("other", "Other"),
    ]
    liability_type = models.CharField(max_length=20, choices=LIABILITY_TYPES)
    amount = models.DecimalField(max_digits=12, decimal_places=2)

    def __str__(self):
        return f"{self.get_liability_type_display()} - ₹{self.amount}"
    
class Financial_goals(models.Model):
    goals = models.ForeignKey(Finacial_statements, on_delete=models.CASCADE, related_name="goals_list")
    goal_type = models.CharField(max_length=50)


class FinancialAdvice(models.Model):
    user = models.ForeignKey(Customer, on_delete=models.CASCADE)  # or use Customer
    statement = models.ForeignKey(Finacial_statements, on_delete=models.CASCADE)
    is_saving_enough = models.BooleanField(null=True, blank=True)
    can_achieve_goal = models.BooleanField(null=True, blank=True)
    advice_text = models.TextField()  # Store full advice as plain text or JSON
    created_at = models.DateTimeField(auto_now_add=True)
    score = models.IntegerField(default=0)

    def __str__(self):
        return f"Advice for {self.user.name} - Advice on {self.created_at.strftime('%Y-%m-%d')}"
