# myapp/urls.py

from django.urls import path
from .views import (
    RegisterView,
    LogoutView,
    BankAccountListCreateView,
    DepositWithdrawView,
    LoginLogoutHistoryView,
    DepositWithdrawView,
)
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('accounts/', BankAccountListCreateView.as_view(), name='bank_accounts'),
    path('transaction/', DepositWithdrawView.as_view(), name='transaction'),
    path('login-logout-history/', LoginLogoutHistoryView.as_view(), name='login_logout_history'),
    path('deposite_withdraw/',DepositWithdrawView.as_view(),name='deposite_withdraw'),
]
