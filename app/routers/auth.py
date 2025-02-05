# from fastapi import APIRouter, Depends, HTTPException
# from fastapi.security import OAuth2PasswordBearer
# import jwt

# router = APIRouter(prefix="/auth", tags=["auth"])

# oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
# SECRET_KEY = "secret123"

# def verify_token(token: str = Depends(oauth2_scheme)):
#     """Verify JWT token."""
#     try:
#         payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
#         return payload  # Return user info from token
#     except jwt.ExpiredSignatureError:
#         raise HTTPException(status_code=401, detail="Token expired")
#     except jwt.InvalidTokenError:
#         raise HTTPException(status_code=401, detail="Invalid token")
