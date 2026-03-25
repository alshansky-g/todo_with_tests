from django.http import HttpRequest

from accounts.models import Token, User


class PasswordlessAuthenticationBackend:
    def authenticate(self, request: HttpRequest, uid: str) -> User | None:
        try:
            token = Token.objects.get(uid=uid)
            return User.objects.get(email=token.email)
        except Token.DoesNotExist:
            return None
        except User.DoesNotExist:
            return User.objects.create(email=token.email)

    def get_user(self, email: str):
        try:
            return User.objects.get(email=email)
        except User.DoesNotExist:
            return None
