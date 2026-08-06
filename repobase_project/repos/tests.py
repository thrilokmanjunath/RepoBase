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
    repo = Repository.objects.create(owner=user, name='Test Repo', description='A test repo', is_public=True)
    assert repo.name == 'Test Repo'
    assert repo.owner == user

@pytest.mark.django_db
def test_api_list_repositories(client):
    user = User.objects.create_user(username='apiuser', password='password123')
    Repository.objects.create(owner=user, name='Public Repo', is_public=True)
    Repository.objects.create(owner=user, name='Private Repo', is_public=False)
    
    response = client.get('/api/repos')
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]['name'] == 'Public Repo'
