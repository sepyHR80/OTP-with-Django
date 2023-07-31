from django.shortcuts import render
from rest_framework.views import APIView
from . import serializers
from rest_framework.response import Response
from rest_framework import status
from . import models
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken


class OTPView(APIView):
    def get(self, request):
        serializer = serializers.OTPRequestSerializers(data = request.query_params)
        if serializer.is_valid():
            data = serializer.validated_data
            try:
                otp = models.RequestOTP.objects.generate(data)
                return Response(data =serializers.OTPRequestResponseSerializers(otp).data)
            except Exception as e:
                print(e)
                return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST,data =serializer.errors) 
    def post(self, request):
        serializer = serializers.VerifyOTPRequestSerializers(data = request.data)
        if serializer.is_valid():
            data = serializer.validated_data
            if models.RequestOTP.objects.is_valid(data['reciver'],data['request_id'],data['password']):
                return Response(self._handle_login(data))
        else :
            return Response(status=status.HTTP_401_UNAUTHORIZED,data =serializer.errors)

    def _handle_login(self, otp):
        User = get_user_model()
        query = models.User.objects.filter(username = otp['reciver'])
        if query.exists():
            created = False
            user = query.first()
        else :
            user  = models.User.objects.create(username = otp['reciver'])
            created = True

        refresh = RefreshToken.for_user(user)

        return serializers.ObtainTokenSerializer({
            'refresh' : str(refresh),
            'token' : str(refresh.access_token),
            'created' : created
        }).data