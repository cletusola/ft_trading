from django.contrib.auth import get_user_model
User = get_user_model()

from rest_framework import serializers 

import re


# register serializer 
class RegisterSerializer(serializers.Serializer): 
    firstname = serializers.CharField(min_length=2, max_length=20, required=True)
    lastname = serializers.CharField(min_length=2, max_length=20, required=True)
    username = serializers.CharField(min_length=4, max_length=20, required=True)
    email = serializers.EmailField(min_length=8, max_length=50,required=True)
    password = serializers.CharField(required=True)
    password_again = serializers.CharField(required=True)


    """ validate firstname """ 
    def validate_firstname(self, value):
        # firstname = data.get('firstname').lower()

        if value == " ":
            raise serializers.ValidationError("Firstname is required")
        
        # check firstname length
        if len(value) < 2 or len(value) > 20:
            raise serializers.ValidationError("Firstname must be between 2 to 20 characters")

        return value

    """ validate lastname """ 
    def validate_lastname(self, value):

        if value == " ":
            raise serializers.ValidationError("Lastname is required")
        
        # check lastname length
        if len(value) < 2 or len(value) > 20:
            raise serializers.ValidationError("Lastname must be between 2 to 20 characters")

        return value


    """ validate username """ 
    def validate_username(self, value):
        # check if username already exists 
        chk_username = User.objects.filter(username__iexact=value)

        if chk_username.count():
            raise serializers.ValidationError(f" username {value} is not available")

        # check username length 
        if len(value) < 4 or len(value) > 20:
            raise serializers.ValidationError("username must be between 4 to 20 characters")
        #check if username is empty 
        if value == " ":
            raise serializers.ValidationError("username can not be empty")

        return value

    """ validate email """ 
    def validate_email(self, value):

        # check if email exists 
        chk_email = User.objects.filter(email__iexact=value)

        if chk_email.count():
            raise serializers.ValidationError(f"email {value} is unavailable")

        #check email length 
        if len(value) < 8 or len(value) > 60:
            raise serializers.ValidationError("email must be between 6 to 60 characters")
        #check if email is empty 
        if value == " ":
            raise serializers.ValidationError("email cannot be empty")

        return value  


    """ validate password """
    def validate(self, data):
        password1 = data.get('password')
        password2 = data.get('password_again')

        if password1 and password2 and password1 != password2:
            raise serializers.ValidationError("passwords do not match")

        if not re.search("[@_!#$%^&*()<>?/\|}{~:]", password1):
            raise serializers.ValidationError("password must contain at least on special character")

        if not any(p.isupper() for p in password1):
            raise serializers.ValidationError("password must contain at least one uppercase letter")

        if not any(p.islower() for p in password1):
            raise serializers.ValidationError("password must contain at least one lowercase latter")

        if not any(p.isdigit() for p in password1):
            raise serializers.ValidationError("password must contain at least a digit")


        return data 

""" Login serializer """ 
class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(min_length=4, max_length=20, required=True)
    password = serializers.CharField(required=True)


