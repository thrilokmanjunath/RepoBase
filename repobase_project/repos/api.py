import logging
from typing import List, Optional, Generic, TypeVar
from django.shortcuts import get_object_or_404
from django.http import Http404
from django.db.models import Q
from ninja import NinjaAPI, Schema, Field
from ninja.pagination import paginate, PageNumberPagination
from django.core.cache import cache
from .models import Repository, Tag

logger = logging.getLogger(__name__)

def check_rate_limit(request, action: str, limit: int = 10, timeout: int = 60) -> bool:
    ip = request.META.get('HTTP_X_FORWARDED_FOR', request.META.get('REMOTE_ADDR', 'unknown'))
    if ',' in ip:
        ip = ip.split(',')[0].strip()
    key = f"rl_{action}_{ip}"
    count = cache.get(key, 0)
    if count >= limit:
        return False
    cache.set(key, count + 1, timeout)
    return True

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

T = TypeVar('T')
class ApiResponse(Schema, Generic[T]):
    success: bool = True
    data: T

class RepositoryCreateSchema(Schema):
    name: str = Field(..., max_length=100, pattern=r'^[a-zA-Z0-9_.-]+$')
    description: str = Field("", max_length=500)
    url: str = Field("", max_length=200)
    is_public: bool = True
    tag_names: List[str] = Field(default_factory=list, max_length=10)

class PaginatedRepositorySchema(Schema):
    items: List[RepositorySchema]
    total: int
    page: int
    size: int
    pages: int

@api.get("/repos", response=ApiResponse[PaginatedRepositorySchema])
def list_repositories(request, search: str = None, page: int = 1, size: int = 20):
    qs = Repository.objects.select_related('owner').prefetch_related('tags').all()
    
    if not request.user.is_authenticated:
        qs = qs.filter(is_public=True)
    else:
        qs = qs.filter(Q(is_public=True) | Q(owner=request.user))
        
    if search:
        qs = qs.filter(name__icontains=search)
    
    total = qs.count()
    
    import math
    pages = math.ceil(total / size) if size > 0 else 0
    if page < 1:
        page = 1
        
    offset = (page - 1) * size
    items = list(qs[offset:offset + size])
    
    paginated_data = {
        "items": items,
        "total": total,
        "page": page,
        "size": size,
        "pages": pages
    }
    
    return {"success": True, "data": paginated_data}

@api.get("/repos/{repo_id}", response=ApiResponse[RepositorySchema])
def get_repository(request, repo_id: int):
    repo = get_object_or_404(Repository, id=repo_id)
    if not repo.is_public:
        if not request.user.is_authenticated or repo.owner != request.user:
            logger.warning(f"Unauthorized access attempt to repo {repo_id} by {request.user}")
            raise Http404("No Repository matches the given query.")
    
    repo.views_count += 1
    repo.save(update_fields=['views_count'])
    return {"success": True, "data": repo}

@api.post("/repos", response=ApiResponse[RepositorySchema])
def create_repository(request, payload: RepositoryCreateSchema):
    if not request.user.is_authenticated:
        return api.create_response(request, {"success": False, "error": {"code": "unauthorized", "message": "Authentication required"}}, status=401)
    
    if not check_rate_limit(request, 'create_repo', limit=10, timeout=60):
        return api.create_response(request, {"success": False, "error": {"code": "rate_limited", "message": "Too many requests. Please try again later."}}, status=429)
    
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
        
    logger.info(f"User {request.user.id} created repository {repo.id}")
    return {"success": True, "data": repo}

@api.put("/repos/{repo_id}", response=ApiResponse[RepositorySchema])
def update_repository(request, repo_id: int, payload: RepositoryCreateSchema):
    if not request.user.is_authenticated:
        return api.create_response(request, {"success": False, "error": {"code": "unauthorized", "message": "Authentication required"}}, status=401)
        
    if not check_rate_limit(request, 'update_repo', limit=20, timeout=60):
        return api.create_response(request, {"success": False, "error": {"code": "rate_limited", "message": "Too many requests. Please try again later."}}, status=429)
        
    repo = get_object_or_404(Repository, id=repo_id, owner=request.user)
    
    repo.name = payload.name
    repo.description = payload.description
    repo.url = payload.url
    repo.is_public = payload.is_public
    repo.save()
    
    repo.tags.clear()
    for tag_name in payload.tag_names:
        tag, _ = Tag.objects.get_or_create(name=tag_name)
        repo.tags.add(tag)
        
    logger.info(f"User {request.user.id} updated repository {repo.id}")
    return {"success": True, "data": repo}

@api.delete("/repos/{repo_id}")
def delete_repository(request, repo_id: int):
    if not request.user.is_authenticated:
        return api.create_response(request, {"success": False, "error": {"code": "unauthorized", "message": "Authentication required"}}, status=401)
        
    if not check_rate_limit(request, 'delete_repo', limit=10, timeout=60):
        return api.create_response(request, {"success": False, "error": {"code": "rate_limited", "message": "Too many requests. Please try again later."}}, status=429)
        
    repo = get_object_or_404(Repository, id=repo_id, owner=request.user)
    repo_id_deleted = repo.id
    repo.delete()
    logger.info(f"User {request.user.id} deleted repository {repo_id_deleted}")
    return {"success": True, "data": None}
