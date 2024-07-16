import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from flask import Flask, request, jsonify, send_from_directory
from database import db
import click
from flask.cli import with_appcontext
from flask_cors import CORS
from models import Player
from dotenv import load_dotenv


app = Flask(__name__, static_folder='../build', static_url_path='')
CORS(app, resources={r"/api/*": {"origins": "*"}})

dotenv_path = os.path.join(os.path.dirname(__file__), '..', '.env')

# Load the environment variables from the specified .env file
load_dotenv(dotenv_path)

# Now you can use os.getenv to get the environment variables
database_url = os.getenv('DATABASE_URL')

app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

@app.route('/api/players', methods=['GET'])
def get_players():
    active_stats = request.args.getlist('stats')  # Example: ['points', 'rebounds', 'assists']
    players = Player.query.all()

    # Calculate total value based on active stats
    for player in players:
        total_value = 0
        if 'PTS' in active_stats:
            total_value += player.z_points
        if 'REB' in active_stats:
            total_value += player.z_rebounds
        if 'AST' in active_stats:
            total_value += player.z_assists
        if 'STL' in active_stats:
            total_value += player.z_steals
        if 'BLK' in active_stats:
            total_value += player.z_blocks
        if '3PM' in active_stats:
            total_value += player.z_threes_made
        if 'FG%' in active_stats:
            total_value += player.z_fg_percentage
        if 'FT%' in active_stats:
            total_value += player.z_ft_percentage
        if 'TO' in active_stats:
            total_value -= player.z_turnovers  # Subtract because it's a negative stat

        player.value = round(total_value, 2)

    sorted_players = sorted(players, key=lambda x: x.value, reverse=True)

    players_data = [
        {
            'id': player.id,
            'name': player.name,
            'team': player.team,
            'position': player.position,
            'games': player.games,
            'minutes': player.minutes,
            'points': player.points,
            'rebounds': player.rebounds,
            'assists': player.assists,
            'steals': player.steals,
            'blocks': player.blocks,
            'threePM': player.threes_made,
            'fgPct': player.fg_percentage,
            'ftPct': player.ft_percentage,
            'turnovers': player.turnovers,
            'value': player.value
        } for player in sorted_players
    ]
    return jsonify(players_data)

@app.route('/')
def serve():
    return send_from_directory(app.static_folder, 'index.html')

@app.cli.command("load-data")
@with_appcontext
def load_data_command():
    from data_preprocessing import load_data
    load_data()
    click.echo("Data loaded successfully.")

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)