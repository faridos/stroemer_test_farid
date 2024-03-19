from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework import exceptions

from myauth.models import FakeUser


class FakeUserAuthentication(JWTAuthentication):
    def authenticate(self, request):
        try:
            # Attempt to authenticate the token
            user = super().authenticate(request)
        except exceptions.AuthenticationFailed:
            # If authentication fails, return a fake user object
            return (FakeUser(id=99999942), None)
        else:
            return user