from flask import render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required
from ext import app, db
from forms import JerseyForm, EditJerseyForm, RegisterForm, LoginForm, RatingForm, EditStatsForm, TeamsForm
from models import Jersey, Tickets, User, Player, News, Championships, EasternTeams, WesternTeams, Games
from werkzeug.security import check_password_hash

from os import path
from uuid import uuid4


@app.route('/')
def main():
    games = Games.query.all()
    newses = News.query.all()
    return render_template("main.html", newses=newses, games=games)


@app.route('/register', methods=["GET", "POST"])
def register_page():
    form = RegisterForm()
    if form.validate_on_submit():
        new_user = User(username=form.username.data,
                        password=form.password.data,
                        age=form.age.data,
                        role='user')

        new_user.create()
        return redirect("/")
    return render_template("register.html", form=form)


@app.route('/login', methods=["GET", "POST"])
def login_page():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter(User.username == form.username.data).first()
        if user and check_password_hash(user.password, form.password.data):
            login_user(user)
            return redirect("/")
    print(form.errors)
    return render_template("login.html", form=form)


@app.route("/log_out")
def logout():
    logout_user()
    return redirect("/")


@app.route('/NBA_games')
def NBA_games():
    tickets = Tickets.query.all()
    return render_template("NBA_games_tickets.html", tickets=tickets)


@app.route('/jersey_view')
def jersey_view():
    form = RatingForm()
    jerseys = Jersey.query.all()
    return render_template("jersey.html", jerseys=jerseys, form=form)


@app.route('/players_stats')
def players_stats():
    stats = Player.query.order_by(Player.pts.desc()).all()
    return render_template("players_stats.html", stats=stats)


@app.route('/create_product', methods=["GET", "POST"])
def add_jersey():
    form = JerseyForm()
    if form.validate_on_submit():
        file = form.image.data
        filetype = file.filename.split(".")
        filename = uuid4()
        filepath = path.join(app.root_path, "static", "jerseys", f"{filename}.{filetype[-1]}")
        file.save(filepath)
        new_jersey = Jersey(name=form.name.data,
                            price=form.price.data,
                            image=f"/static/jerseys/{filename}.{filetype[-1]}")

        new_jersey.create()

        return redirect("/jersey_view")

    print(form.errors)
    return render_template("create_product.html", form=form)


@app.route("/edit_jersey/<int:jersey_id>", methods=["GET", "POST"])
@login_required
def edit_product(jersey_id):
    product = Jersey.query.get(jersey_id)

    if not product:
        flash("Jersey not found.", "danger")
        return redirect(url_for("jersey_view"))

    form = EditJerseyForm()
    if request.method == "GET":
        form.name.data = product.name
        form.price.data = product.price

    if form.validate_on_submit():
        file = form.image.data
        if file:
            _, file_extension = path.splitext(file.filename)
            if file_extension.lower() not in [".jpg", ".png", ".jpeg"]:
                flash("Invalid file type. Please upload a JPG or PNG image.", "danger")
                return redirect(request.url)

            filename = f"{uuid4()}{file_extension}"
            filepath = path.join(app.root_path, "static", "jerseys", filename)
            file.save(filepath)

            product.image = f"/static/jerseys/{filename}"

        product.name = form.name.data
        product.price = form.price.data

        db.session.commit()
        flash("Jersey updated successfully!", "success")
        return redirect(url_for("jersey_view"))

    return render_template("edit_jersey.html", form=form)


@app.route("/delete_jersey/<int:jersey_id>")
@login_required
def delete_product(jersey_id):
    product = Jersey.query.get(jersey_id)
    product.delete()

    return redirect("/jersey_view")


@app.route("/profile/<username>")
def profile(username):
    found_user = User.query.filter_by(username=username).first()
    if not found_user:
        return "User not found", 404
    return render_template("profile.html", user=found_user)


@app.route("/rate_product/<int:jersey_id>", methods=["GET", "POST"])
def rate_product(jersey_id):
    jersey = Jersey.query.get(jersey_id)
    if not jersey:
        return render_template("Product not found!")

    form = RatingForm()
    if form.validate_on_submit():
        rating = form.rating.data
        jersey.rating_count = jersey.rating_count or 0
        jersey.rating = jersey.rating or 0
        jersey.rating = (jersey.rating * jersey.rating_count + rating) / (jersey.rating_count + 1)
        jersey.rating_count += 1
        db.session.commit()

        return render_template(
            "rate_product.html", form=form, jersey=jersey, success=True
        )

    return render_template("rate_product.html", form=form, jersey=jersey)


@app.route('/buy/<item_name>')
def buy_item(item_name):
    selected_game = Tickets.query.filter_by(name=item_name).first()
    selected_jersey = Jersey.query.filter_by(name=item_name).first()

    if selected_game:
        return render_template("buy.html", item=selected_game, item_type="game")
    elif selected_jersey:
        return render_template("buy.html", item=selected_jersey, item_type="jersey")
    else:
        return "Item not found"


@app.route('/view_news/<news_title>')
def view_news(news_title):
    selected_news = News.query.filter_by(title=news_title).first()

    if selected_news:
        return render_template("view_news.html", news=selected_news)
    else:
        return "News not found"


@app.route("/edit_player_stats/<int:player_id>", methods=["GET", "POST"])
@login_required
def edit_player_stats(player_id):
    player_stats = Player.query.get(player_id)

    form = EditStatsForm(
        player=player_stats.player,
        team=player_stats.team,
        gp=player_stats.gp,
        pts=player_stats.pts,
        fgm=player_stats.fgm,
        fga=player_stats.fga,
        fg_pct=player_stats.fg_pct,
        three_pm=player_stats.three_pm,
        three_pa=player_stats.three_pa,
        three_pct=player_stats.three_pct,
        ftm=player_stats.ftm,
        fta=player_stats.fta,
        ft_pct=player_stats.ft_pct,
        oreb=player_stats.oreb,
        dreb=player_stats.dreb,
        reb=player_stats.reb,
        ast=player_stats.ast,
        stl=player_stats.stl,
        blk=player_stats.blk,
        tov=player_stats.tov,
        eff=player_stats.eff,
        min=player_stats.min,
    )

    if form.validate_on_submit():
        player_stats.player = form.player.data
        player_stats.team = form.team.data
        player_stats.gp = form.gp.data
        player_stats.pts = form.pts.data
        player_stats.fgm = form.fgm.data
        player_stats.fga = form.fga.data
        player_stats.fg_pct = form.fg_pct.data
        player_stats.three_pm = form.three_pm.data
        player_stats.three_pa = form.three_pa.data
        player_stats.three_pct = form.three_pct.data
        player_stats.ftm = form.ftm.data
        player_stats.fta = form.fta.data
        player_stats.ft_pct = form.ft_pct.data
        player_stats.oreb = form.oreb.data
        player_stats.dreb = form.dreb.data
        player_stats.reb = form.reb.data
        player_stats.ast = form.ast.data
        player_stats.stl = form.stl.data
        player_stats.blk = form.blk.data
        player_stats.tov = form.tov.data
        player_stats.eff = form.eff.data
        player_stats.min = form.min.data

        player_stats.save()
        return redirect(url_for("player_stats"))

    return render_template("edit_player_stats.html", player_stats=player_stats, form=form)


@app.route("/championships")
def championships():
    championships = Championships.query.all()
    return render_template("championships.html", championships=championships)


@app.route("/standing", methods=["GET"])
def standing():
    easternteams = EasternTeams.query.order_by(EasternTeams.win_percentage.desc()).all()
    westernteams = WesternTeams.query.order_by(WesternTeams.win_percentage.desc()).all()
    return render_template("standing.html", easternteams=easternteams, westernteams=westernteams)


@app.route("/edit_standing/<int:easternteams_id>", methods=["GET", "POST"])
@login_required
def edit_standing(easternteams_id):
    easternteams = EasternTeams.query.get(easternteams_id)
    form = TeamsForm(
        name=easternteams.name,
        W=easternteams.W,
        L=easternteams.L,
        win_percentage=easternteams.win_percentage,
        GB=easternteams.GB,
        CONF=easternteams.CONF,
        DIV=easternteams.DIV,
        HOME=easternteams.HOME,
        ROAD=easternteams.ROAD,
        Neutral=easternteams.Neutral,
        OT=easternteams.OT,
        LAST10=easternteams.LAST10,
        STREAK=easternteams.STREAK
    )

    if form.validate_on_submit():
        easternteams.name = form.name.data
        easternteams.W = form.W.data
        easternteams.L = form.L.data
        easternteams.win_percentage = form.win_percentage.data
        easternteams.GB = form.GB.data
        easternteams.CONF = form.CONF.data
        easternteams.DIV = form.DIV.data
        easternteams.HOME = form.HOME.data
        easternteams.ROAD = form.ROAD.data
        easternteams.Neutral = form.Neutral.data
        easternteams.OT = form.OT.data
        easternteams.LAST10 = form.LAST10.data
        easternteams.STREAK = form.STREAK.data

        db.session.commit()
        return redirect(url_for("standing"))

    return render_template("edit_stending.html", form=form)


@app.route("/edit_westernteam/<int:westernteam_id>", methods=["GET", "POST"])
@login_required
def edit_westernteam(westernteam_id):
    westernteam = WesternTeams.query.get(westernteam_id)
    form = TeamsForm(
        name=westernteam.name,
        W=westernteam.W,
        L=westernteam.L,
        win_percentage=westernteam.win_percentage,
        GB=westernteam.GB,
        CONF=westernteam.CONF,
        DIV=westernteam.DIV,
        HOME=westernteam.HOME,
        ROAD=westernteam.ROAD,
        Neutral=westernteam.Neutral,
        OT=westernteam.OT,
        LAST10=westernteam.LAST10,
        STREAK=westernteam.STREAK
    )

    if form.validate_on_submit():
        westernteam.name = form.name.data
        westernteam.W = form.W.data
        westernteam.L = form.L.data
        westernteam.win_percentage = form.win_percentage.data
        westernteam.GB = form.GB.data
        westernteam.CONF = form.CONF.data
        westernteam.DIV = form.DIV.data
        westernteam.HOME = form.HOME.data
        westernteam.ROAD = form.ROAD.data
        westernteam.Neutral = form.Neutral.data
        westernteam.OT = form.OT.data
        westernteam.LAST10 = form.LAST10.data
        westernteam.STREAK = form.STREAK.data

        westernteam.save()
        return redirect(url_for("standing"))

    return render_template("edit_westernteam", form=form)
