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

    def test_basic_homepage_functionality(self):
        self.browser.get(self.live_server_url)

        # As a visitor - I want to see a short description of what this
        # app does/can do (on the splash page)
        home_body = self.browser.body
        self.assertIn('HAUS is an open-source Home Automation User Service',
                      home_body)

        # as a visitor, I'd like to be invited to create an account
        self.assertIn('Register', home_body)

        self.fail('Add more tests!')

        # as a visitor, i'd like to create an account


class MemberTests(LiveServerTestCase):
    def setUp(self):
        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(3)

    def tearDown(self):
        self.browser.quit()

    def test_member_login(self):
        # as a member, I'd like to log in to a secure account
        ## This may get changed around for actual homepage functionality
        username_box = self.browser.find_element_by_id('username')
        password_box = self.browser.find_element_by_id('password')

        username_box.send_keys('admin')
        password_box.send_keys('admin')
        self.browser.find_element_by_id('login').click()

        self.wait_for_element_with_id('logout')
        navbar = self.browser.find_element_by_css_selector('.navbar')
        self.assertIn('admin', navbar.text)

    def test_dashboard_functionality(self):
        pass
        # As a member, I'd like to be able to add a device to my dashboard

        # as a memeber, i'd like to customize which of my devices
        # I see on my dashboard
