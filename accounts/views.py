from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse

from .forms import UserRegistrationForm
from accounts.models import UserProfile
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404



#def login_user(request):
#    if request.method == "POST":
#        username = request.POST.get('username')
#        password = request.POST.get('password')
#        user = authenticate(request, username=username, password=password)
#        if user is not None:
#            login(request, user)
#            return HttpResponseRedirect(reverse('questions_list_url'))
#        else:
#            messages.error(request, 'Bad username or password')
#    return render(request, 'accounts/login.html', {})


#def logout_user(request):
#    logout(request)
#    return redirect('accounts:login')


def user_registration(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            email = form.cleaned_data['email']
            avatar = request.FILES['avatar']
            user = User.objects.create_user(username, email=email, password=password)
            userprofile = UserProfile.objects.create(user=user, avatar=avatar)
            messages.success(request, 'Thanks for registering {}'.format(user.username))
            return redirect('accounts:login')
    else:
        form = UserRegistrationForm()
    return render(request, 'accounts/register.html', context={'form': form})


@login_required
def user_settings(request):
    user = get_object_or_404(User, pk=request.user.pk)
    try:
        userprofile = user.userprofile
    except:
        userprofile = None
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            email = form.cleaned_data['email']
            avatar = request.FILES['avatar']
            user.delete()
            if userprofile:
                userprofile.delete()
            user = User.objects.create_user(username, email=email, password=password)
            if avatar:
                userprofile = UserProfile.objects.create(user=user, avatar=avatar)
            messages.success(request, 'Successfully update {}'.format(user.username))
            return render(request, 'accounts/settings.html', context={'form': form, 'user': user})
    else:
        form = UserRegistrationForm()
        form.fields['username'].initial = user.username
        form.fields['email'].initial = user.email
    return render(request, 'accounts/settings.html', context={'form': form, 'user': user})

