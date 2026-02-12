from fastapi import APIRouter, Depends, HTTPException
from models.models import User
from db.session import get_session
from main import bcrypt_context
from security.jwt import authenticate_user, create_token, verify_token
from schema.schemas import UserSchema, LoginSchema
from sqlalchemy.orm import Session
from datetime import timedelta


auth_route = APIRouter(prefix="/auth", tags=["auth"])


@auth_route.get("/")
async def get_auth():
    return {"message": "voce acessou a rota de auth"}


@auth_route.post("/create_user")
async def create_user( userSchema: UserSchema, session: Session = Depends(get_session)):
    user = session.query(User).filter(User.email == userSchema.email).first()

    if user:
        raise HTTPException(status_code=400, detail="user already exists")
    
    else:
        password_encrypted = bcrypt_context.hash(userSchema.password)
        new_user = User(userSchema.name, userSchema.email, password_encrypted, userSchema.is_active, userSchema.admin)
        session.add(new_user)
        session.commit()
        return HTTPException(status_code=201, detail=f"user created {new_user.name}")



@auth_route.post("/login")
async def login(loginSchema: LoginSchema, session: Session = Depends(get_session)):
    user = authenticate_user(loginSchema.email, loginSchema.password, session)

    access_token = create_token(user.id)
    refresh_token = create_token(user.id, duration_token=timedelta(days=7))

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "Bearer",
    }



@auth_route.get("/refresh")
async def refresh_token(token):
    user = verify_token(token)
    access_token = create_token(user.id)

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "Bearer",
    }