from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from django.db.models import Q
from .models import Message

@login_required
def load_messages_home(request):
    users = None
    if request.method=="POST":
        search = request.POST.get('searchuser')
        users = User.objects.filter(username__icontains=search)
        if users.count()>0:
            return load_messages(request, users[0].pk, users)
    return load_messages(request, request.user.pk, users)

@login_required
def load_messages(request, pk, users=None):
    other_user = get_object_or_404(User, pk=pk)
    messages = Message.objects.filter( Q(sender=request.user), Q(receiver=other_user))
    messages.update(seen=True)
    context = {
        "other_user": other_user,
        "messages": messages,
    }

    return render(request, "privatChat.html", context)
