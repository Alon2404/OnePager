import requests
from twilio.rest import Client

STOCK_NAME = "TSLA"
COMPANY_NAME = "Tesla Inc"

# Ich habe alle Key's nicht beigegeben aus Gründen der Sicherheit. Ich weiß, ich könnte das os importieren und
# Environment variables nutzen aber ich denke mir das, was Sie hier sehen, schon ausreicht.
STOCK_ENDPOINT = "https://www.alphavantage.co/query"
STOCK_API_KEY = "Geheim"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"
NEWS_API = "Geheim"
TWILIO_SID = "Geheim"
TWILIO_AUT = "Geheim"

stock_params = {
    "function": "TIME_SERIES_DAILY",
    "symbol": STOCK_NAME,
    "apikey": STOCK_API_KEY,
}

response = requests.get(STOCK_ENDPOINT, params=stock_params)
data = response.json()["Time Series (Daily)"]
print(data)

data_list = [value for (key, value) in data.items()]
print(data_list)

yesterday_data = data_list[0]
yesterday_closing_price = yesterday_data["4. close"]
print(yesterday_closing_price)

day_before_yesterday_data = data_list[1]
day_before_yesterday_closing_price = day_before_yesterday_data["4. close"]
print(day_before_yesterday_closing_price)

difference = float(yesterday_closing_price) - float(day_before_yesterday_closing_price)
print(difference)

diff_percent = (difference / float(yesterday_closing_price))*100
print(diff_percent)
print("------------------------------------------------")

if diff_percent > 0:
    print("Get News")
    # Anstelle von "Get News" soll es mir eine Nachricht senden. Ich habe Get News dennoch beibelassen da es zum Bug Testing hilfreich ist.

    news_params = {
        "apiKey": NEWS_API,
        "qInTitle": COMPANY_NAME,
    }

    news_response = requests.get(NEWS_ENDPOINT, params=news_params)
    articles = news_response.json()["articles"]
    print(news_response.json())

    three_articles = articles[:3]
    print(three_articles)

    # Eine Liste der ersten 3 Artikel generieren
    formatted_articles = [(f"{STOCK_NAME}: {diff_percent}%\nHeadline: {article['title']}. \n"
                           f"Brief: {article['description']}") for article in three_articles]
    client = Client(TWILIO_SID, TWILIO_AUT)

    for article in formatted_articles:
        message = client.messages.create(
            from_='Geheim',
            body=article,
            to='+436769651539',
        )

    print(message.sid)
