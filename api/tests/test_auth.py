import pytest
from django.contrib.auth import get_user_model

User = get_user_model()

@pytest.mark.django_db
def test_register_user(api_client):
    response = api_client.post('/api/register/', {
        'username': 'newuser',
        'password': 'newpass12345',
        'role': 'client'
    })
    
    assert response.status_code == 201
    assert User.objects.filter(username='newuser').exists()
    

@pytest.mark.django_db    
def test_register_duplicate_username(api_client, client_user):
    response = api_client.post('/api/register/', {
        'username': 'client1',
        'password': 'client12345',
        'role': 'client'
    })
    
    assert response.status_code == 400
    

@pytest.mark.django_db    
def test_login_returns_token(api_client, client_user):
    response = api_client.post('/api/token/', {
        'username': 'client1',
        'password': 'client12345'
    })
    
    assert response.status_code == 200
    assert 'access' in response.data
    assert 'refresh' in response.data
    
    
@pytest.mark.django_db
def test_login_wrong_password(api_client, client_user):
    response = api_client.post('/api/token/', {
        'username': 'client1',
        'password': 'wrong'
    })
    
    assert response.status_code == 401

