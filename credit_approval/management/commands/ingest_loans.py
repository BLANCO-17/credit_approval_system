# myapp/management/commands/ingest_loans.py
import pandas as pd
from django.core.management.base import BaseCommand
from credit_approval.models import Loan, Customer  # Adjust the import statement based on your app name and model location

class Command(BaseCommand):
    help = 'Ingest loan data from loan_data.xlsx'

    def handle(self, *args, **options):

        cust_file_path = 'data/customer_data.xlsx'  # Update with the actual path to your loan_data.xlsx file
        df = pd.read_excel(cust_file_path)

        for _, row in df.iterrows():
            try:
                Customer.objects.update_or_create(
                customer_id=row['Customer ID'],
                first_name=row['First Name'],
                last_name=row['Last Name'],
                age=row['Age'],
                phone_number=row['Phone Number'],
                monthly_salary=row['Monthly Salary'],
                approved_limit=row['Approved Limit'],
                current_debt=0.0
            )
                print("Customer Data : ", row)
            except Exception as e:
                print("Customer Insertion Error : ROW - ", e)
    
        loan_file_path = 'data/loan_data.xlsx'  # Update with the actual path to your loan_data.xlsx file
        df = pd.read_excel(loan_file_path)

        for _, row in df.iterrows():
            
            try:
                Loan.objects.update_or_create(
                    customer_id=row['Customer ID'],
                    loan_id=row['Loan ID'],
                    loan_amount=row['Loan Amount'],
                    tenure=row['Tenure'],
                    interest_rate=row['Interest Rate'],
                    monthly_repayment=row['Monthly payment'],
                    emis_paid_on_time=row['EMIs paid on Time'],
                    start_date=row['Date of Approval'],
                    end_date=row['End Date'],
                )
            
                print("Loan Data : ", row)
            except Exception as e:
                print("Loan Insertion Error : ROW - ", e)
        
        
        self.stdout.write(self.style.SUCCESS('Loan data ingested successfully.'))
