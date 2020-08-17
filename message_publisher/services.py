from django.utils import timezone
from django.contrib.auth import get_user
from django.core.files.storage import FileSystemStorage
from django.shortcuts import render, redirect

from .models import Message
from .validators import text_validator


def main_page_content(request):
    if request.GET:
        messages = _filtered_messages(request)
    else:
        messages = _unfiltered_messages()

    context = {
        'Messages': messages,
        'User': get_user(request)
    }
    return render(request, 'message_publisher/published_messages.html', context)


def create_message_context_to_publish(request):
    context = _to_form_context(request)
    if request.method == 'POST':
        if not text_validator(request.POST['message_body']):
            context.update({'Error_message': 'Поле для ввода сообщения не должно быть пустым'})
            return render(request, 'message_publisher/create_and_publish_message.html', context)
        return _create_message_post_request(request)
    else:
        return render(request, 'message_publisher/create_and_publish_message.html', context)


def _to_form_context(request):
    context = {
        'User': get_user(request)
    }
    return context


def _create_message_post_request(request):
    user = _define_username(request)
    uploaded_image = _upload_file(request)
    _create_message_object_in_database(user, request, uploaded_image)
    return redirect('message_publisher:main')


def _define_username(request):
    user = get_user(request)
    if not user.username:
        user = 'Anonymous'
    else:
        user = user.username
    return user


def _upload_file(request):
    if request.FILES:
        fs = FileSystemStorage()
        uploaded_image = request.FILES['image_file']
        fs.save(uploaded_image.name, uploaded_image)
        return uploaded_image
    else:
        return None


def _create_message_object_in_database(user, request, uploaded_image):
    message = Message(user=user, message_body=request.POST['message_body'], image=uploaded_image)
    message.save()


def _filtered_messages(request):
    if request.GET['filter']:
        messages = Message.objects.filter(user=request.GET['filter'])
    else:
        messages = Message.objects.all()
    if 'this_day' in request.GET:
        messages = _last_twenty_four_hours_messages(messages)
    if request.GET['choise'] == 'new':
        messages = _get_newest_messages(messages)
    elif request.GET['choise'] == 'old':
        messages = _get_oldest_messages(messages)
    return messages


def _unfiltered_messages():
    messages = Message.objects.all().order_by('-pub_date')
    return messages


def _get_newest_messages(messages):
    messages = messages.order_by('-pub_date')
    return messages


def _get_oldest_messages(messages):
    messages = messages.order_by('pub_date')
    return messages


def _last_twenty_four_hours_messages(messages):
    day = timezone.now() - timezone.timedelta(hours=24)
    messages = messages.filter(pub_date__gt=day)
    return messages