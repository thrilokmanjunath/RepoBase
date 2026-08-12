import pytest
from django.contrib.auth.models import User
from repos.models import Repository

@pytest.mark.django_db
def test_create_user():
    user = User.objects.create_user(username='testuser', password='password123')
    assert user.username == 'testuser'

@pytest.mark.django_db
def test_create_repository():
    user = User.objects.create_user(username='repo_owner', password='password123')
    repo = Repository.objects.create(owner=user, name='Test_Repo', description='A test repo', is_public=True)
    assert repo.name == 'Test_Repo'
    assert repo.owner == user

@pytest.mark.django_db
def test_api_list_repositories(client):
    user = User.objects.create_user(username='apiuser', password='password123')
    Repository.objects.create(owner=user, name='Public_Repo', is_public=True)
    Repository.objects.create(owner=user, name='Private_Repo', is_public=False)
    
    response = client.get('/api/repos')
    assert response.status_code == 200
    res_data = response.json()
    items = res_data['data']['items']
    assert len(items) == 1
    assert items[0]['name'] == 'Public_Repo'

@pytest.mark.django_db
def test_api_update_and_delete_repository(client):
    user = User.objects.create_user(username='apiuser2', password='password123')
    client.force_login(user)
    
    # Create repo
    repo = Repository.objects.create(owner=user, name='Initial_Name')
    
    # Update via PUT
    response = client.put(
        f'/api/repos/{repo.id}',
        data={'name': 'Updated_Name', 'is_public': True, 'tag_names': ['newtag']},
        content_type='application/json'
    )
    assert response.status_code == 200
    assert response.json()['data']['name'] == 'Updated_Name'
    
    # Delete via DELETE
    del_response = client.delete(f'/api/repos/{repo.id}')
    assert del_response.status_code == 200
    assert Repository.objects.filter(id=repo.id).count() == 0
