from ext import app, db
from models import Jersey, Tickets, User, Player, News, Championships, EasternTeams, WesternTeams, Games
from variables import jerseys, tickets, users, players, newses, championships, eastern_teams, western_teams, games

with app.app_context():
    db.drop_all()
    db.create_all()

    for jersey in jerseys:
        new_jersey = Jersey(name=jersey["name"], price=jersey["price"], image=jersey["image"])
        new_jersey.create()

    for ticket in tickets:
        new_ticket = Tickets(name=ticket["game_name"], description=ticket["game_description"],
                             price=ticket["game_price"], image=ticket["game_image"])
        new_ticket.create()

    for user in users.values():
        new_user = User(username=user["fullname"], age=user["age"], password="name1234", role=user["role"])
        new_user.create()

    for player in players:
        new_player = Player(player=player["player"], player_photo=player["player_photo"], team=player["team"], gp=player["gp"], min=player["min"],
                            pts=player["pts"],
                            fgm=player["fgm"], fga=player["fga"], fg_pct=player["fg_pct"], three_pm=player["three_pm"],
                            three_pa=player["three_pa"],
                            three_pct=player["three_pct"], ftm=player["ftm"], fta=player["fta"],
                            ft_pct=player["ft_pct"],
                            oreb=player["oreb"], dreb=player["dreb"], reb=player["reb"], ast=player["ast"],
                            stl=player["stl"], blk=player["blk"],
                            tov=player["tov"], eff=player["eff"])

        new_player.create()
    for news in newses:
        new_news = News(
            title=news["title"],
            author=news["author"],
            date=news["date"],
            image=news["image"],
            news=news["news"],
            link=news["link"]
        )
        new_news.create()

    for championship in championships:
        new_championship = Championships(
            name=championship["name"],
            country=championship["country"],
            official_site=championship["official_site"],
            logo=championship["logo"]
        )
        new_championship.create()

    for eastern_team in eastern_teams:
        new_eastern_team = EasternTeams(
            name=eastern_team["name"],
            image=eastern_team["image"],
            W=eastern_team["W"],
            L=eastern_team["L"],
            win_percentage=eastern_team["win_percentage"],
            GB=eastern_team["GB"],
            CONF=eastern_team["CONF"],
            DIV=eastern_team["DIV"],
            HOME=eastern_team["HOME"],
            ROAD=eastern_team["ROAD"],
            Neutral=eastern_team["Neutral"],
            OT=eastern_team["OT"],
            LAST10=eastern_team["LAST10"],
            STREAK=eastern_team["STREAK"]
        )
        new_eastern_team.create()

    for western_team in western_teams:
        new_western_team = WesternTeams(
            name=western_team["name"],
            image=western_team["image"],
            W=western_team["W"],
            L=western_team["L"],
            win_percentage=western_team["win_percentage"],
            GB=western_team["GB"],
            CONF=western_team["CONF"],
            DIV=western_team["DIV"],
            HOME=western_team["HOME"],
            ROAD=western_team["ROAD"],
            Neutral=western_team["Neutral"],
            OT=western_team["OT"],
            LAST10=western_team["LAST10"],
            STREAK=western_team["STREAK"]
        )
        new_western_team.create()


    for game in games:
        new_game = Games(
            team_1=game["team_1"],
            team_1_img=game["team_1_img"],
            team_2=game["team_2"],
            team_2_img=game["team_2_img"],
            final_score=game["final_score"],
        )
        new_game.create()
