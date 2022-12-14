# Generated by Django 3.2.15 on 2022-09-12 20:26

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Budget',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('creation_date', models.DateTimeField(auto_now_add=True, verbose_name='creation date')),
                ('last_update', models.DateTimeField(auto_now=True, verbose_name='last update')),
            ],
        ),
        migrations.CreateModel(
            name='IncomeTransaction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category', models.CharField(choices=[('Other', 'Other'), ('Salary', 'Salary'), ('Gift', 'Gift'), ('Payback', 'Payback')], default='Other', max_length=20)),
                ('amount', models.FloatField()),
                ('creation_date', models.DateTimeField(auto_now_add=True, verbose_name='creation date')),
                ('budget', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='income', to='family_budget.budget')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Family',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('creation_date', models.DateTimeField(auto_now_add=True, verbose_name='creation date')),
                ('users', models.ManyToManyField(blank=True, related_name='users', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='ExpenseTransaction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category', models.CharField(choices=[('Other', 'Other'), ('Food', 'Food'), ('Housing', 'Housing'), ('Transportation', 'Transportation'), ('Utilities', 'Utilities'), ('Heathcare', 'Healthcare'), ('Child', 'Child'), ('Personal', 'Personal'), ('Entertainment', 'Entertainment'), ('Holidays', 'Holidays'), ('Gifts', 'Gifts'), ('Savings', 'Savings')], default='Other', max_length=20)),
                ('amount', models.FloatField()),
                ('creation_date', models.DateTimeField(auto_now_add=True, verbose_name='creation date')),
                ('budget', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='expense', to='family_budget.budget')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='BudgetShare',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('budget', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='family_budget.budget')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='budget',
            name='family',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='family', to='family_budget.family'),
        ),
        migrations.AddField(
            model_name='budget',
            name='owner',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
