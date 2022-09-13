import pytest
from django.urls import reverse

@pytest.mark.django_db
@pytest.mark.parametrize(
    'username, email, password, status_code', [
        (123, 123, 123, 400),
        ('username', 'userexample.com', 'invalid_pass', 400),
        ('username', 'userexample.com', 123, 400),
        ("miki", 'user@example.com', 'strong_pass', 201),
    ]
)
def test_login_data_validation(username, email, password, status_code, client):
    url = reverse('user_create')
    data = {
        'username': username,
        'email': email,
        'password': password
    }

    response = client.post(url, data=data)
    assert response.status_code == status_code

# @pytest.mark.django_db
# @pytest.mark.parametrize(
#     'username, password', [
#         ('miki', 'strong_pass')
#     ]
# )
# def test_login(username, password, client):
#     # response = client.login(username=username, password=password)
#     # print(response)
#     data = {"username": username, "password": password}
#     response = client.post('/api-auth/', data=json.dumps(data), content_type='application/json')
#     assert response.status_code == 200

from rest_framework.test import APIClient
@pytest.mark.django_db
@pytest.mark.parametrize(
    'name, status_code', [
        (123, 200),
        (123, 400),
        ('test_name', 200),
        (["miki"], 400),
    ]
)
def test_family_create_validation(name, status_code, client):
    url = reverse('family_create')
    data = {
        'name': name
    }
    clients = APIClient()
    clients.login(username='miki', password='strong_pass')
    response = client.post(url, data=data)
    print(response.json)
    assert response.status_code == status_code

