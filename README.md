# flask_restful_api

## Instration
1. Clone the repository.
```bash
git clone https://github.com/sabigara/flask_restful_api.git
cd flask_restful_api
```
2. Create venv and pip-install required libaries.
```bash
python3 -m venv venv
source ./venv/bin/activate
pip install -r requirements.txt
```
3. Migrate models.
```bash
flask db init
flask db migrate
flask db upgrade

# if flask command refers to the global one, and not one in the venv,
# just call explicitly:
./venv/bin/flask db init
```
4. Run flask server.
```bash
flask run
```

## Using APIs
1. Create user.
```bash
curl localhost:5000/users -F username=user1 -F email=user1@gmail.com -F password=user1
```
2. Register the created `user1` as API's client.
```bash
curl localhost:5000/clients -F client_name=user1 -F grant_type=password -F token_endpoint_auth_method=client_secret_basic
```
3. Issue token for `user1`
```bash
curl -u <client_id>:<client_secret> localhost:5000/token -F grant_type=password -F username=user1 -F password=user1
```
4. Get user info tied to the token via `/users` endpoint.
```bash
curl -H "Authorization: Bearer <access_token>" localhost:5000/users
```