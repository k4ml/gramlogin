
from django.core.signing import TimestampSigner
from django.contrib.auth.models import User

class TelegramBackend(object):
    def authenticate(self, request, auths=None):
        signer = TimestampSigner()
        try:
            username = signer.unsign(auths, max_age=60*2)
        except Exception as e:
            print(e)
            return None

        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            print("%s does not exists" % username)
            return None

        return user

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
