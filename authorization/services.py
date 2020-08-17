from django.contrib.auth import authenticate, login, logout


def authenticate_and_login_user(request):
    user = _authenticate(request)
    if user:
        _login(request, user)
        return True, {}
    else:
        return False, {'login_error': 'Неверно введен логин или пароль'}


def _authenticate(request):
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(request, username=username, password=password)
    if user:
        return user
    else:
        return None


def _login(request, user):
    login(request, user)