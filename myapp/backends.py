from django.contrib.auth.backends import ModelBackend
from .models import Employee

class PlainTextAuthBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = Employee.objects.get(email=username)
            if user.check_password(password):  # Utilisation de check_password pour vérifier le mot de passe haché
                return user
            else:
                print('Password incorrect')
        except Employee.DoesNotExist:
            print('User does not exist')
            return None
