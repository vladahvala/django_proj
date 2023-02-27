from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from django.db.models import Q
from .models import Message

@login_required
def load_messages_home(request): #запит на чат із певною людиною
    users = None
    if request.method=="POST":
        search = request.POST.get('searchuser')
        users = User.objects.filter(username__icontains=search)
        if users.count()>0:
            return load_messages(request, users[0].pk, users)
    return load_messages(request, request.user.pk, users) #чат "із собою"

@login_required
def load_messages(request, pk, users=None):
    other_user = get_object_or_404(User, pk=pk)
    messages = Message.objects.filter( Q(sender=request.user), Q(receiver=other_user))
    messages.update(seen=True)

    if not users: #якщо юзера не знаходить, то показуємо всіх користувачів
        users = User.objects.all() 

    context = {
        "other_user": other_user,
        "messages": messages,
        "users": users,
    }

    return render(request, "privatChat.html", context)

def search_user(request):
    return load_messages_home(request)
