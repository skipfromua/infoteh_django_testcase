from .validators import custom_validate_email, custom_validate_password, custom_validate_username, \
    custom_validate_for_empty_spaces

from django.contrib.auth.models import User, Permission
from django.contrib.contenttypes.models import ContentType

from message_publisher.models import Message


def registrate_new_user_and_give_permissions(request):
    new_user = Registration()
    context = new_user.registration_validation(request)
    new_user.registrate(request)
    if new_user.done:
        new_user.give_premissions(User.objects.get_by_natural_key(request.POST.get('username')))
        return True, context
    else:
        return False, context


class Registration():
    passed = True
    done = False

    def registration_validation(self, request):
        context = {}
        if request.method == 'POST':
            if custom_validate_username(request.POST.get('username')):
                context.update({'username_error': 'Пользователь с таким именем уже зарегистрирован'})
                self.passed = False
            elif not custom_validate_for_empty_spaces(request.POST.get('username')):
                context.update({'username_error': 'Нельзя оставлять поле для ввода пустым'})
                self.passed = False
            else:
                context.update({'valid_username': request.POST.get('username') })
            error = custom_validate_email(request.POST.get('email'))
            if error:
                context.update({'email_error': error})
                self.passed = False
            else:
                context.update({'valid_email': request.POST.get('email')})
            error = custom_validate_password(request.POST.get('password'))
            if error:
                context.update({'password_error': error})
                self.passed = False
            else:
                context.update({'valid_password': request.POST.get('password')})
        return context

    def registrate(self, request):
        if self.passed:
            user = User.objects.create_user(username=request.POST.get('username'),
                                            email=request.POST.get('email'),
                                            password=request.POST.get('password'))
            user.save()

            self.done = True

    def give_premissions(self, user):
        content_type = ContentType.objects.get_for_model(Message)
        premission = Permission.objects.get(codename='add_message', content_type=content_type)
        user.user_permissions.add(premission)