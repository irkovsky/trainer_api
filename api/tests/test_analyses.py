import pytest
from api.models import Analysis

@pytest.mark.django_db
def test_create_analysis(client_api, client_user):
    response = client_api.post('/api/analyses/', {
        'date': '2026-09-30',
        'title': 'Общий анализ крови',
        'data': {'hemoglobin': 140}
    }, format='json')
    
    assert response.status_code == 201
    assert Analysis.objects.filter(user=client_user).count() == 1


@pytest.mark.django_db
def test_list_own_analyses(client_api, client_user):
    Analysis.objects.create(
        user=client_user,
        date='2026-09-30',
        title='Свой',
        data={}
    )
    
    response = client_api.get('/api/analyses/')
    assert response.status_code == 200
    assert response.data['count'] == 1


@pytest.mark.django_db
def test_get_one_analysis(client_api, client_user):
    analysis = Analysis.objects.create(
        user=client_user,
        date='2026-10-01',
        title='Свой',
        data={}
    )
    response = client_api.get(f'/api/analyses/{analysis.id}/')
    
    assert response.status_code == 200
    assert response.data['title'] == 'Свой'


def test_update_own_analysis(client_api, client_user):
    analysis = Analysis.objects.create(
        user=client_user,
        date='2026-10-01',
        title='Свой',
        data={}
    )
    response = client_api.patch(f'/api/analyses/{analysis.id}/', {
        'title': 'Новый'
    })
    
    assert response.status_code == 200
    analysis.refresh_from_db()
    assert analysis.title == 'Новый'
    

@pytest.mark.django_db
def test_delete_own_analysis(client_api, client_user):
    analysis = Analysis.objects.create(
        user=client_user,
        date='2026-10-01',
        title='Свой',
        data={}   
    )
    
    response = client_api.delete(f'/api/analyses/{analysis.id}/')
    
    assert response.status_code == 204
    assert not Analysis.objects.filter(id=analysis.id).exists()


@pytest.mark.django_db
def test_anonymous_cannot_create(api_client):
    response = api_client.post('/api/analyses/', {
        'date': '2026-10-01',
        'title': 'test',
        'data': {}        
    }, format='json')
    
    assert response.status_code == 401