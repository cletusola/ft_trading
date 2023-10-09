from django.contrib.auth import authenticate, logout
from django.contrib.auth import get_user_model
User = get_user_model()

from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.token_blacklist.models import OutstandingToken, BlacklistedToken
from rest_framework.response import Response 
from rest_framework.views import APIView
from rest_framework import permissions, status, generics

from .serializers import RegisterSerializer, LoginSerializer
from trade.models import Trade  

import re 
import random 
from datetime import datetime, timedelta



# time frame function
def get_time(n):
    current_time = datetime.now()
    futre_time = current_time + timedelta(minutes=n)
    str_future_time = futre_time.strftime("%H:%M")
    return(str_future_time)



# register view 
class RegisterView(generics.CreateAPIView):

    permissions_classes = (permissions.AllowAny, )

    def post(self, request, *args, **kwargs):
        serializer = RegisterSerializer(data=request.data)

        if serializer.is_valid(raise_exception=False):
            firstname = serializer.data["firstname"]
            lastname = serializer.data["lastname"]
            username = serializer.data["username"].lower()
            email = serializer.data["email"].lower()
            password = serializer.data["password"]
            password_again = serializer.data["password_again"]

            # check if username already exists 
            chk_username = User.objects.filter(username__iexact=username)

            # check if email already exists 
            chk_email = User.objects.filter(email__iexact=email)


            """ validate field data """

            # check if password and password_again are the same 
            if not re.search("[@_!#$%^&*()-<>?/\|}={+~:]", password):
                return Response({
                    "password_error": "Password must contain at least one special character"
                })
            elif len(password) < 8:
                return Response({
                    "password_error": "Pasword must be atleast 8 characters"
                })
            elif password and password_again != password:
                return Response({
                    "password_error": "passwords must match"
                })
                
            elif not any(p.isupper() for p in password):
                return Response({
                    "password_error": "Password must have at least one uppercase letter"
                })
            elif not any(p.islower() for p in password):
                return Response({
                    "password_error":"Password must have at least one lowercase letter"
                })
            elif not any(p.isdigit() for p in password):
                return Response({
                    "password_error":"Password must have at least a digit"
                })

            # validate firstname 
            elif firstname == " ":
                return Response({
                    "firstname_error": "Fristname is required"
                })
            elif len(firstname) < 2 or len(firstname) > 20:
                return Response({
                    "firstname_error": "Firstname must be between 2 to 20 characters long"
                })

            # validate lastname 
            elif lastname == " ":
                return Response({
                    "lastname_error": "Lastname is required"
                })
            elif len(lastname) < 2 or len(lastname) > 20:
                return Response({
                    "lastname_error": "Lastname must be between 2 to 20 characters long"
                })

            # validate username
            elif username == " ":
                return Response({
                    "username_error": "Username is required"
                })
            elif chk_username.count():
                return Response({
                    "username_error":"user with this username already exists"
                })
            elif len(username) < 4 or len(username) > 20:
                return Response({
                    "username_error": "Username must be between 4 to 20 characters"
                })

            # validate email 
            elif email == " ":
                return Response({
                    "email_error": "Email is required"
                })
            elif chk_email.count():
                return Response({
                    "email_error":"user with this email already exists"
                })
            elif len(email) < 6 or len(email) > 50:
                return Response({
                    "email_error": "Email must be between 6 to 50 characters",
                    "status":status.HTTP_400_BAD_REQUEST
                })
            else:
                try: 
                    # create user instance 
                    user = User.objects.create_user(
                        firstname=firstname,
                        lastname=lastname,
                        username=username,
                        email=email,
                        password=password
                    )
                    # save user 
                    user.save()
                    try:
                        # create 5 times profit or loss data with random numbers for user trade 
                        
                        # trade 1
                        trade1 = Trade.objects.create(
                            profit_or_loss = random.randint(-50, 50),
                            user = user,
                            time = get_time(0)
                        )
                        trade1.save()

                        # trade2
                        trade2 = Trade.objects.create(
                            profit_or_loss = random.randint(-50, 50),
                            user = user,
                            time = get_time(1)
                        )
                        trade2.save()

                        # trade3
                        trade3 = Trade.objects.create(
                            profit_or_loss = random.randint(-50, 50),
                            user = user,
                            time = get_time(2)
                        )
                        trade3.save()

                        # trade4
                        trade4 = Trade.objects.create(
                            profit_or_loss = random.randint(-50, 50),
                            user = user,
                            time = get_time(3)
                        )
                        trade4.save()

                        # trade 5
                        trade5 = Trade.objects.create(
                            profit_or_loss = random.randint(-50, 50),
                            user = user,
                            time = get_time(4)
                        )
                        trade5.save()
                    except:
                        return Response({
                            "error": "Unable to create trade",
                        })

                    return Response({
                        "success": "User account created successfully",
                        "status": status.HTTP_201_CREATED
                    })
                                        
                except:
                    return Response({
                        "error": "Unable to create account",
                    })
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



""" Login View """ 
class LoginView(APIView):

    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid(raise_exception=True):
            username = serializer.validated_data["username"].lower()
            password = serializer.validated_data["password"]

            user = authenticate(username=username, password=password)

            if user is not None:
                
                if user.is_active:
                    
                    refresh = RefreshToken.for_user(user)
                    access_token = str(refresh.access_token)

                    return Response({
                        "access": access_token,
                        # "refresh_token": refresh
                        },
                        status = status.HTTP_200_OK
                    )
                else:

                    return Response({
                        "message":"Your account is inactive, please contact our support"
                        },
                        status = status.HTTP_401_UNAUTHORIZED
                    )
            else:
                
                return Response({
                    "message":"Incorrect username or password"
                    },
                    status = status.HTTP_401_UNAUTHORIZED
                )
        return Response(status= status.HTTP_400_BAD_REQUEST)
