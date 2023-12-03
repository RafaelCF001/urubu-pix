import bcrypt
from models.handler import Handler

class PasswordHasher(Handler):
    def handle(self, request):
        if request["action"] == "hash":
            password = request["password"].encode()
            hashed_password = bcrypt.hashpw(password, bcrypt.gensalt())
            return hashed_password

        return super().handle(request)
