from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect
from .forms import loginForm
from django.contrib.auth import authenticate, login, logout


# Create your views here.
def loginView(request):
    form = loginForm(request.POST or None)
    if form.is_valid():
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password")
        user = authenticate(username=username, password=password)
        login(request, user)
        return redirect('evaluations/quizstate') if user.is_staff else redirect('evaluations/quizselector')
    if request.user.is_authenticated:
        return redirect('evaluations/quizstate') if request.user.is_staff else redirect('evaluations/quizselector')
    context = {'form': form,}
    return render(request, 'core/login.html', context)


def logoutView(request):
    logout(request)
    return redirect('/')