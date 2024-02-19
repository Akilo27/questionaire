from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.login, name='login'),
    path('local_admin/', views.mini_admin, name='mini_admin'),
    path('users/<int:user_id>/', views.user_detail, name='user_detail'),
    path('group/<int:group_id>/', views.group_detail, name='group_detail'),


    path('local_admin/competences/', views.competence_list, name='competence_list'),
    path('local_admin/competences/create/', views.competence_create, name='competence_create'),
    path('local_admin/competences/update/<int:pk>/', views.competence_update, name='competence_update'),
    path('local_admin/competences/delete/<int:pk>/', views.competence_delete, name='competence_delete'),


    path('local_admin/groups/', views.group_list, name='group_list'),
    path('local_admin/groups/create/', views.group_create, name='group_create'),
    path('local_admin/groups/update/<int:pk>/', views.group_update, name='group_update'),
    path('local_admin/groups/delete/<int:pk>/', views.group_delete, name='group_delete'),

    path('local_admin/question_update/<int:pk>/', views.Block_update, name='block_update'),

    path('local_admin/questions/', views.question_list, name='question_list'),
    path('local_admin/question/create/', views.question_create, name='question_create'),
    path('local_admin/question/update/<int:pk>/', views.question_update, name='question_update'),
    path('local_admin/question/delete/<int:pk>/', views.question_delete, name='question_delete'),

    path('questions/<int:user_id>/', views.questions, name='questions'),
    path('selected_questions/<int:user_id>/', views.selected_questions, name='selected_questions'),
    path('results/<int:user_id>/', views.results, name='results'),
]