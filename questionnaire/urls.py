from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('questions/<int:user_id>/', views.questions, name='questions'),
    path('selected_questions/<int:user_id>/', views.selected_questions, name='selected_questions'),
    path('results/<int:user_id>/', views.results, name='results'),
]