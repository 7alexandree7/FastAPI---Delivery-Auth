from security.create_token import create_token
from security.authenticate_user import authenticate_user
from security.verify_token import verify_token
from models.models import User
from schema.schemas import UserSchema, LoginSchema
from db.session import get_session
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from main import bcrypt_context
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


@auth_route.post("/login-form")
async def login_form(data_form: OAuth2PasswordRequestForm = Depends(), session: Session = Depends(get_session)):
    user = authenticate_user(data_form.username, data_form.password, session)
    access_token = create_token(user.id)

    return {
        "access_token": access_token,
        "token_type": "Bearer",
    }



@auth_route.post("/refresh")
async def refresh_token(user: User = Depends(verify_token)):
    new_access_token = create_token(user.id)
    new_refresh_token = create_token(user.id, duration_token=timedelta(days=7))

    return {
        "access_token": new_access_token,
        "refresh_token": new_refresh_token,
        "token_type": "Bearer",
    }