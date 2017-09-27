import re

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
