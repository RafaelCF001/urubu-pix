from models.handler import Handler
import bcrypt


class PasswordVerifier(Handler):
    def handle(self, request):
        if request["action"] == "verify":
            print(request["password"])
            password = request["password"].encode()
            print(request["hashed_password"])
            hashed_password = request["hashed_password"].encode('utf-8')

            if bcrypt.checkpw(password, hashed_password):
                return True
            else:
                return False

        return super().handle(request)
