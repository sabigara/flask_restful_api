from flask import request, jsonify, abort
from flask_restful import Resource, fields, marshal
from app import db
from app.main import bp
from werkzeug.security import gen_salt
from authlib.flask.oauth2 import current_token
from app.models import User, Client
from app.main.oauth import authorization, require_oauth


user_fields = {
    'username': fields.String,
    'email': fields.String,
    'password_hash': fields.String,
    'id': fields.String,
}


class UserListAPI(Resource):
    @require_oauth(None)
    def get(self):
        user = current_token.user
        return {'user': marshal(user.serialize, user_fields)}

    def post(self):
        if not request.form or \
            not 'username' in request.form or \
            not 'email' in request.form:
                abort(400)
        all_users = User.query.all()
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        if email in [user.email for user in all_users]:
            abort(409)
        user = User(username=username, email=email)
        user.hash_password(password)
        db.session.add(user)
        db.session.commit()
        return jsonify({'username': user.username})
        

@bp.route('/clients', methods=(['POST']))
def register_client():
    client_name = request.form['client_name']
    grant_type = request.form['grant_type']
    token_endpoint_auth_method = request.form['token_endpoint_auth_method']
    client = Client(
        client_name=client_name, grant_type=grant_type,
        token_endpoint_auth_method=token_endpoint_auth_method)
    user = User.query.filter_by(username=client_name).first()
    if not user:
        return None
    client.user_id = user.id
    client.client_id = gen_salt(24)
    if client.token_endpoint_auth_method == 'none':
        client.client_secret = ''
    else:
        client.client_secret = gen_salt(48)
    db.session.add(client)
    db.session.commit()
    return jsonify({'client_id': client.client_id, 'client_secret': client.client_secret})


@bp.route('/token', methods=['POST'])
def get_tokens():
    res = authorization.create_token_response(request)
    return res

