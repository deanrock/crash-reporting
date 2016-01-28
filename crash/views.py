from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout as logout_user
from django.core.urlresolvers import reverse


def login(request):
    return HttpResponseRedirect(reverse('simple-sso-login'))


@login_required
def logout(request):
    logout_user(request)
    return HttpResponseRedirect('/')
