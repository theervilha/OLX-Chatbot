from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By

from datetime import datetime, timedelta
import locale
locale.setlocale(locale.LC_TIME, "pt")

class SeleniumOLX:
    product_l = (By.CSS_SELECTOR, ".sc-12rk7z2-1.huFwya")
    title_l = (By.CSS_SELECTOR, 'h2')
    img_l = (By.CSS_SELECTOR, 'img')
    price_l = (By.CSS_SELECTOR, '.sc-1kn4z61-1.dGMPPn span')
    date_l = (By.CSS_SELECTOR, '.sc-11h4wdr-0.javKJU')

    def __init__(self):
        self.driver = webdriver.Chrome(ChromeDriverManager().install())

    def search_in_url(self, url):
        self.driver.get(url)
    
    def get_products_in_page(self):
        for self.element in self.driver.find_elements(*self.product_l):
            yield {
                'product_link': self.element.get_attribute('href'),
                'title': self.element.find_element(*self.title_l).text,
                'img': self.element.find_element(*self.img_l).get_attribute('src'),
                'price': self.get_price(),
                'date': self.get_date(),
            }

    def get_price(self):
        price = self.element.find_element(*self.price_l).text[3:].replace('.', '')
        return float(price) if price != '' else price

    def get_date(self):
        self.date = self.element.find_element(*self.date_l).text
        self.clean_date()
        return self.date

    def clean_date(self):
        if "Hoje" in self.date:
            self.date = datetime.strptime(datetime.now().strftime('%d %b') + self.date[4:], '%d %b, %H:%M')
        elif "Ontem" in self.date:
            yesterday = datetime.now() - timedelta(1)
            self.date = datetime.strptime(yesterday.strftime('%d %b') + self.date[5:], '%d %b, %H:%M')
        else:
            self.date = datetime.strptime(self.date, '%d %b, %H:%M')

