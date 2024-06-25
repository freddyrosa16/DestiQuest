from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views import generic


class RegisterView(generic.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'register.html'

    def get(self, request, *args, **kwargs):
        print("RegisterView GET request")
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        print("RegisterView POST request")
        return super().post(request, *args, **kwargs)
