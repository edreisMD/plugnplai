# This file is example for the handling the login with oauth authentication.
# it has two endpoints 
# 1. /login : it is used for redirecting the user to a aunthentication_url(you can get this deatils from the mantifest file) of particular plugin.
# 2. /callback : it is called automatically on success or failure response of the /login endpoint.
# requirements.
# pip install requests_oauthlib
# run this file first.


import json
from urllib.parse import urljoin

from requests_oauthlib import OAuth2Session
from flask import Flask, request, session, redirect
import ssl

redirect_uri = 'https://localhost:5000/callback'
app = Flask(__name__)
app.secret_key = "qazwsx"
# Update the SSL context with the certificate and key file paths

context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
# add the certificate and key from the pyopenssl or generate it.
context.load_cert_chain(certfile='certificate.crt', keyfile='private.key')
client_id = "client_id"
client_secret = "client_secret"
client_url = "client_url" 
token_url = "authorization_token_url"

@app.route('/login', methods=["GET"])
def login():
    try:
        global oauth
        oauth = OAuth2Session(client_id, redirect_uri=redirect_uri)
        authorization_url, state = oauth.authorization_url(client_url)
        session['oauth_state'] = state
        return redirect(authorization_url)
    except Exception as e:
        print(e)


@app.route('/callback')
def callback():
    if 'error' in request.args:
        return 'Error: ' + request.args['error']

    token = oauth.fetch_token(
        token_url,
        client_secret=client_secret,
        code=request.args.get("code", "")
    )

    return token


if __name__ == '__main__':
    app.run(debug=True, ssl_context=context)
