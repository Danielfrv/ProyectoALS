
import flask
import flask_login
import sirope
from flask_login import login_manager

from model.gamedto import GameDto
from model.userdto import UserDto


def create_app():
    lmanager = login_manager.LoginManager()
    fapp = flask.Flask(__name__)
    syrp = sirope.Sirope()

    fapp.config.from_json("config.json")
    lmanager.init_app(fapp)
    return fapp, lmanager, syrp


app, lm, srp = create_app()


@lm.user_loader
def user_loader(email):
    return UserDto.find(srp, email)


@app.route('/')
def get_index():
    usr = UserDto.current_user()

    sust = {
        "usr": usr,
    }

    return flask.render_template("index.html", **sust)


@app.route('/main')
def get_main():
    usr = UserDto.current_user()
    messages_list = list(sirope.Sirope().load_last(GameDto, 9))

    sust = {
        "usr": usr,
        "messages_list": messages_list,
    }

    return flask.render_template("main.html", **sust)


@app.route('/login', methods=['POST'])
def login():
    email_txt = flask.request.form.get("edEmail")
    password_txt = flask.request.form.get("edPassword")

    if not email_txt:
        usr = UserDto.current_user()

        if not usr:
            flask.flash("Debes iniciar sesión.")
            return flask.redirect("/")
    else:
        usr = UserDto.find(srp, email_txt)
        if not password_txt:
            flask.flash("Introduce una contraseña.")
            return flask.redirect("/")

        if not usr:
            usr = UserDto(email_txt, password_txt)
            srp.save(usr)
        elif not usr.chk_password(password_txt):
            flask.flash("La contraseña no es correcta.")
            return flask.redirect("/")

        flask_login.login_user(usr)

    srp.save(usr)
    return flask.redirect("/main")


@app.route("/save_message", methods=["POST"])
def save_message():
    name_txt = flask.request.form.get("edName")
    gender_txt = flask.request.form.get("edGender")
    message_txt = flask.request.form.get("edMessage")
    usr = UserDto.current_user()

    if not message_txt:
        flask.flash("Introduce un mensaje.")
        return flask.redirect("/publish_review")

    if not name_txt:
        flask.flash("Introduce el nombre del juego.")
        return flask.redirect("/publish_review")

    if not gender_txt:
        flask.flash("Introduce el género del juego")
        return flask.redirect("/publish_review")

    msg_oid = srp.save(GameDto(f"{usr.email} comentó: {message_txt}", name_txt, gender_txt))
    usr.add_message_oid(msg_oid)

    return flask.redirect("/main")


@app.route("/publish_review")
def publish_review():
    usr = UserDto.current_user()

    sust = {
        "usr": usr,
    }

    return flask.render_template('publish.html', **sust)


@app.route('/logout')
def logout():
    flask_login.logout_user()
    flask.flash("Has cerrado sesión.")
    return flask.redirect("/")


@lm.unauthorized_handler
def unauthorized_handler():
    flask.flash("No autorizado.")
    return flask.redirect("/")


if __name__ == '__main__':
    app.run()
