from django.contrib.auth import get_user_model
User = get_user_model()

from rest_framework import serializers

from .models import Profile, Trade




# profile serializer 
class ProfileSerializer(serializers.ModelSerializer):
    username = serializers.CharField(required=False)#this is the make the username field return a string and not an object

    class Meta:
        model = Profile
        fields = ['id','firstname','lastname','username','email']


# trade serializer 
class TradeSerializer(serializers.ModelSerializer):
    user = serializers.CharField(required=False)#this is the make the user field return a string and not an object

    class Meta:
        model = Trade
        fields = ['id','balance','profit_or_loss','user','time']

""" user serializer """ 
class UserSerializer(serializers.Serializer):
    username = serializers.CharField(required=False)
