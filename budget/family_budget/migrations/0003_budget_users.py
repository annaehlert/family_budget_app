# Generated by Django 3.2.15 on 2022-09-12 20:52

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('family_budget', '0002_alter_budget_owner'),
    ]

    operations = [
        migrations.AddField(
            model_name='budget',
            name='users',
            field=models.ManyToManyField(blank=True, related_name='usersk', to=settings.AUTH_USER_MODEL),
        ),
    ]