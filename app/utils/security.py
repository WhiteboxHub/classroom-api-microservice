import jwt
import bcrypt
from jose import jwt, JWTError
from datetime import datetime, timedelta

SECRET_KEY = "secret_key"  
ALGORITHM = "HS256"  # Must be consistent

def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

def verify_password(password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8'))

def create_jwt_token(email: str, role: str = "user") -> str:
    expiration = datetime.utcnow() + timedelta(hours=2)
    payload = {"email": email, "role": role, "exp": expiration}
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

def decode_jwt_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        return None
