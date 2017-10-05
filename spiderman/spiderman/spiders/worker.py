import time
import traceback

from selenium import webdriver

# return the cookies string

class Worker(object):

    def __init__(self, port):
        self._url = '';
        self.target = "http://127.0.0.1:%s/wd/hub" % port
        self.worker = webdriver.Remote(self.target, desired_capabilities=webdriver.DesiredCapabilities.CHROME)

    @property
    def url(self):
        """ GETTER """
        return self._url

    @url.setter
    def url(self, value):
        """ SETTER """
        self._url = value

    def reopen(self):
        self.quit()
        self.worker = webdriver.Remote(self.target, desired_capabilities=webdriver.DesiredCapabilities.CHROME)

    def retries(method):
        def wrapper(*args, **kw):
            retries = 3

            while retries:
                try:
                    result = method(*args, **kw)
                    return result
                except Exception as ex:
                    traceback.print_exc()
                    retries-=1
            return False
        return wrapper

    @retries
    def execute_script(self, script, implicit_waiting=1):
        result = self.worker.execute_script(script)
        time.sleep(implicit_waiting)

        return result

    @retries
    def get(self, url, implicit_waiting=1):
        self.url = url
        self.worker.get(url)
        time.sleep(implicit_waiting)

        return True

    def close(self):
        self.worker.quit()

        return True


