from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('fibonacci/', include('fibonacci.urls')),
    path('', include('todo.urls')),
]
