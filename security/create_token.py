from jose import jwt
from datetime import datetime, timedelta, timezone
from main import ACCESS_TOKEN_EXPIRES_MINUTES, SECRET_KEY, ALGORITHM


def create_token(id_user, duration_token=timedelta(minutes=ACCESS_TOKEN_EXPIRES_MINUTES)):
    expiration_date = datetime.now(timezone.utc) + duration_token
    dic_info = { "sub": id_user, "exp": expiration_date }
    encoded_jwt = jwt.encode(dic_info, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt
