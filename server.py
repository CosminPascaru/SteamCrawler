from flask import Flask, render_template, request
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, BooleanField, IntegerField
from wtforms.validators import InputRequired, NumberRange
from flask_wtf.csrf import CSRFProtect
import secrets
import crawler

app = Flask(__name__)
app.config['SECRET_KEY'] = secrets.token_hex(16)

csrf = CSRFProtect(app)

class Form(FlaskForm):
    games_number = IntegerField('Number of games', validators=[InputRequired(), NumberRange(min=1, max=100)], default=10)
    checkbox_indie = BooleanField("indie")
    checkbox_singleplayer = BooleanField("singleplayer")
    checkbox_adventure = BooleanField("adventure")
    checkbox_action = BooleanField("action")
    checkbox_2d = BooleanField("2d")
    checkbox_pixel = BooleanField("pixel")
    checkbox_platformer = BooleanField("platformer")
    checkbox_casual = BooleanField("casual")
    checkbox_rpg = BooleanField("rpg")
    checkbox_storyrich = BooleanField("storyrich")
    checkbox_strategy = BooleanField("strategy")
    checkbox_simulation = BooleanField("simulation")
    checkbox_firstperson = BooleanField("firstperson")
    checkbox_shooter = BooleanField("shooter")
    checkbox_pvp = BooleanField("pvp")
    checkbox_coop = BooleanField("coop")
    checkbox_achievement = BooleanField("achievement")
    checkbox_workshop = BooleanField("workshop")
    checkbox_cloud = BooleanField("cloud")
    checkbox_windows = BooleanField("windows")
    checkbox_linux = BooleanField("linux")

    submit = SubmitField('Submit')

@app.route('/')
def index():
    return render_template('/index.html')

@app.route('/form', methods=['GET', 'POST'])
def form():
    form = Form()

    if form.validate_on_submit():
        games_number = form.games_number.data

        tag_list = []
        tag_list.append(form.checkbox_indie.data)
        tag_list.append(form.checkbox_singleplayer.data)
        tag_list.append(form.checkbox_adventure.data)
        tag_list.append(form.checkbox_action.data)
        tag_list.append(form.checkbox_2d.data)
        tag_list.append(form.checkbox_pixel.data)
        tag_list.append(form.checkbox_platformer.data)
        tag_list.append(form.checkbox_casual.data)    
        tag_list.append(form.checkbox_rpg.data)
        tag_list.append(form.checkbox_storyrich.data)
        tag_list.append(form.checkbox_strategy.data)
        tag_list.append(form.checkbox_simulation.data)
        tag_list.append(form.checkbox_firstperson.data)
        tag_list.append(form.checkbox_shooter.data)
        tag_list.append(form.checkbox_pvp.data)
        tag_list.append(form.checkbox_coop.data)
        
        feature_list = []
        feature_list.append(form.checkbox_achievement)
        feature_list.append(form.checkbox_workshop)
        feature_list.append(form.checkbox_cloud)
        feature_list.append(form.checkbox_windows)
        feature_list.append(form.checkbox_linux)

        parsed_tag_list = crawler.parse_tag_list(tag_list)
        parsed_feature_list = crawler.parse_feature_list(feature_list)

        results = crawler.get_game_urls(parsed_tag_list, parsed_feature_list, games_number)
        
        for game in results:
            crawler.extract_game_data(game)

        return render_template('/results.html', results=results)

    return render_template('/form.html', form=form)

app.run(host='0.0.0.0', port=5000)