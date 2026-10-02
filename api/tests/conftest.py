import pytest
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model

User = get_user_model()

@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def client_user(db):
    return User.objects.create_user(
        username='client1',
        password='client12345',
        role='client'
    )
    

@pytest.fixture   
def admin_user(db):
    return User.objects.create_user(
        username='admin1',
        password='admin12345',
        role='admin'
    )
   

@pytest.fixture   
def client_api(api_client, client_user):
    api_client.force_authenticate(user=client_user)
    return api_client


@pytest.fixture
def admin_api(api_client, admin_user):
    api_client.force_authenticate(user=admin_user)
    return api_client