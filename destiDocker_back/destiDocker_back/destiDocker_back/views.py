from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views import generic
from django.contrib.auth import views as auth_views
from django.contrib.auth.signals import user_logged_in


class RegisterView(generic.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'register.html'

    def form_valid(self, form):
        response = super().form_valid(form)
        return response


class CustomLoginView(auth_views.LoginView):
    def form_valid(self, form):
        response = super().form_valid(form)
        user_logged_in.send(sender=self.__class__,
                            request=self.request, user=self.request.user)
        return response
