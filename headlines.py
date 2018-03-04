import datetime
from flask import Flask, render_template, request, make_response
import feedparser
import requests
import urllib

app = Flask(__name__)

RSS_FEEDS = {'bbc': 'http://feeds.bbci.co.uk/news/rss.xml',
            'fox': 'http://feeds.foxnews.com/foxnews/latest'}
DEFAULTS = {'publication':'bbc',
            'city':'Los Angeles,US',
            'currency_from': 'GBP',
            'currency_to': 'USD'}

WEATHER_URL="http://api.openweathermap.org/data/2.5/weather?q={}&units=imperial&appid=39f52a3d976f3e5fef30cdf8d5bc0eb1"
CURRENCY_URL = "https://openexchangerates.org/api/latest.json?app_id=cb898aa84fd8472eb7a437258ee4e041"


@app.route("/")
def home() -> "html":
    # Get customized headlines, based on user input or default
    publication = get_value_with_fallback("publication")
    articles = get_news(publication)
    # Get customized weather based on user input or default
    city = get_value_with_fallback('city')
    weather = get_weather(city)
    # Get customized currency based on user input
    currency_from = get_value_with_fallback("currency_from")
    currency_to = get_value_with_fallback('currency_to')
    rate, currencies = get_rate(currency_from, currency_to)
    #print(sorted(currencies))
    # Save cookies and return template
    response = make_response(render_template("home.html", articles=articles,weather=weather, currency_from=currency_from,
                           currency_to=currency_to, rate=rate, currencies=sorted(currencies)))
    expires = datetime.datetime.now() + datetime.timedelta(days=365)
    response.set_cookie("publication", publication, expires=expires)
    response.set_cookie("city", city, expires=expires)
    response.set_cookie("currency_from", currency_from, expires=expires)
    response.set_cookie("currency_to", currency_to, expires=expires)
    return response

def get_value_with_fallback(key) -> "str":
    if request.args.get(key):
        return request.args.get(key)
    if request.cookies.get(key):
        return request.cookies.get(key)
    return DEFAULTS[key]

def get_news(query) -> "html":
    if not query or query.lower() not in RSS_FEEDS:
        publication = "bbc"
    else:
        publication = query.lower()
    feed = feedparser.parse(RSS_FEEDS[publication])
    return feed["entries"]

def get_weather(query):
    query = urllib.parse.quote(query)
    #print(query)
    url = WEATHER_URL.format(query)
    data = requests.get(url)
    parsed = data.json()
    #print(type(parsed))
    #print(parsed)
    if parsed.get("weather"):
        weather = {"description": str(parsed["weather"][0]["description"]).title(), "temperature": parsed["main"]["temp"],
                   "city": parsed["name"], "country": parsed['sys']['country']}
    return weather

def get_rate(frm, to) -> "html":
    all_currency = requests.get(CURRENCY_URL)
    parsed = all_currency.json()
    ex_rates = parsed["rates"]
    #print(ex_rates)
    frm_rate = ex_rates.get(frm.upper())
    to_rate = ex_rates.get(to.upper())
    return (to_rate/frm_rate, ex_rates.keys())




if __name__ == '__main__':
    app.run(port=5000, debug=True)

