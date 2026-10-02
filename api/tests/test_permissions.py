import pytest
from api.models import Analysis


def test_admin_sees_all_analyses(admin_api, client_user):
    Analysis.objects.create(
        user=client_user,
        date='2026-10-01',
        title='',
        data={}
    )
    
    response = admin_api.get('/api/analyses/')
    assert response.status_code == 200
    assert response.data['count'] == 1


def test_client_does_not_see_others(client_api, admin_user):
    Analysis.objects.create(
        user=admin_user,
        date='2026-10-02',
        title='Чужой анализ',
        data={}
    )
    
    response = client_api.get('/api/analyses/')
    
    assert response.status_code == 200
    assert response.data['count'] == 0


def test_admin_can_delete_any(admin_api, client_user):
    analysis = Analysis.objects.create(
        user=client_user,
        date='2026-10-02',
        title='Чужой',
        data={}
    )
    
    response = admin_api.delete(f'/api/analyses/{analysis.id}/')
    assert response.status_code == 204
    assert not Analysis.objects.filter(id=analysis.id).exists()

def test_client_cannot_delete_others(client_api, admin_user):
    analysis = Analysis.objects.create(
            user=admin_user,
            date='2026-10-02',
            title='Чужой',
            data={}
        )
    response = client_api.delete(f'/api/analyses/{analysis.id}/')
    assert response.status_code == 404
    assert Analysis.objects.filter(id=analysis.id).exists()
    