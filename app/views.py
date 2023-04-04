from models import Session, Ads, User
from flask import jsonify, request
from flask.views import MethodView
from crud import get_item, create_item, patch_item, delete_item
from schema import validate, CreateItem, CreateUser, AdsData
from errors import HttpError
from auth import hash_password, check_password, check_auth
from schema import RegisterUser, LoginUser
from models import Token
from sqlalchemy.exc import IntegrityError


def register():
    user_data = validate(RegisterUser, request.json)
    with Session() as session:
        user_data["password"] = hash_password(user_data["password"])
        user = create_item(session, User, **user_data)
        return jsonify({
            "id": user.id
        })


def login():
    login_data = validate(LoginUser, request.json)
    with Session() as session:
        user = session.query(User).filter(User.email == login_data["email"]).first()
        if user is None or not check_password(user.password, login_data["password"]):
            raise HttpError(401, "Invalid user or password")

        token = Token(user=user)
        session.add(token)
        session.commit()
        return jsonify({
            "token": token.id
        })


class UserView(MethodView):

    def get(self, user_id: int):
        with Session() as session:
            user = get_item(session, User, user_id)
            return jsonify({
                'id': user.id, 'email': user.email
            })

    def patch(self, user_id: int):
        with Session() as session:
            data_to_change = validate(CreateUser, request.json)
            if 'password' in data_to_change:
                data_to_change['password'] = hash_password(data_to_change['password'])
            token = check_auth(session)
            user = get_item(session, User, user_id)
            if token.user_id != user.id:
                raise HttpError(403, "user has no access")
            user = patch_item(session, user, **data_to_change)
            return jsonify({
                "id": user.id,
                "email": user.email
            })

    def delete(self, user_id: int):
        with Session() as session:
            user = get_item(session, User, user_id)
            token = check_auth(session)
            if token.user_id != user.id:
                raise HttpError(403, "user has no access")
            delete_item(session, user)
            return {"deleted": True}


class AdsView(MethodView):

    def get(self, ads_id: int):
        with Session() as session:
            ads = get_item(session, Ads, ads_id)
            return jsonify({
                'id': ads.id,
                'title': ads.title,
                'description': ads.description,
                'registration_time': ads.registration_time.isoformat(),
                'owner_id': ads.owner_id
            })

    def post(self):
        json_data = validate(CreateItem, request.json)
        with Session() as session:
            new_ads = Ads(**json_data)
            token = check_auth(session)
            if token.user_id != new_ads.owner_id:
                raise HttpError(403, "You must be logged in to post an ad.")
            session.add(new_ads)
            try:
                session.commit()
            except IntegrityError:
                raise HttpError(409, 'Ad with the same header or description already exists!')
            return jsonify({
                'id': new_ads.id,
                'title': new_ads.title,
                'description': new_ads.description,
                'registration_time': new_ads.registration_time.isoformat(),
                'owner_id': new_ads.owner_id
            })

    def patch(self, ads_id: int):
        json_data = validate(AdsData, request.json)
        with Session() as session:
            token = check_auth(session)
            ads = get_item(session, Ads, ads_id)
            if token.user_id != ads.owner_id:
                raise HttpError(403, "You need to be owner to chage the add")
            for field, value in json_data.items():
                setattr(ads, field, value)
            session.add(ads)
            session.commit()
            return jsonify({
                'status': 'fields successfully changed'
            })

    def delete(self, ads_id: int):
        with Session() as session:
            token = check_auth(session)
            ads = get_item(ads_id, session)
            if token.user_id != ads.owner_id:
                raise HttpError(403, "You need to be owner to chage the add")
            session.delete(ads)
            session.commit()
            return jsonify({
                'status': f'Ad with id {ads_id} is deleted'
            })
