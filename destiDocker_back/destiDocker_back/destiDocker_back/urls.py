from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
<<<<<<< HEAD
from .views import RegisterView
from django.conf import settings
from django.conf.urls.static import static
=======
from .views import RegisterView, CustomLoginView, IATACodeAutocomplete
>>>>>>> recovery-branch

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('register/', RegisterView.as_view(template_name='register.html'),
         name='register'),
    path('get-iata-codes/', IATACodeAutocomplete.as_view(), name='get_iata_codes'),
    path('', include('questions.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)