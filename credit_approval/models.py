from django.db import models

class Customer(models.Model):
    customer_id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=15)
    monthly_salary = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    approved_limit = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    current_debt = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    age = models.IntegerField(default=18)

class Loan(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    loan_id = models.AutoField(primary_key=True)
    loan_amount = models.DecimalField(max_digits=10, decimal_places=2)
    tenure = models.IntegerField()
    interest_rate = models.DecimalField(max_digits=5, decimal_places=2)
    monthly_repayment = models.DecimalField(max_digits=10, decimal_places=2)
    emis_paid_on_time = models.IntegerField(default=0, null=True)
    start_date = models.DateField(default=None, null=True)
    end_date = models.DateField(default=None, null=True)
