import time

from selenium import webdriver

# return the cookies string

class Worker(object):

    def __init__(self, port):
        self._url = '';
        target = "http://192.168.10.16:%s/wd/hub" % port
        self.worker = webdriver.Remote(target, desired_capabilities=webdriver.DesiredCapabilities.CHROME)

    @property
    def url(self):
        """ GETTER """
        return self._url

    @url.setter
    def url(self, value):
        """ SETTER """
        self._url = value

    def execute_script(self, script, implicit_waiting=0.5):
        result = self.worker.execute_script(script)
        time.sleep(implicit_waiting)
        return result

    def get(self, url, implicit_waiting=0.5):
        self.url = url
        self.worker.get(url)
        time.sleep(implicit_waiting)

        return True
