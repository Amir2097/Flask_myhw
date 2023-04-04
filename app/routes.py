from errors import HttpError, error_handler
from app import create_app
from views import AdsView, register, login, UserView

app = create_app()

app.add_url_rule("/register/", view_func=register, methods=["POST"])
app.add_url_rule("/login/", view_func=login, methods=["POST"])
app.add_url_rule(
    "/users/<int:user_id>/",
    view_func=UserView.as_view("user"),
    methods=["GET", "PATCH", "DELETE"],
)
app.add_url_rule(
    '/ads/<int:ads_id>/',
    view_func=AdsView.as_view('ads_existed'),
    methods=['GET', 'PATCH', 'DELETE', ]
)
app.add_url_rule(
    '/ads/',
    view_func=AdsView.as_view('ads_new'),
    methods=['POST']
)

app.errorhandler(HttpError)(error_handler)

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000)
