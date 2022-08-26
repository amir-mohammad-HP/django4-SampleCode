from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend

class EmailAuthentication(ModelBackend):
    def authenticate(self, request, email=None, password=None, **kwargs):
        UserModel = get_user_model()
        try:
            user = UserModel.objects.get(email=email)
        except UserModel.DoesNotExist:
            return None
        except UserModel.MultipleObjectsReturned:
            return None # in case multiple users with the same email exist none of them will authentify
        else:
            if user.check_password(password):
                return user
        return None