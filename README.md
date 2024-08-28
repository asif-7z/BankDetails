# BankDetails

## login credentials
```
username : asif
password :admin@123
```

## generate access token
- Register account
```
http://127.0.0.1:8000/api/register/
```
- login
```
http://127.0.0.1:8000/login
```
## token generated
- for example
```
{
    "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTcyNDkyMDU3MiwiaWF0IjoxNzI0ODM0MTcyLCJqdGkiOiI0MDQyMWE4ODlmYTU0Y2FlYTE4YmMxODVkOTlmNDZmMCIsInVzZXJfaWQiOjF9.ti4B_xAp-MnKbQXr2AGO-qH_l-YfhgzklwpYeKbBk9w",
    "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzI0ODM3NzcyLCJpYXQiOjE3MjQ4MzQxNzIsImp0aSI6IjJkMmZiNThlM2Q0NDRiNTc5YjgyN2Y1NzFiMTdlNzY2IiwidXNlcl9pZCI6MX0.vCrjUKfP5hrZtCQze1ZVDsyuYL0litqJy0PUYCqEnn8"
}
```




## endpoints

```
api/register/
api/login/?token=" access token "
api/token/refresh/?token=" access token "
api/logout/?token=" access token "
api/accounts/?token=" access token "
api/transaction/?token=" access token "
api/login-logout-history/?token=" access token "
api/deposite_withdraw/?token=" access token "

```

