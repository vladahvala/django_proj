from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

#ForeignKey - one to many

class Message(models.Model):
    sender = models.OneToOneField(User, 
                                  on_delete=models.CASCADE, related_name='sent_messages')
    receiver = models.ForeignKey(User, 
                                on_delete=models.CASCADE, related_name='received_messages')
    text = models.TextField()
    date_created = models.DateTimeField(default=timezone.now)
    seen = models.BooleanField(default = False) #true or false
    class Meta:
        ordering = ('date_created',)
    def __str__(self):
        return self.text