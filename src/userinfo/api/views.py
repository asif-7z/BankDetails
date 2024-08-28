# myapp/views.py

from rest_framework import generics, status
from django.contrib.auth import get_user_model
from django.contrib.auth.signals import user_logged_in, user_logged_out
from django.dispatch import receiver
from rest_framework.permissions import IsAuthenticated,AllowAny
from django.utils import timezone
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from userinfo.models import BankAccount, Transaction, LoginLogoutHistory
from .serializers import (
    RegisterSerializer,
    BankAccountSerializer,
    TransactionSerializer,
    LoginLogoutHistorySerializer,
)
from decimal import Decimal
from rest_framework.views import APIView


User = get_user_model()

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer

class LogoutView(APIView):
    def post(self, request):
        # try:
        #     refresh_token = request.data.get("refresh")
        #     if not refresh_token:
        #         return Response({"error": "Refresh token is required"}, status=400)

        #     token = RefreshToken(refresh_token)
        #     token.blacklist()

            # Record logout time
        LoginLogoutHistory.objects.create(user=request.user, logout_time=timezone.now())

        return Response({"message": "Successfully logged out"}, status=200)
        # except Exception as e:
        #     return Response({"error": str(e)}, status=400)

class BankAccountListCreateView(generics.ListCreateAPIView):
    queryset = BankAccount.objects.all()
    serializer_class = BankAccountSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class DepositWithdrawView(generics.GenericAPIView):
    queryset = BankAccount.objects.all()
    serializer_class = TransactionSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        print("Request data:", request.data)
        transaction_type = request.data.get('transaction_type')
        amount = request.data.get('amount')
        account_id = request.data.get('account')
        print(account_id)
        
        
        # Ensure amount is provided and is a valid number
        if not amount or not isinstance(amount, (int, float, str)) or not str(amount).replace('.', '', 1).isdigit():
            return Response({"error": "Invalid amount."}, status=status.HTTP_400_BAD_REQUEST)
        
        amount = float(amount)  # Convert amount to float after validation
        amount = Decimal(str(amount))


        # Handle BankAccount retrieval
        try:
            account = BankAccount.objects.get(pk=account_id, user=request.user)
        except BankAccount.DoesNotExist:
            return Response({"error": "Bank account not found."}, status=status.HTTP_404_NOT_FOUND)

        # Validate transaction type
        if transaction_type not in ['DEPOSIT', 'WITHDRAW']:
            return Response({"error": "Invalid transaction type."}, status=status.HTTP_400_BAD_REQUEST)

        # Check for sufficient funds
        if transaction_type == 'WITHDRAW' and account.balance < amount:
            return Response({"error": "Insufficient funds."}, status=status.HTTP_400_BAD_REQUEST)

        # Update balance
        if transaction_type == 'DEPOSIT':
            account.balance += amount
            
        else:  # For WITHDRAW
            account.balance -= amount
        account.save()

        # Record transaction
        Transaction.objects.create(account=account, transaction_type=transaction_type, amount=amount)

        # Prepare the response message
        if transaction_type == 'DEPOSIT':
            response_message = f"Transaction successful: {transaction_type} of +{amount}. avalable balance = {account.balance}"
        else:
            response_message = f"Transaction successful: {transaction_type} of -{amount}. avalable balance = {account.balance}"



        return Response({"message": response_message}, status=status.HTTP_200_OK)


class LoginLogoutHistoryView(generics.ListAPIView):
    queryset = LoginLogoutHistory.objects.all()
    serializer_class = LoginLogoutHistorySerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)

@receiver(user_logged_in)
def user_logged_in_handler(sender, request, user, **kwargs):
    LoginLogoutHistory.objects.create(user=user, login_time=timezone.now())

@receiver(user_logged_out)
def user_logged_out_handler(sender, request, user, **kwargs):
    LoginLogoutHistory.objects.create(user=user, logout_time=timezone.now())

