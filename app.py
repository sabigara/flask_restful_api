from app import create_app, db
from app.models import User, Client, Token

app = create_app()

@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'Client': Client, 'Token': Token}


