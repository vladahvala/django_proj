from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from django.db.models import Q
from django.http.response import JsonResponse
from django.contrib.humanize.templatetags.humanize import naturaltime
from .models import Message
import json

def unread_msgs(request, sender):
    msgs = Message.objects.filter(Q(seen=False) & Q(receiver=request.user, sender=sender))
    return msgs.count()


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
    messages = messages | Message.objects.filter( Q(receiver=other_user), Q(sender=request.user))

    if not users: #якщо юзера не знаходить, то показуємо всіх користувачів
        users = User.objects.all() 

    print("Словник")

    unread_num_dict = {} #{"other_user"}: 19, ...
    for usr in users:
        unread_num_dict[usr.username] = unread_msgs(request, usr)

    context = {
        "other_user": other_user,
        "messages": messages,
        "users": users,
        "unread_num_dict": unread_num_dict
    }

    return render(request, "privatChat.html", context)

@login_required
def load_msgAJAX(request, pk):
    other_user = get_object_or_404(User, pk=pk)
    messages = Message.objects.filter(seen=False, receiver=request.user, sender=other_user)

    message_list = []
    for msg in messages:
        message_list.append({
            "sender": msg.sender.username,
            "message": msg.text,
            "date_created": naturaltime(msg.date_created)
        })
        msg.seen = True
    messages.update(seen=True)

    if request.method=="POST":
        inMessage = json.loads(request.body)["message"]
        if inMessage:
            m = Message.objects.create(sender=request.user, receiver=other_user, text=inMessage)
            m.save()
            message_list.append({
            "sender": m.sender.username,
            "message": m.text,
            "date_created": naturaltime(m.date_created)
            })
    return JsonResponse(message_list, safe=False)

def search_user(request):
    return load_messages_home(request)
