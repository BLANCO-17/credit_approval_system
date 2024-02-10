# credit_approval/tasks.py

import pandas as pd
from celery import shared_task
from .models import Customer, Loan

# @shared_task
# def create_new_user(fname, lname, age, m_income, ph_no):
    

# @shared_task
# def ingest_data_from_excel(customer_file_path, loan_file_path):
#     try:
#         # print("brrrrrrrrrr")
#         # Read customer data from Excel file
#         # customer_df = pd.read_excel(customer_file_path)
#         # for _, row in customer_df.iterrows():
#         #     Customer.objects.create(
#         #         customer_id=row['Customer ID'],
#         #         first_name=row['First Name'],
#         #         last_name=row['Last Name'],
#         #         phone_number=row['Phone Number'],
#         #         monthly_salary=row['Monthly Salary'],
#         #         approved_limit=row['Approved Limit'],
#         #         current_debt=0.0
#         #     )
#         # print(customer_df)
#         # # Read loan data from Excel file
#         # loan_df = pd.read_excel(loan_file_path)
#         # for _, row in loan_df.iterrows():
#         #     Loan.objects.create(
#         #         customer_id=row['Customer ID'],
#         #         loan_id=row['Loadn ID'],
#         #         loan_amount=row['Loan Amount'],
#         #         tenure=row['Tenure'],
#         #         interest_rate=row['Interest Rate'],
#         #         monthly_repayment=row['Monthly payment'],
#         #         emis_paid_on_time=row['EMIs paid on Time'],
#         #         start_date=row['Start Date'],
#         #         end_date=row['End Date'],
#         #     )
#         bruh = "someinput"
#         return bruh
            
            
#     except Exception as e:
#         # Handle any errors appropriately, such as logging
#         print(f"Error while ingesting data: {e}")

