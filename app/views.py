from models import Session, Ads
from flask import jsonify, request
from flask.views import MethodView
from crud import get_item


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
        json_data = request.json
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