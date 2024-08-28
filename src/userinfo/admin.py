from django.contrib import admin

# Register your models here.
from .models import CustomUser,BankAccount,Transaction,LoginLogoutHistory

admin.site.register(CustomUser)
admin.site.register(BankAccount)
admin.site.register(Transaction)
admin.site.register(LoginLogoutHistory)