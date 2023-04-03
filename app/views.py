from models import Session, Ads, User
from flask import jsonify, request
from flask.views import MethodView
from crud import get_item
from schema import validate, CreateItem, CreateUser
from hashlib import md5
from errors import HttpError
from sqlalchemy.exc import IntegrityError


class UserView(MethodView):

    def get(self, user_id: int):
        with Session() as session:
            user = get_item(session, User, user_id)
            return jsonify({
                'id': user.id, 'email': user.email
                })

    def post(self):
        json_data = validate(CreateUser, request.json)
        password: str = json_data['password']
        password: bytes = password.encode()
        hashed_password = md5(password).hexdigest()

        with Session() as session:
            new_user = User(**json_data)
            session.add(new_user)
            try:
                session.commit()
            except IntegrityError as er:
                raise HttpError(409, 'user already exists')
            return jsonify({
                'id': new_user.id
            })

    def patch(self, user_id: int):
        json_data = validate(CreateUser, request.json)
        with Session() as session:
            data_to_change = validate(UserData, request.json)
            if 'password' in data_to_change:
                data_to_change['password'] = hash_password(data_to_change['password'])
            token = check_auth(session)
            user = get_user(user_id, session)
            if token.user_id != user.id:
                raise HttpError(403, "You need to log in to chage any data")
            for field, value in data_to_change.items():
                setattr(user, field, value)
            session.add(user)
            session.commit()
        return jsonify({'status': 'fields successfully changed'})

    def delete(self, user_id: int):
        with Session() as session:
            user = get_user(user_id, session)
            token = check_auth(session)
            if token.user_id != user.id:
                raise HttpError(403, "You need to log in to delete")
            session.delete(user)
            session.commit()
            return jsonify({'status': 'User and all his ads are deleted'})




class AdsView(MethodView):

    def get(self, ads_id: int):
        with Session() as session:
            ads = get_item(ads_id, session)
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
            session.add(new_ads)
            session.commit()
            return jsonify({
                'id': new_ads.id
            })

    def patch(self, ads_id: int):
        pass

    def delete(self, ads_id: int):
        pass
