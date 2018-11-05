from authlib.flask.oauth2 import AuthorizationServer, ResourceProtector
from authlib.flask.oauth2.sqla import (
    create_query_client_func,
    create_save_token_func,
    create_revocation_endpoint,
)
from authlib.specs.rfc6749 import grants
from app import db
from app.models import Client, Token, User
from authlib.flask.oauth2.sqla import create_bearer_token_validator

class PasswordGrant(grants.ResourceOwnerPasswordCredentialsGrant):
    def authenticate_user(self, username, password):
        user = User.query.filter_by(username=username).first()
        if user:
            if user.check_password(password):
                return user


query_client = create_query_client_func(db.session, Client)
save_token = create_save_token_func(db.session, Token)
BearerTokenValidator = create_bearer_token_validator(db.session, Token)
authorization = AuthorizationServer()
require_oauth = ResourceProtector()
require_oauth.register_token_validator(BearerTokenValidator())

def config_oauth(app):
    authorization.init_app(app, query_client=query_client,
        save_token=save_token)

    authorization.register_grant(PasswordGrant)

    revocation_cls = create_revocation_endpoint(db.session, Token)
    authorization.register_endpoint(revocation_cls)

    # protect resource
    bearer_cls = create_bearer_token_validator(db.session, Token)
    require_oauth.register_token_validator(bearer_cls())