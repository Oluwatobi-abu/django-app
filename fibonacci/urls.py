from django.urls import path
from . import views

app_name = 'fibonacci'

urlpatterns = [
    path('', views.fibonacci_view, name='index'),
    path('api/', views.fibonacci_api, name='api'),
]
