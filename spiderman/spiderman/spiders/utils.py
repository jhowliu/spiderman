from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait

# return the cookies string

spider = webdriver.Remote("http://192.168.10.16:4445/wd/hub", desired_capabilities=webdriver.DesiredCapabilities.CHROME)
worker = webdriver.Remote("http://192.168.10.16:4446/wd/hub", desired_capabilities=webdriver.DesiredCapabilities.CHROME)
