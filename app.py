from ext import app
from routes import main, register_page, login_page, logout, NBA_games, jersey_view, players_stats, add_jersey, edit_product, delete_product, profile, rate_product, buy_item, view_news, edit_player_stats, championships, standing, edit_standing, edit_westernteam

app.run(debug=True, host="0.0.0.0")
