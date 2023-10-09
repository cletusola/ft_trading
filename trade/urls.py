from django.urls import path

from .views import Dashboard, GetUserDashboard, GetUsers



urlpatterns = [
    path('admin/users/', GetUsers.as_view(), name="get_users"),
    path('admin/user/dashboard/', GetUserDashboard.as_view(), name="user_dashboard"),
    path('dashboard/', Dashboard.as_view(), name="dashboard"),
]
