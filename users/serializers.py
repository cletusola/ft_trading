from django.contrib.auth import get_user_model
User = get_user_model()


from rest_framework import serializers 



# register serializer 
class RegisterSerializer(serializers.Serializer): 
    firstname = serializers.CharField(max_length=20, required=True)
    lastname = serializers.CharField(max_length=20, required=True)
    username = serializers.CharField(max_length=20, required=True)
    email = serializers.EmailField(max_length=50,required=True)
    password = serializers.CharField(required=True)
    password_again = serializers.CharField(required=True)


""" Login serializer """ 
class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(min_length=4, max_length=20, required=True)
    password = serializers.CharField(required=True)


