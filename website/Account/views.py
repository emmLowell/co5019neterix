from django.shortcuts import render

def login(request):
    return render(request, 'account/login.html', {'title': 'Login'})


def signup(request):
    return render(request, 'account/signup.html', {'title': 'Signup'})


def recover2(request):
    return render(request, 'account/forgotton-password.html', {'title': 'Recover2'})


def recover3(request):
    return render(request, 'account/forgotton-password-number.html', {'title': 'Recover3'})


def recover(request):
    return render(request, 'account/create-new-password.html', {'title': 'Recover'})
