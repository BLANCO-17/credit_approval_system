# Generated by Django 4.2.9 on 2024-02-07 08:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('customer_id', models.IntegerField(primary_key=True, serialize=False, unique=True)),
                ('first_name', models.CharField(max_length=100)),
                ('last_name', models.CharField(max_length=100)),
                ('phone_number', models.CharField(max_length=15)),
                ('monthly_salary', models.DecimalField(decimal_places=2, max_digits=10)),
                ('approved_limit', models.DecimalField(decimal_places=2, max_digits=10)),
                ('current_debt', models.DecimalField(decimal_places=2, max_digits=10)),
                ('age', models.IntegerField(default=18)),
            ],
        ),
        migrations.CreateModel(
            name='Loan',
            fields=[
                ('loan_id', models.IntegerField(primary_key=True, serialize=False, unique=True)),
                ('loan_amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('tenure', models.IntegerField()),
                ('interest_rate', models.DecimalField(decimal_places=2, max_digits=5)),
                ('monthly_repayment', models.DecimalField(decimal_places=2, max_digits=10)),
                ('emis_paid_on_time', models.IntegerField()),
                ('start_date', models.DateField()),
                ('end_date', models.DateField()),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='credit_approval.customer')),
            ],
        ),
    ]