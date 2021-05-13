from django.urls import reverse_lazy
from django.views import generic
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.models import User, Group
from django.contrib.auth import authenticate, login
from django.shortcuts import HttpResponse, get_object_or_404, render, HttpResponseRedirect
import json
from accounts import subscribe
from accounts.models import CustomUser
from accounts.forms import *
from django.contrib.auth.decorators import login_required


class SignUpView(generic.CreateView):
    model = CustomUser()
    template_name = 'accounts/signup.html'
    form_class = RegisterUserForm
    success_url = reverse_lazy('start_page')

    def form_valid(self, form):
        form_valid = super().form_valid(form)
        email = form.cleaned_data['email']
        password = form.cleaned_data['password']
        aut_user = authenticate(email=email, password=password)
        aut_user.groups.add(Group.objects.get(name='User'))
        login(self.request, aut_user)
        return form_valid


class LoginView(LoginView):
    model = User
    template_name = 'accounts/login.html'
    form_class = AuthUserForm
    success_url = reverse_lazy('start_page')

    def form_valid(self, form):
        """Security check complete. Log the user in."""
        auth = super().form_valid(form)
        x_forwarded_for = self.request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[-1].strip()
        else:
            ip = self.request.META.get('REMOTE_ADDR')
        ssid = self.request.session.session_key
        uid = self.request.user.id
        subscribe.subscribe_authorization(uid, ssid, ip)
        return HttpResponseRedirect(self.get_success_url())


class UserLogoutView(LogoutView):
    next_page = reverse_lazy('start_page')


def is_user_exist(request):
    if request.method == 'POST':
        data = request.POST
        is_user = CustomUser.is_user_email(data['mail'])
        data_response = {'result': is_user}
        return HttpResponse(json.dumps(data_response), content_type='application/json')


def user_page(request):
    context = {}
    return render(request, 'user-page.html', context)


def mailing_promotions(request):
    template = 'accounts/promotions.html'
    if request.method == 'POST':
        data = request.POST
        msg_promotions = data.get('text_promotions')
        subscribe.subscribe_promo(msg_promotions)
        return HttpResponseRedirect(request.path_info)
    return render(request, template)


@login_required(login_url='main_page')
def subscribes(request):
    template = 'accounts/subscribe.html'
    context = {}
    subs, _ = Subscribe.objects.get_or_create(user=request.user)
    form = SubscribeForm(instance=subs)
    context['form'] = form
    if request.method == 'POST':
        form = SubscribeForm(request.POST, instance=subs)
        if form.is_valid():
            form = form.save(commit=False)
            form.user = request.user
            form.save()
            return HttpResponseRedirect(request.path_info)
    return render(request, template, context)


def wishlist(request):
    return render(request, 'wishlist-page.html')


def mail_sub(request):
    if request.POST:
        user = request.user
        if user.subscription_email:
            user.subscription_email = False
        else:
            user.subscription_email = True
        user.save()
        data_response = {'sub': user.subscription_email}

        return HttpResponse(json.dumps(data_response), content_type='application/json')


def change_fullname(request):
    if request.POST:
        user = request.user
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        if not first_name == ' ' and not last_name == ' ':
            user.first_name = request.POST.get('first_name')
            user.last_name = request.POST.get('last_name')
            user.save()
            data_response = {'success': True}
        else:
            data_response = {'success': False}

        return HttpResponse(json.dumps(data_response), content_type='application/json')
