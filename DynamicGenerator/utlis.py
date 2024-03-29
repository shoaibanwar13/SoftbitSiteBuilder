import uuid
from django.contrib.auth.tokens import PasswordResetTokenGenerator
import six

class tokengenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        return (six.text_type(user.pk)+six.text_type(timestamp)+six.text_type(user.is_active))
generate_token=tokengenerator()
def generate_ref_code():
    code=str(uuid.uuid4()).replace("-","")[:5]
    return code
