import util

from forms import *
from django.template import RequestContext, loader
from django.http import HttpResponse, HttpResponseRedirect
from . import forms
from django.core.urlresolvers import reverse

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth import models as _models
from django.contrib.auth.decorators import login_required
from django.contrib import messages

''' Renders login form
'''
def render_login_form(request):
    template = loader.get_template('templates/login.html')
    context = RequestContext(request, {"form": LoginForm()})

    return HttpResponse(template.render(context))

''' Renders registration page and form
'''
def render_register_form(request):

    template = loader.get_template('templates/reg.html')
    context = RequestContext(request, {"form": RegistrationForm()})

    return HttpResponse(template.render(context))

''' Processes login form. Redirects to home page if login is successful,
    otherwise, returns to login page and displays error information
'''
def process_login(request):
    form = forms.LoginForm(request.POST)

    if form.is_valid():
        user = authenticate(username=request.POST['login'], password=request.POST["password"])

        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse('auth:home'))
        else:
            response = HttpResponseRedirect(reverse('auth:login'))
            messages.add_message(request, messages.INFO, 'Current user is not registred yet')

            return response
    else:
        messages.add_message(request, messages.INFO, 'Fill required fields')

        response = HttpResponseRedirect(reverse('auth:login'))
        return response

''' Processes registration form. Redirects to login page if registration is successful,
    otherwise, returns to registration page and displays error information
'''
def process_registration(request):
    form = forms.RegistrationForm(request.POST)

    login = request.POST.get('login')
    if form.is_valid():
        passwd = request.POST.get('password')

        user = _models.User.objects.create_user(username=login, password=passwd)

        return HttpResponseRedirect(reverse('auth:login'))
    else:
        messages.add_message(request, messages.INFO, 'User with login "{}" already exists.'.format(login))

        response = HttpResponseRedirect(reverse('auth:register'))
        return response

''' Provides logout for user
'''
def process_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('auth:login'))

''' Renders home page
'''
@login_required
def render_home(request):
    if not request.session.get('credentials', False):
        uri = util.refresh_credentials()
        return HttpResponseRedirect(uri)

    template = loader.get_template('templates/home.html')
    context = RequestContext(request, {"username": request.user.username})

    return HttpResponse(template.render(context))


''' Handle OAuth2 authorization
'''
def oauth_autorization(request):
    http_auth = util.authorize(request.GET['code'])
    request.session['credentials'] = http_auth.to_json()

    return HttpResponseRedirect(reverse('auth:home'))

''' Handles root path ('/') redirect
'''
def handle_all(request):
    return HttpResponseRedirect(reverse('auth:home'))