from flask import Flask, render_template, request, url_for, redirect
from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SubmitField, validators, URLField
from wtforms.validators import DataRequired
from flask_bootstrap import Bootstrap
import os
import csv

app = Flask(__name__)
key = os.urandom(20)
app.secret_key = key
Bootstrap(app)


@app.route("/cafes")
def cafes():
    with open("cafe-data.csv", encoding="utf-8") as data:
        csv_content = list(csv.reader(data))
        header = csv_content[0]
        cafes_detail = csv_content[1:]
        column_length = len(header)
    return render_template("cafes.html", table_header=header, table_detail=cafes_detail, column_length=column_length)


class AddCafeForm(FlaskForm):
    cafe_name = StringField(label="Cafe Name", validators=[validators.DataRequired()])
    location = URLField(label="Location",
                        validators=[validators.DataRequired(message="Enter a valid URL")],
                        render_kw={'placeholder': 'Ex: https://goo.gl/maps/wahZGrq1tw9mV5Jh7'}
                        )
    open_time = StringField(
        render_kw={'placeholder': 'Valid Format is 12:00 AM/PM'},
        validators=[validators.DataRequired()]
    )
    close_time = StringField(
        render_kw={'placeholder': 'Valid Format is 12:00 AM/PM'},
        validators=[validators.DataRequired()]
    )
    coffee_rating = SelectField(label="Coffee Taste",
                                choices=[("☕☕☕☕☕"), ("☕☕☕☕"), ("☕☕☕"), ("☕☕"), ("☕"), ("✘")]
                                )
    wifi_rating = SelectField(label="Wifi",
                                choices=[("💪💪💪💪💪"), ("💪💪💪💪"), ("💪💪💪"), ("💪💪"), ("💪"), ("✘")]
                              )
    power_rating = SelectField(label="Power",
                                choices=[("🔌🔌🔌🔌🔌"), ("🔌🔌🔌🔌"), ("🔌🔌🔌"), ("🔌🔌"), ("🔌"), ("✘")]
                               )
    submit = SubmitField(label="Submit")


@app.route("/add", methods=['GET', 'POST'])
def add_cafes():
    cafe_rating = AddCafeForm()
    cafe_rating.validate_on_submit()
    if request.method == "POST":
        name_data = cafe_rating.cafe_name.data
        location_date = cafe_rating.location.data
        open_time = cafe_rating.open_time.data
        close_time = cafe_rating.close_time.data
        coffee_rating = cafe_rating.coffee_rating.data
        wifi_rating = cafe_rating.wifi_rating.data
        power_rating = cafe_rating.power_rating.data
        submit_data = cafe_rating.submit.data

        with open("cafe-data.csv", mode="a", encoding="utf-8") as append_data:
            append_data.write(
                f"\n{name_data},{location_date},{open_time},{close_time},{coffee_rating},{wifi_rating},{power_rating}"
            )
        return redirect(url_for("cafes"))
    else:
        return render_template("add-cafe.html", cafe_rating_form=cafe_rating)


@app.route("/")
def homepage():
    return render_template("index.html")


if __name__ == '__main__':
    app.run(debug=True)