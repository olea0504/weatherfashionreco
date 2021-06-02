from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user
import os
import requests


auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                flash('Logged in successfully!', category='success')
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            else:
                flash('Incorrect password, try again.', category='error')
        else:
            flash('Email does not exist.', category='error')

    return render_template("login.html", user=current_user)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))


@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        email = request.form.get('email')
        first_name = request.form.get('firstName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        user = User.query.filter_by(email=email).first()
        if user:
            flash('Email already exists.', category='error')
        elif len(email) < 4:
            flash('Email must be greater than 3 characters.', category='error')
        elif len(first_name) < 2:
            flash('First name must be greater than 1 character.', category='error')
        elif password1 != password2:
            flash('Passwords don\'t match.', category='error')
        elif len(password1) < 7:
            flash('Password must be at least 7 characters.', category='error')
        else:
            new_user = User(email=email, first_name=first_name, password=generate_password_hash(
                password1, method='sha256'))
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            flash('Account created!', category='success')
            return redirect(url_for('views.home'))

    return render_template("sign_up.html", user=current_user)

# @auth.route("/")
# def index():
#     return render_template("index.html")


@auth.route('/city', methods=["POST", "GET"])
def city():
    if request.method == "POST":
        cityname = request.form["city"]
        api_key = 'd90d601c5aaea292dacedef00010fd11'

        base_url = "http://api.openweathermap.org/data/2.5/weather?"

        complete_url = base_url + "q=" + cityname + "&appid=" + api_key

        response = requests.get(complete_url)
        x = response.json()
    
        if x["cod"] != "404":
            w = x["sys"]
            cityTitle=x["name"]
            country = w["country"]
            y = x["main"]
            currentTemperature = y["temp"]
            feels_like_f = y["feels_like"]
            temp_min_f = y["temp_min"]
            temp_max_f = y["temp_max"]
            feels_like = round(feels_like_f - 273.15)
            temp_min = round(temp_min_f - 273.15)
            temp_max = round(temp_max_f - 273.15)
            temp_range = temp_max-temp_min
            current_pressure = y["pressure"]
            current_humidiy = y["humidity"]
            test=0
            z = x["weather"]
            weather_description = z[0]["description"]
            Temperature = str(round(currentTemperature - 273.15))
            AtmosphericPressure = str(current_pressure)
            Humidity = str(current_humidiy)
            Description = str(weather_description)
            return render_template("cityResult.html", x =x, 
                                    user=current_user, Temperature=Temperature, 
                                    AtmosphericPressure=AtmosphericPressure, 
                                    Humidity=Humidity, Description=Description,
                                    cityTitle=cityTitle, country=country, feels_like=feels_like,
                                    temp_min=temp_min, temp_max=temp_max, temp_range=temp_range, test=test)
                # " Temperature : " + str(currentTemperature - 273.15) + u"\N{DEGREE SIGN}" + "C" + "<br>" +
                # "Atmospheric pressure : " + str(current_pressure) + " hPa" + "<br>" +
                # "Humidity : " + str(current_humidiy) + "%" + "<br>" +
                # "Description : " + str(weather_description)
            
        else:
            return "City Not Found"
    else:
        return render_template("city.html", user=current_user)


@auth.route('/cityResult.html', methods=['GET', 'POST'])
@login_required
def cityResult():
    if request.method == 'POST':
        temperature = Temperature
        info = request.form['info']

        # if len(note) < 1:
        #     flash('Note is too short!', category='error')
        # else:
        if true:
            new_info = Note(data=info, user_id=current_user.id)
            db.session.add(new_info)
            db.session.commit()
            flash('info added!', category='success')

    return render_template("home.html", user=current_user)