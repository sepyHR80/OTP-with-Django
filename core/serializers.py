from rest_framework import serializers
from .models import RequestOTP



class OTPRequestSerializers(serializers.Serializer):
    reciver = serializers.CharField(max_length=50, allow_null = False)
    channel = serializers.ChoiceField(choices =RequestOTP.OTPTypeChoiches.choices , allow_null = False)


class OTPRequestResponseSerializers(serializers.ModelSerializer):
    class Meta:
        model = RequestOTP
        fields = ['request_id']

class VerifyOTPRequestSerializers(serializers.Serializer):
    request_id = serializers.UUIDField(allow_null = False)
    password = serializers.CharField(max_length=50, allow_null = False)
    reciver = serializers.CharField(max_length=50, allow_null = False)

class ObtainTokenSerializer(serializers.Serializer):
    token = serializers.CharField(max_length=50, allow_null = False)
    refresh = serializers.CharField(max_length=50, allow_null = False)
    created = serializers.BooleanField()
    
