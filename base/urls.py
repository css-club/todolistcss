from django.urls import path 
from django.contrib.auth.views import LogoutView
from . import views

urlpatterns = [
    path('', views.task_list, name='task'),
    path('login/', views.login_view, name='login'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
    path('register/', views.register, name='register'),   
    path('task/<int:pk>/', views.task_detail, name='detail'),
    path('create-view', views.task_create, name='create-view'),
    path('task-update/<int:pk>/', views.task_update, name='task-update'),
    path('task-delete/<int:pk>/', views.task_delete, name='task-delete')
]
