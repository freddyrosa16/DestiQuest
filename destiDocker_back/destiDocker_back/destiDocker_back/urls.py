from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from .views import RegisterView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('register/', RegisterView.as_view(template_name='register.html'),
         name='register'),
    path('', include('questions.urls')),
]
