
from django.urls import path
from .import views

urlpatterns =[
    path('dashboard/', views.dashboard, name='dashboard'),
    path('register/', views.dashboard, name='register'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),

    path('book/<int:pk>/', views.book_detail, name='book_detail'),
]