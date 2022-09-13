import pytest
from django.urls import reverse
from rest_framework.authtoken.admin import User
from rest_framework.test import APIClient
import json
from family_budget.models import Budget, Family


class Tests:
    @pytest.fixture
    def context(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username="miki", password="password", is_staff=True, is_superuser=True)
        # self.user = self.client.login(username='miki', password='strong_pass', is_staff=True, is_superuser=True)
        self.family = Family.objects.create(name="test_family")
        self.budget = Budget.objects.create(name="test_budget", owner="admin", family=self.family)

    @pytest.mark.django_db
    @pytest.mark.parametrize(
        'username, email, password, status_code', [
            (123, 123, 123, 400),
            ('username', 'userexample.com', 'invalid_pass', 400),
            ('username', 'userexample.com', 123, 400),
            ("miki", 'user@example.com', 'strong_pass', 201),
        ]
    )
    def test_login_data_validation(self, username, email, password, status_code, client):
        url = reverse('user_create')
        data = {
            'username': username,
            'email': email,
            'password': password
        }

        response = client.post(url, data=data)
        assert response.status_code == status_code

    @pytest.mark.django_db
    @pytest.mark.parametrize(
        'name, status_code', [
            (123, 400),
            ('"123"', 201),
            ('"test_name"', 201),
            ('["miki"]', 400),
        ]
    )
    def test_family_create_validation(self, name, status_code, admin_client, context):
        url = reverse('family_create')
        data = {
            "name": name
        }
        clients = APIClient()
        clients.login(username='miki', password='strong_pass', is_staff=True, is_superuser=True)
        response = admin_client.post(url, data=data)
        assert response.status_code == status_code

    @pytest.mark.django_db
    @pytest.mark.parametrize(
        'name, status_code', [
            (123, 201),
            ('"123"', 201),
            ('"test_name"', 201),
            ('["miki"]', 400),
        ]
    )
    def test_budget_create_validation(self, name, status_code, admin_client, context):
        url = reverse('budget_create')
        data = {
            "name": name,
            "owner": "miki",
            "family": self.family.id
        }
        clients = APIClient()
        clients.login(username='miki', password='strong_pass', is_staff=True, is_superuser=True)
        response = admin_client.post(url, data=data)
        assert response.status_code == status_code

    @pytest.mark.django_db
    def test_family_get_validation(self, admin_client, context):
        url = reverse('family_details', kwargs={'pk': self.family.id})
        clients = APIClient()
        clients.login(username='miki', password='strong_pass', is_staff=True, is_superuser=True)
        response = admin_client.get(url)
        print(response.data)
        assert response.status_code == 200

    @pytest.mark.django_db
    def test_budget_get_validation(self, admin_client, context):
        url = reverse('budget_details', kwargs={'pk': self.budget.id})
        clients = APIClient()
        clients.login(username='miki', password='strong_pass', is_staff=True, is_superuser=True)
        response = admin_client.get(url)
        print(response.data)
        assert response.status_code == 200

    @pytest.mark.django_db
    @pytest.mark.parametrize(
        'category, amount, status_code', [
            ("Other", 1000, 201),
            ("Salary", ["pop"], 400),
            ("Gifty", "none", 400),
            (123, 100, 400),
        ]
    )
    def test_income_create_validation(self, category, amount, status_code, context, admin_client):
        url = reverse('income_create')
        data = {
            "budget": self.budget.id,
            "category": category,
            "amount": amount,
            "user": self.user.id

        }
        clients = APIClient()
        clients.login(username='miki', password='strong_pass', is_staff=True, is_superuser=True)
        response = admin_client.post(url, data=data)
        print(response.data)
        assert response.status_code == status_code

    @pytest.mark.django_db
    @pytest.mark.parametrize(
        'category, amount, status_code', [
            ("Transportation", 1000, 201),
            ("Salary", ["pop"], 400),
            ("Gifty", "none", 400),
            (123, 100, 400),
        ]
    )
    def test_expense_create_validation(self, category, amount, status_code, context, admin_client):
        url = reverse('expense_create')
        data = {
            "budget": self.budget.id,
            "category": category,
            "amount": amount,
            "user": self.user.id

        }
        clients = APIClient()
        clients.login(username='miki', password='strong_pass', is_staff=True, is_superuser=True)
        response = admin_client.post(url, data=data)
        print(response.data)
        assert response.status_code == status_code

    @pytest.mark.django_db
    def test_clean_up(self, context, admin_client):
        budget_delete = reverse('budget_details', kwargs={'pk': self.budget.id})
        family_delete = reverse('family_details', kwargs={'pk': self.family.id})
        clients = APIClient()
        clients.login(username='miki', password='strong_pass', is_staff=True, is_superuser=True)
        user = User.objects.get(id=self.user.id)
        user.delete()
        budget_response = admin_client.delete(budget_delete)
        family_response = admin_client.delete(family_delete)
        print(budget_response.data)
        print(family_response.data)
        assert budget_response.status_code == 204
        assert family_response.status_code == 204
