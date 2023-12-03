import re

USERNAME_REGEX = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
PASSWORD_REGEX = re.compile(r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[a-zA-Z\d]{8,}$")



class Validation: 


    def validate_username(self,username: str) -> bool:
        return bool(USERNAME_REGEX.match(username))
    
    def validate_password(self,password: str) -> bool:
        return bool(PASSWORD_REGEX.match(password))