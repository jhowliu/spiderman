import re
from selenium import webdriver


def find_by_class_name(soup, tag, class_name):
    raw = soup.find(tag, class_=class_name)

    if raw is None:
        print("there is no class name: %s" % class_name)
        return None

    return raw

def find_by_css(soup, css_pattern):
    raw = soup.select(css_pattern)

    if not len(raw):
        print("failed to find css pattern: %s" % css_pattern)
        return None

    return raw

target = re.compile('(vpadn-sd=([0-9]+))')

def generate_cookies(url):
    driver = webdriver.Remote("http://192.168.10.16:4444/wd/hub", webdriver.DesiredCapabilities.CHROME)
    driver.get(url)

    cookies = driver.get_cookies()

    key_pairs = []
    for cookie in cookies:
        key_pairs.append("%s=%s" % (cookie['name'], cookie['value']))

    driver.close()
    return ";".join(key_pairs)


