from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid
import random
import string
from .sender import send_otp
from django.utils import timezone



class User(AbstractUser):
    pass

class OTPRequestQuerySet(models.QuerySet):
    def is_valid(self, reciver, request, password):
        current_time = timezone.now()
        return self.filter(
            reciver = reciver,
            request_id = request,
            password = password,
            created_at__lt = current_time,
            created_at__gt = current_time - timezone.timedelta(minutes=2)
        ).exists()


class OTPManager(models.Manager):
    def get_queryset(self):
        return OTPRequestQuerySet(self.model, using=self._db)

    def is_valid(self, reciver, request, password):
        return self.get_queryset().is_valid(reciver, request, password)


    def generate(self, data):
        otp = self.model(reciver=data['reciver'],channel=data['channel'])
        otp.save(using = self._db)
        send_otp(otp)
        return otp



def random_pass():
    rand = random.SystemRandom()
    digits = rand.choices(string.digits,k=4)
    return ''.join(digits)

class RequestOTP(models.Model):
    class OTPTypeChoiches(models.TextChoices):
        Phone = 'Phone'
        Email = 'E-mail'
    request_id = models.UUIDField(primary_key=True, editable=False,default=uuid.uuid4)
    channel = models.CharField(max_length=10,choices=OTPTypeChoiches.choices,default=OTPTypeChoiches.Phone)
    reciver = models.CharField(max_length=50)
    password = models.CharField(max_length=4, default=random_pass )
    created_at = models.DateTimeField(auto_now_add=True, editable=False)

    objects = OTPManager()