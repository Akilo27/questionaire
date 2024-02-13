from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('mini_admin/', views.mini_admin, name='home'),
    path('users/<int:user_id>/', views.user_detail, name='user_detail'),
    path('questions/<int:user_id>/', views.questions, name='questions'),
    path('selected_questions/<int:user_id>/', views.selected_questions, name='selected_questions'),
    path('results/<int:user_id>/', views.results, name='results'),
]