# Generated by Django 3.2.15 on 2022-09-12 21:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('family_budget', '0004_alter_budget_users'),
    ]

    operations = [
        migrations.DeleteModel(
            name='BudgetShare',
        ),
    ]