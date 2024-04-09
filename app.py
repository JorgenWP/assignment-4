import identity.web
import requests
import os
from flask import Flask, redirect, render_template, request, session, url_for, flash
from flask_session import Session

# The following variables are required for the app to run.

# TODO: Use the Azure portal to register your application and generate client id and secret credentials.
CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")

# TODO: Figure out your authentication authority id.
AUTHORITY = os.getenv("AUTHORITY")

# TODO: generate a secret. Used by flask session for protecting cookies.
SESSION_SECRET = os.getenv("SESSION_SECRET")

# TODO: Figure out what scopes you need to use
# SCOPES = ["User.Read"]
SCOPES = os.getenv("SCOPES", "").split()

# TODO: Figure out the URO where Azure will redirect to after authentication. After deployment, this should
#  be on your server. The URI must match one you have configured in your application registration.
REDIRECT_URI = os.getenv("REDIRECT_URI")

REDIRECT_PATH = "/getAToken"

app = Flask(__name__)

app.config['SECRET_KEY'] = SESSION_SECRET
app.config['SESSION_TYPE'] = 'filesystem'
app.config['TESTING'] = True
app.config['DEBUG'] = True
Session(app)

# The auth object provide methods for interacting with the Microsoft OpenID service.
auth = identity.web.Auth(session=session,
                         authority=AUTHORITY,
                         client_id=CLIENT_ID,
                         client_credential=CLIENT_SECRET)

@app.route("/login")
def login():
    # TODO: Use the auth object to log in.
    response = auth.log_in(
        scopes=SCOPES,
        redirect_uri=url_for("auth_response", _external=True),
        prompt="select_account"
    )
        
    return render_template("login.html", **response)


@app.route(REDIRECT_PATH)
def auth_response():
    # TODO: Use the flask request object and auth object to complete the authentication.
    result = auth.complete_log_in(request.args)
    if "error" in result:
        return render_template("auth_error.html", result=result)
    
    return redirect("/")


@app.route("/logout")
def logout():
    # TODO: Use the auth object to log out and redirect to the home page.
    return redirect(auth.log_out(url_for("index", _external=True)))


@app.route("/")
def index():
    # TODO: use the auth object to get the profile of the logged in user.
    user = auth.get_user()
    if not user:
        return redirect(url_for("login"))
    
    return render_template('index.html', user=user)


@app.route("/profile", methods=["GET"])
def get_profile():

    # TODO: Check that the user is loggen in and add credentials to the http request.
    token = auth.get_token_for_user(SCOPES)
    if "error" in token:
        flash("You must be logged in to view that page.", "error")
        return redirect(url_for("login"))
    
    result = requests.get(
        'https://graph.microsoft.com/v1.0/me',
        headers={'Authorization': 'Bearer ' + token['access_token']}
    )

    return render_template('profile.html', user=result.json(), result=None)

@app.route("/profile", methods=["POST"])
def post_profile():

    # TODO: check that the user is logged in and add credentials to the http request.
    token = auth.get_token_for_user(SCOPES)
    if "error" in token:
        flash("You must be logged in to modify this content.", "error")
        return redirect(url_for("login"))
    
    form_data = request.form.to_dict()
    
    if 'businessPhones' in form_data:
        form_data['businessPhones'] = [form_data['businessPhones']]
        
    result = requests.patch(
        'https://graph.microsoft.com/v1.0/users/' + request.form.get("id"),
        json=form_data,
        headers={'Authorization': 'Bearer ' + token['access_token']}
    )

    # TODO: add credentials to the http request.
    profile = requests.get(
        'https://graph.microsoft.com/v1.0/me',
        headers={'Authorization': 'Bearer ' + token['access_token']}
    )
    return render_template('profile.html',
                           user=profile.json(),
                           result=result)


@app.route("/users")
def get_users():

    # TODO: Check that user is logged in and add credentials to the request.
    token = auth.get_token_for_user(SCOPES)
    if "error" in token:
        flash("You must be logged in to view that page.", "error")
        return redirect(url_for("login"))

    result = requests.get(
        'https://graph.microsoft.com/v1.0/users',
        headers={'Authorization': 'Bearer ' + token['access_token']}
    )
    return render_template('users.html', result=result.json())


if __name__ == "__main__":
    app.run()
