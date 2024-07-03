from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model


from firebase_admin import credentials
from firebase_admin import auth as firebase_auth

from .models import User, Profile

class EmailBackend(ModelBackend):
    def authenticate(self, request, email, password):
        try:
            user = User.objects.get(email = email)
            print(user)
        except User.DoesNotExist:
            return None
        print(user.check_password(user))
        if user.check_password(password):
            return user

    def get_user(self, user_id):
        UserModel = get_user_model()
        try:
            return UserModel.objects.get(pk=user_id)
        except UserModel.DoesNotExist:
            return None


class FirebaseBackend(ModelBackend):
    def authenticate(self, request, id_token):
        try:
            # Verify the ID token first
            decoded_token = firebase_auth.verify_id_token(id_token)
            user_uid = decoded_token['uid']
            firebase_user = firebase_auth.get_user(user_uid)

            if firebase_user:
                if not firebase_user.email:
                    user_email = ""
                else:
                    user_email = firebase_user.email
                if User.objects.filter(
                    email = user_email,
                    username = user_email,
                    id = user_uid,
                ).exists():
                    user = User.objects.get(
                        id = user_uid,
                        email = user_email,
                        username= user_email,
                    )
                    return user
                else:
                    user = User.objects.create(
                        id = user_uid,
                        email = user_email,
                        username= user_email,
                    )
                    profile = Profile.objects.create(
                        user = user,
                        phone_number = firebase_user.phone_number,
                        full_name = firebase_user.display_name,
                        bio = "",
                    )
                    return user
                
            else:
                return None
        except Exception as e:
            print(e)
            return None
    
    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None