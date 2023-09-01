import smtplib
import requests
import secrets
from bs4 import BeautifulSoup

URL = ("https://www.amazon.com/LEGO-Star-Wars-Mustafar-Skywalker/dp/B07WFHWSLR/ref=sr_1_1?keywords=anakin+vs+obi+wan"
       "+lego&sr=8-1")
HEADERS = {
       "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                     "Chrome/116.0.0.0 Safari/537.36",
       "Accept-Language": "en-US,en;q=0.5"
}
LOWEST_PRICE: float = 50.25
email = secrets.EMAIL
password = secrets.PASSWORD

response = requests.get(URL, headers=HEADERS)
content = response.text
soup = BeautifulSoup(content, "lxml")
price_tag = soup.find(name="span", class_="a-offscreen").get_text()
product_name = soup.find(name="span", id="productTitle",
                         class_="a-size-large product-title-word-break").get_text().strip()
price = float(price_tag[1:])

if price < LOWEST_PRICE:
    with smtplib.SMTP("smtp.gmail.com") as connection:
        connection.starttls()
        connection.login(user=email, password=password)
        connection.sendmail(from_addr=email,
                            to_addrs=email,
                            msg=f"Subject:Amazon Deal Alert!\n\n{product_name} is now ${price}!\n{URL}\n\n"
                                f"Save yourself ${LOWEST_PRICE-price}!")
