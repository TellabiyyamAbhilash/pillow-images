from .models import *
from rest_framework import serializers

class userserializer(serializers.Serializer):
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    email = serializers.EmailField()
    password = serializers.CharField()

class loginserializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()

class inputimageserializer(serializers.Serializer):
    input_image = serializers.ImageField()