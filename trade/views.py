from django.contrib.auth import get_user_model
User = get_user_model()

from rest_framework.response import Response 
from rest_framework.views import APIView
from rest_framework import permissions, status, generics 

from .models import Trade, Profile
from .serializers import ProfileSerializer, TradeSerializer, UserSerializer

 

# dashboard view 
class Dashboard(APIView):

    permissions_classes = (permissions.IsAuthenticated, )

    # get objects by user 
    def get(self, request, format=None): 

        # get profile query 
        profile = Profile.objects.filter(username=request.user)
        # profile serializer 
        profile_serializer = ProfileSerializer(profile, many=True)
        # profit and loss query
        profit_or_loss_data = Trade.objects.filter(user=self.request.user).values_list('profit_or_loss', flat=True)
        # trade time query 
        trade_time_data = Trade.objects.filter(user=self.request.user).values_list('time', flat=True)
        # convert profit and loss query to list 
        profit_or_loss = list(profit_or_loss_data)
        # convert trade time query to list
        trade_time = list(trade_time_data)


        data = {
            "profit_or_loss": profit_or_loss,
            "trade_time": trade_time,
            "profile": profile_serializer.data
        }

        return Response (data, status=status.HTTP_200_OK) 

#admin profile view 
class GetUsers(APIView):
    permissions_classes = (permissions.IsAdminUser, )

    def get(self, request, format=None):
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

# dynamically get trade data by specific user
class GetUserDashboard(APIView):
    permissions_classes = (permissions.IsAdminUser, )

    def post(self, request, format=None):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            username = serializer.validated_data["username"].lower()

            user = User.objects.get(username=username)
            # get profile query 
            profile = Profile.objects.filter(username=user)
            # profile serializer 
            profile_serializer = ProfileSerializer(profile, many=True)
            # profit and loss query
            profit_or_loss_data = Trade.objects.filter(user=user).values_list('profit_or_loss', flat=True)
            # trade time query 
            trade_time_data = Trade.objects.filter(user=user).values_list('time', flat=True)
            # convert profit and loss query to list 
            profit_or_loss = list(profit_or_loss_data)
            # convert trade time query to list
            trade_time = list(trade_time_data)


            data = {
                "profit_or_loss": profit_or_loss,
                "trade_time": trade_time,
                "profile": profile_serializer.data
            }

            return Response (data, status=status.HTTP_200_OK) 










