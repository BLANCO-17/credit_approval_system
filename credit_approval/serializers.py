# serializers.py

from rest_framework import serializers

class RegistrationSerializer(serializers.Serializer):
    first_name = serializers.CharField(max_length=100)
    last_name = serializers.CharField(max_length=100)
    age = serializers.IntegerField()
    phone_number = serializers.CharField(max_length=15)
    monthly_income = serializers.DecimalField(max_digits=10, decimal_places=2)

class EligibilitySerializer(serializers.Serializer):
    customer_id = serializers.IntegerField()
    loan_amount = serializers.DecimalField(max_digits=10, decimal_places=2)    
    interest_rate = serializers.DecimalField(max_digits=3, decimal_places=2)
    tenure = serializers.IntegerField()
    
class CreateLoanSerializer(serializers.Serializer):
    customer_id = serializers.IntegerField()
    loan_amount = serializers.DecimalField(max_digits=10, decimal_places=2)    
    interest_rate = serializers.DecimalField(max_digits=3, decimal_places=2)
    tenure = serializers.IntegerField()

