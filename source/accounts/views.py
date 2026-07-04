from django.contrib.auth import login, get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView

from accounts.forms import RegisterForm
from accounts.models import Profile


class UserLoginView(LoginView):
    template_name = 'accounts/login.html'
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('threads:index')


class UserLogoutView(LogoutView):
    next_page = 'index'


class RegisterView(CreateView):
    model = get_user_model()
    template_name = 'accounts/register.html'
    form_class = RegisterForm

    def post(self, request, *args, **kwargs):
        self.object = None
        form = self.get_form()
        if form.is_valid():
            user = form.save()
            Profile.objects.create(
                user=user,
                avatar=form.cleaned_data['avatar'],
            )
            login(request, user)
            return redirect('threads:index')
        return self.render_to_response(self.get_context_data(form=form))


class UserDetailView(LoginRequiredMixin, DetailView):
    model = get_user_model()
    template_name = 'accounts/profile.html'
    context_object_name = 'profile_user'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['threads'] = self.get_object().threads.order_by('-created_at')
        return context