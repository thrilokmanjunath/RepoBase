from django.urls import path
from . import views
from .api import api

urlpatterns =[
    path('signup/',views.signup_view,name='signup'),
    path('login/',views.login_view,name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('',views.home_view,name='home'),
    path('repo/<int:repo_id>/', views.repo_detail_view, name='repo_detail'),
    path('api/', api.urls),
]