from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('todo/', views.todo_list, name='todo_list'),
    path('delete/<int:task_id>/', views.delete_task, name='delete_task'),
    path('password-hash-and-salt/', views.view_password_hash_and_salt, name='view_password_hash_and_salt'),
]
