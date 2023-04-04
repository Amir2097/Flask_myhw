import time
import uuid
from dotenv import load_dotenv
import flask_bcrypt
from errors import HttpError
from flask import request
from models import Token
import os
from app import create_app

app = create_app()
bcrypt = flask_bcrypt.Bcrypt(app)

load_dotenv()

TOKEN_TTL = int(os.getenv("TOKEN_TTL"))


def hash_password(password: str) -> str:
    return bcrypt.generate_password_hash(password.encode()).decode()


def check_password(password_hash: str, password: str) -> bool:
    return bcrypt.check_password_hash(password_hash.encode(), password.encode())


def check_auth(session) -> Token:
    try:
        token = uuid.UUID(request.headers.get("token"))
    except (ValueError, TypeError):
        raise HttpError(403, "incorrect token")
    token = session.query(Token).get(token)

    if token is None:
        raise HttpError(403, "incorrect token")

    if time.time() - token.creation_time.timestamp() > TOKEN_TTL:
        raise HttpError(403, "incorrect token")

    return token