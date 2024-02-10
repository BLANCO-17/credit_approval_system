"""
URL configuration for credit_approval_system project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from credit_approval.views import RegistrationView, EligibilityView, CreateLoanView, view_loan, view_loans_for_customer


urlpatterns = [    
    path('admin/', admin.site.urls),
    # path('trigger-ingestion/', trigger_data_ingestion, name='trigger_data_ingestion'),
    path('register/', RegistrationView.as_view(), name='register'),
    path('check-eligibility/', EligibilityView.as_view(), name='eligilibility'),
    path('create-loan/', CreateLoanView.as_view(), name='create_loan'),
    path('view-loan/<int:loan_id>/', view_loan, name='loanview'), 
    path('view-loans/<int:customer_id>/', view_loans_for_customer, name='customerloanview'), 
    
]
