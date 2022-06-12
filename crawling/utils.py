from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait

def remove_space(text):
    return ' '.join(text.split())

def start_webdriver():
    options = webdriver.ChromeOptions()
    options.add_argument("window-size=1000,1000")
    options.add_argument("no-sandbox")
    chrome = webdriver.Chrome("chromedriver.exe", options=options)
    wait = WebDriverWait(chrome, 5)
    return chrome, wait
