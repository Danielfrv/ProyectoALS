
import os
import flask
import flask_login
import sirope
from flask_login import login_manager
from flask import *
from model.gamedto import GameDto
from model.userdto import UserDto
from model.reviewdto import ReviewDto


def create_app():
    lmanager = login_manager.LoginManager()
    fapp = flask.Flask(__name__)
    syrp = sirope.Sirope()

    fapp.config.from_json("config.json")
    lmanager.init_app(fapp)
    return fapp, lmanager, syrp


app, lm, srp = create_app()
app.config['UPLOAD_FOLDER'] = "static/images"


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
    games_list = list(sirope.Sirope().load_last(GameDto, 18))

    sust = {
        "usr": usr,
        "games_list": games_list,
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


@app.route("/save_game", methods=["POST"])
def save_game():
    name_txt = flask.request.form.get("edName")
    gender_txt = flask.request.form.get("edGender")
    description_txt = flask.request.form.get("edDescription")
    image = request.files['edImage']
    image_txt = image.filename

    if not name_txt:
        flask.flash("Introduce el nombre del juego.")
        return flask.redirect("/create_game")

    if not gender_txt:
        flask.flash("Introduce el género del juego")
        return flask.redirect("/create_game")

    if not image:
        flask.flash("Introduce una imagen")
        return flask.redirect("/create_game")
    else:
        path = os.path.join(app.config['UPLOAD_FOLDER'], image.filename)
        image.save(path)

    if not description_txt:
        flask.flash("Introduce una descripcion")
        return flask.redirect("/create_game")

    srp.save(GameDto(name_txt, gender_txt, image_txt, description_txt))
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

    msg_oid = srp.save(ReviewDto(name_txt, f"{usr.email}: {message_txt}"))
    usr.add_message_oid(msg_oid)

    return flask.redirect("/view_reviews/"+name_txt+"/"+gender_txt)


@app.route("/publish_review/<name>/<gender>", methods=["GET"])
def publish_review(name, gender):
    usr = UserDto.current_user()
    name = name
    gender = gender

    sust = {
        "usr": usr,
        "name": name,
        "gender": gender
    }

    return flask.render_template('publish.html', **sust)


@app.route("/view_reviews/<name>/<gender>", methods=["GET"])
def view_reviews(name, gender):
    usr = UserDto.current_user()
    name_txt = name
    gender_txt = gender
    game = list(sirope.Sirope().filter(GameDto, lambda u: u.name == name_txt, 1))
    messages_list = list(sirope.Sirope().filter(ReviewDto, lambda u: u.game == name_txt, 18))

    sust = {
        "usr": usr,
        "name": name_txt,
        "gender": gender_txt,
        "messages_list": messages_list,
        "game": game,
    }

    return flask.render_template('reviews.html', **sust)


@app.route("/create_game")
def create_game():
    usr = UserDto.current_user()

    sust = {
        "usr": usr,
    }

    return flask.render_template('game.html', **sust)


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
