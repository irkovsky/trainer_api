import pytest
from api.models import Workout

@pytest.mark.django_db
def test_create_workout_admin(admin_api, client_user):
    response = admin_api.post('/api/workouts/', {
        'user': client_user.id,
        'date':  '2026-10-09',
        'title': 'Тренировка ног',
        'description': 'Приседания 3x10'
    }, format='json')
    
    assert response.status_code == 201
    assert Workout.objects.count() == 1
    
    
@pytest.mark.django_db
def test_create_workout_client_forbidden(client_api, client_user):
    response = client_api.post('/api/workouts/', {
        'user': client_user.id,
        'date':  '2026-10-09',
        'title': 'Попытка',
        'description': ''
    }, format='json')
    
    assert response.status_code == 403
    assert Workout.objects.count() == 0
    
@pytest.mark.django_db
def test_list_workouts_by_role(client_api, admin_api, client_user, admin_user):
    Workout.objects.create(user=client_user, title='Свой', date='2026-10-08')
    Workout.objects.create(user=admin_user, title='Чужой', date='2026-10-08')
    
    response = client_api.get('/api/workouts/')
    assert response.status_code == 200
    assert response.data['count'] == 1
    
    response = admin_api.get('/api/workouts/')
    assert response.status_code == 200
    assert response.data['count'] == 2
 
    
@pytest.mark.django_db
def test_get_others_workout_404(client_api, admin_user):
    workout = Workout.objects.create(user=admin_user, title='Чужая', date='2026-10-09')
    
    response = client_api.get(f'/api/workouts/{workout.id}/')
    
    assert response.status_code == 404
    
    
@pytest.mark.django_db
def test_anonymous_cannot_access_workouts(api_client):
    response = api_client.get('/api/workouts/')
    assert response.status_code == 401
    