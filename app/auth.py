import functools

from flask import (
    Blueprint,
    flash,
    g,
    redirect,
    render_template,
    request,
    session,
    url_for,
    make_response,
)
from app.forms import RegistrationForm, LoginForm

bp = Blueprint("auth", __name__, url_prefix="/auth")


@bp.route("/register", methods=("GET", "POST"))
def register():
    # TODO: Add SSO support for registration and login.
    form = RegistrationForm(request.form)

    if request.method == "POST" and form.validate():
        form.save()

        flash("Registration successful! You can now log in.")

        return redirect(url_for("auth.login"))

    return render_template("register.html", form=form)


@bp.route("/login", methods=("GET", "POST"))
def login():
    form = LoginForm(request.form)

    if request.method == "POST" and form.validate():
        user, token = form.save()

        response = make_response(redirect(url_for("home.home")))

        response.set_cookie("access_token", token["access_token"])
        session["access_token"] = token["access_token"]
        session["user"] = user.as_dict()

        return response

    return render_template("login.html", form=form)


@bp.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("home.home"))


@bp.before_app_request
def load_user():
    g.user = session.get("user")


def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for("auth.login"))

        return view(**kwargs)

    return wrapped_view
