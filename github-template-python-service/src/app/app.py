import pandas as pd
import folium
from flask import Flask, render_template
import os

n = 15
corona_df = pd.read_csv('src/static/dataset.csv')
by_country = corona_df.groupby('Country_Region').sum()[['Confirmed', 'Deaths', 'Recovered', 'Active']]
cdf = by_country.nlargest(n, 'Confirmed')[['Confirmed']]


def find_top_confirmed(n=15):
    corona_df = pd.read_csv('src/static/dataset.csv')
    by_country = corona_df.groupby('Country_Region').sum()[
        ['Confirmed', 'Deaths', 'Recovered', 'Active']
    ]
    cdf = by_country.nlargest(n, 'Confirmed')[['Confirmed']]
    return cdf


corona_df = pd.read_csv('src/static/dataset.csv')
corona_df = corona_df.dropna()
m = folium.Map(
    location=[34.223334, -82.461707],
    tiles='Stamen Toner',
    attr='Map tiles by Stamen Design, under CC BY 3.0. Data by OpenStreetMap, under ODbL',
    zoom_start=8
)


def circle_maker(x):
    folium.Circle(
        location=[x[0], x[1]],
        radius=float(x[2])*10,
        color="red",
        popup='{}\n confirmed cases:{}'.format(x[3], x[2])
    ).add_to(m)


corona_df[['Lat', 'Long_', 'Confirmed', 'Combined_Key']].apply(
    lambda x: circle_maker(x), axis=1
)
html_map = m._repr_html_()

app = Flask(__name__, template_folder='../templates')


@app.route('/')
def home():
    return render_template("home.html", table=cdf, cmap=html_map)


if __name__ == "__main__":
    debug_mode = os.getenv('FLASK_DEBUG', 'False').lower() in ['true', '1', 't']
    app.run(host="0.0.0.0", port=8080)
