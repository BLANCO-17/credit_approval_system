from .models import Customer, Loan
from django.db.models import Sum
import datetime

def calculate_credit_score(customer_id):
    try:
        # Query historical loan data for the customer from the Loan table
        loans = Loan.objects.filter(customer_id=customer_id)

        # Component i: Past Loans paid on time
        past_loans_paid_on_time = loans.filter(emis_paid_on_time=True).count()

        # Component ii: No of loans taken in past
        num_loans_taken = loans.count()

        # Component iii: Loan activity in current year
        current_year = datetime.datetime.now().year
        loans_current_year = loans.filter(start_date__year=current_year)
        loan_activity_current_year = loans_current_year.count()

        # Component iv: Loan approved volume
        loan_approved_volume = loans.aggregate(Sum('loan_amount'))['loan_amount__sum'] or 0
        
        # Component v: If sum of current loans > approved limit, credit score = 0
        approved_limit = Customer.objects.get(customer_id=customer_id).approved_limit
        sum_current_loans = loans.aggregate(Sum('loan_amount'))['loan_amount__sum'] or 0
        
        if sum_current_loans > approved_limit:
            return 0

        # Combine components to calculate credit score
        # You may assign weights to each component and adjust the formula as needed
        credit_score = (past_loans_paid_on_time * 20 +
                        num_loans_taken * 20 +
                        loan_activity_current_year * 20 +
                        loan_approved_volume * 20 +
                        approved_limit * 20)

        # Scale the credit score to fit within the range of 0 to 100
        credit_score = min(100, max(0, credit_score))

        return credit_score

    except Customer.DoesNotExist:
        return None

def determine_loan_approval(credit_rating, interest_rate):
    # Determine loan approval based on credit rating and interest rate
    # Adjust the conditions as needed based on your specific criteria
    if credit_rating > 50:
        approval = True
        corrected_interest_rate = interest_rate
    elif 30 < credit_rating <= 50 and interest_rate > 12:
        approval = True
        corrected_interest_rate = interest_rate
    elif 10 < credit_rating <= 30 and interest_rate > 16:
        approval = True
        corrected_interest_rate = interest_rate
    else:
        approval = False
        corrected_interest_rate = None
    
    return approval, corrected_interest_rate

def calculate_monthly_installment(loan_amount, interest_rate, tenure):
    # Calculate monthly installment based on loan amount, interest rate, and tenure
    # Formula for calculating EMI: EMI = [P * r * (1 + r)^n] / [(1 + r)^n - 1]
    # Where P = Loan amount, r = Monthly interest rate, n = Total number of payments (tenure in months)

    # Convert interest rate from annual to monthly and percentage to decimal
    r = interest_rate / (12 * 100)

    # Calculate the total number of payments
    n = tenure

    # Calculate EMI
    monthly_installment = (loan_amount * r * (1 + r)**n) / ((1 + r)**n - 1)
    
    return monthly_installment

