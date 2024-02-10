from django.http import JsonResponse 
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status   

from .models import Customer, Loan
from .serializers import RegistrationSerializer, EligibilitySerializer, CreateLoanSerializer
from .utils import calculate_credit_score, calculate_monthly_installment, determine_loan_approval

import math, datetime

def round_up_to_nearest_lakh(salary):
    return math.ceil(salary / 100000) * 100000


class RegistrationView(APIView):
    
    def post(self, request):
        serializer = RegistrationSerializer(data=request.data)
        # print("in function")
        if serializer.is_valid():
            
            app_limit = 36 * round_up_to_nearest_lakh(serializer.validated_data['monthly_income'])
            customer = Customer.objects.create(
                first_name = serializer.validated_data['first_name'],
                last_name = serializer.validated_data['last_name'],
                age = serializer.validated_data['age'],
                phone_number = serializer.validated_data['phone_number'],
                monthly_salary = serializer.validated_data['monthly_income'],
                approved_limit = app_limit
            )
            
            out = {
                'customer_id': customer.customer_id,
                'name': customer.first_name + ' ' + customer.last_name,
                'age': customer.age,
                'monthly_income': customer.monthly_salary,
                'approved_limit': customer.approved_limit,
                'phone_number': customer.phone_number
            }
            return Response(out, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        


class EligibilityView(APIView):
    
    def post(self, request):
        
        serializer = EligibilitySerializer(data=request.data)
        
        if(serializer.is_valid()):
            
            customer_id = request.data.get('customer_id')
            loan_amount = request.data.get('loan_amount')
            interest_rate = request.data.get('interest_rate')
            tenure = request.data.get('tenure')
            
            try:
                customer = Customer.objects.get(customer_id=customer_id)
            except Customer.DoesNotExist:
                return Response({"error": f"Customer with id {customer_id} does not exist"}, status=status.HTTP_400_BAD_REQUEST)

            # Calculate credit rating based on customer data
            credit_rating = calculate_credit_score(customer.customer_id)

            # Determine if the loan can be approved based on credit rating and other conditions
            approval, corrected_interest_rate = determine_loan_approval(credit_rating, interest_rate)

            # Calculate monthly installment
            monthly_installment = calculate_monthly_installment(loan_amount, interest_rate, tenure)

            # Prepare response body
            response_data = {
                "customer_id": customer_id,
                "approval": approval,
                "interest_rate": interest_rate,
                "corrected_interest_rate": corrected_interest_rate,
                "tenure": tenure,
                "monthly_installment": monthly_installment
            }

            return Response(response_data, status=status.HTTP_200_OK)
                
            # Fetch customer data from Customer model
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    
class CreateLoanView(APIView):
    
    def post(self, request):
        
        serializer = CreateLoanSerializer(data=request.data)
        
        if(serializer.is_valid()):
            
            customer_id = serializer.validated_data["customer_id"]
            loan_amount = serializer.validated_data["loan_amount"]
            interest_rate = serializer.validated_data["interest_rate"]
            tenure = serializer.validated_data["tenure"]
            

            # Check customer eligibility for the loan
            credit_score = calculate_credit_score(customer_id=customer_id)
            if credit_score is None:
                return Response({
                    'loan_id': None,
                    'customer_id': customer_id,
                    'loan_approved': False,
                    'message': 'Customer not found',
                    'monthly_installment': None
                }, status=400)

            approval, corrected_interest_rate = determine_loan_approval(credit_score, interest_rate)

            # Calculate monthly installment regardless of approval status
            monthly_installment = None
            if approval:
                monthly_installment = calculate_monthly_installment(loan_amount, corrected_interest_rate, tenure)

            # Process loan approval and save to database
            if approval:
                # print("here")
                loan = Loan.objects.create(customer_id=customer_id, loan_amount=loan_amount, monthly_repayment=monthly_installment,  interest_rate=corrected_interest_rate, tenure=tenure, start_date=datetime.datetime.now().date())
                return Response({
                    'loan_id': loan.loan_id,
                    'customer_id': customer_id,
                    'loan_approved': True,
                    'message': "Loan Approved.",
                    'monthly_installment': monthly_installment
                }, status=status.HTTP_201_CREATED)
            else:
                return Response({
                    'loan_id': None,
                    'customer_id': customer_id,
                    'loan_approved': False,
                    'message': 'Loan not approved due to credit rating',
                    'monthly_installment': None
                }, status=400)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


def view_loan(request, loan_id):
    
    try:
        # Query loan details using the provided loan_id
        loan = Loan.objects.get(loan_id=loan_id)

        # Query customer details related to the loan
        customer = Customer.objects.get(customer_id=loan.customer.customer_id)

        # Construct the response body
        response_body = {
            'loan_id': loan.loan_id,
            'customer': {
                'id': customer.customer_id,
                'first_name': customer.first_name,
                'last_name': customer.last_name,
                'phone_number': customer.phone_number,
                'age': customer.age
            },
            'loan_amount': loan.loan_amount,
            'interest_rate': loan.interest_rate,
            'monthly_installment': loan.monthly_repayment,
            'tenure': loan.tenure
        }   

        return JsonResponse(response_body, status=status.HTTP_200_OK)

    except Loan.DoesNotExist:
        return JsonResponse({'message': 'Loan not found'}, status=status.HTTP_404_NOT_FOUND)

    except Customer.DoesNotExist:
        return JsonResponse({'message': 'Customer not found'}, status=status.HTTP_404_NOT_FOUND)
    
    
def view_loans_for_customer(request, customer_id):
    try:
        # Query all loans associated with the provided customer ID
        loans = Loan.objects.filter(customer=customer_id)

        # Construct a list of loan items
        loan_items = []
        for loan in loans:
            loan_item = {
                'loan_id': loan.loan_id,
                'loan_amount': loan.loan_amount,
                'interest_rate': loan.interest_rate,
                'monthly_installment': loan.monthly_repayment,
                'tenure': loan.tenure
                # Add other loan details as needed
            }
            loan_items.append(loan_item)
            
            # If no loans are found, return an empty dictionary with keys but empty values
        if not loan_items:
            return JsonResponse({
                'loan_id': None,
                'loan_amount': None,
                'interest_rate': None,
                'monthly_installment': None,
                'tenure': None
                # Add other loan details keys with empty values as needed
            })

        # Return the list of loan items in the response body
        return JsonResponse(loan_items, status=status.HTTP_200_OK, safe=False)

    except Loan.DoesNotExist:
        return JsonResponse({'message': 'No loans found for the customer'}, status=404)