from typing import List
from django.shortcuts import get_object_or_404
from ninja import NinjaAPI, Schema
from .models import Repository, Tag

api = NinjaAPI(title="RepoBase API", description="High-performance API for RepoBase")

class TagSchema(Schema):
    id: int
    name: str

class RepositorySchema(Schema):
    id: int
    name: str
    description: str
    url: str
    views_count: int
    is_public: bool
    owner_id: int
    tags: List[TagSchema]

class RepositoryCreateSchema(Schema):
    name: str
    description: str = ""
    url: str = ""
    is_public: bool = True
    tag_names: List[str] = []

@api.get("/repos", response=List[RepositorySchema])
def list_repositories(request, search: str = None):
    # Optimize query with select_related and prefetch_related
    qs = Repository.objects.select_related('owner').prefetch_related('tags').all()
    if not request.user.is_authenticated:
        qs = qs.filter(is_public=True)
    if search:
        qs = qs.filter(name__icontains=search)
    return qs

@api.get("/repos/{repo_id}", response=RepositorySchema)
def get_repository(request, repo_id: int):
    repo = get_object_or_404(Repository, id=repo_id)
    repo.views_count += 1
    repo.save(update_fields=['views_count'])
    return repo

@api.post("/repos", response=RepositorySchema)
def create_repository(request, payload: RepositoryCreateSchema):
    if not request.user.is_authenticated:
        return api.create_response(request, {"detail": "Authentication required"}, status=401)
    
    repo = Repository.objects.create(
        owner=request.user,
        name=payload.name,
        description=payload.description,
        url=payload.url,
        is_public=payload.is_public
    )
    
    for tag_name in payload.tag_names:
        tag, _ = Tag.objects.get_or_create(name=tag_name)
        repo.tags.add(tag)
        
    return repo
