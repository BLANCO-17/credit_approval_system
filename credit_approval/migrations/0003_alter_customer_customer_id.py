# Generated by Django 4.2.9 on 2024-02-07 08:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('credit_approval', '0002_alter_customer_approved_limit_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='customer_id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
    ]
