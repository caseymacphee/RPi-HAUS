from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from django.test import LiveServerTestCase


class NewVisitorTest(LiveServerTestCase):

    ## special methods which run before and after each test
    def setUp(self):
        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(3)

    def tearDown(self):
        self.browser.quit()

    # As a visitor - I want to see a short description of what this
    # app does/can do (on the splash page)

    # as a visitor, i'd like to create an account

    # as a member, I'd like to log in to a secure account

    # As a member, I'd like to be able to add a device to my dashboard

    # as a memeber, i'd like to customize which of my devices
    # I see on my dashboard