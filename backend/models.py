from database import db

class Player(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    team = db.Column(db.String(100), nullable=False)
    position = db.Column(db.String(50))
    games = db.Column(db.Integer)
    minutes = db.Column(db.Float)
    points = db.Column(db.Float)
    rebounds = db.Column(db.Float)
    assists = db.Column(db.Float)
    steals = db.Column(db.Float)
    blocks = db.Column(db.Float)
    threes_made = db.Column(db.Float)
    fg_percentage = db.Column(db.Float)
    ft_percentage = db.Column(db.Float)
    turnovers = db.Column(db.Float)
    z_points = db.Column(db.Float)
    z_rebounds = db.Column(db.Float)
    z_assists = db.Column(db.Float)
    z_steals = db.Column(db.Float)
    z_blocks = db.Column(db.Float)
    z_ft_percentage = db.Column(db.Float)
    z_fg_percentage = db.Column(db.Float)
    z_threes_made = db.Column(db.Float)
    z_turnovers = db.Column(db.Float)

    def __repr__(self):
        return f'<Player {self.name}>'