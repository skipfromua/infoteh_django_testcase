from django.shortcuts import render, redirect
from .services import registrate_new_user_and_give_permissions


def registration(request):
    if request.method == 'POST':
        message, context = registrate_new_user_and_give_permissions(request)
        if message:
            return redirect('message_publisher:main')
        else:
            return render(request, 'registration/registration.html', context)
    else:
        return render(request, 'registration/registration.html')