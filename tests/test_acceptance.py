"""
This module contains the acceptance tests for the cbapp.
"""

import unittest
from bs4 import BeautifulSoup
import cbapp

class TestCBAppAccept(unittest.TestCase):
    """ Class of acceptance tests that checks if the templates exist. """
    def setUp(self):
        cbapp.app.config['TESTING'] = True
        self.app = cbapp.app.test_client()

    def test_index_page_h2(self):
        """ Checks if the index page loads correctly. """
        response = self.app.get('/', content_type='html/text')
        soup = BeautifulSoup(response.data, 'html.parser')
        self.assertEqual("Sing, draw, create to your heart's content.",
                         soup.h2.text.strip())

    def test_login_page_loads(self):
        """ Checks if the login page loads correctly. """
        response = self.app.get('/login/', content_type='html/text')
        soup = BeautifulSoup(response.data, 'html.parser')
        self.assertEqual('Login', soup.h2.text)

class TestCBAppAcceptFormsExist(unittest.TestCase):
    """ Class of acceptance tests that checks if the forms exist on certain templates. """
    def setUp(self):
        cbapp.app.config['TESTING'] = True
        self.app = cbapp.app.test_client()

    def test_login_form_exists(self):
        """ Checks that the login form exists. """
        response = self.app.get('/login/', content_type='html/text')
        soup = BeautifulSoup(response.data, 'html.parser')
        self.assertNotEqual(None, soup.form)

    def test_signup_form_exists(self):
        """ Checks that the signup form exists. """
        response = self.app.get('/signup/', content_type='html/text')
        soup = BeautifulSoup(response.data, 'html.parser')
        self.assertNotEqual(None, soup.form)

    def test_create_entry_form_exists(self):
        """ Checks that the create entry form exists. """
        cb = 0
        response = self.app.get('/chorusbattle/{}/entries/create/'.format(cb),
                                content_type='html/text')
        soup = BeautifulSoup(response.data, 'html.parser')
        self.assertNotEqual(None, soup.form)

    # def test_invite_team_form_exists(self):
    #     """"""
    #     teamID = 0
    #     response = self.app.get('/team/{}/'.format(teamID), content_type='html/text')
    #     soup = BeautifulSoup(response.data, 'html.parser')
    #     self.assertNotEqual(None, soup.form)

    # # this fails because there is no start date
    # def test_create_team_form_exists(self):
    #     """"""
    #     cb = 0
    #     response = self.app.get('/chorusbattle/{}/createteam/'.format(cb),
    #                             content_type='html/text')
    #     soup = BeautifulSoup(response.data, 'html.parser')
    #     self.assertNotEqual(None, soup.form)

    # def test_invite_team_member_form_exists(self):
    #     """"""
    #     teamID = 0
    #     response = self.app.get('/team/<teamID>/invite/'.format(teamID),
    #                             content_type='html/text')
    #     soup = BeautifulSoup(response.data, 'html.parser')
    #     self.assertNotEqual(None, soup.form)

    def test_create_chorus_battle_form_exists(self):
        """ Tests that the create chorus battle form exists. """
        response = self.app.get('/create/chorusbattle/', content_type='html/text')
        soup = BeautifulSoup(response.data, 'html.parser')
        self.assertNotEqual(None, soup.form)

    # def test_notification_form_exists(self):
    #     """"""
    #     cb = 0
    #     response = self.app.get('/chorusbattle/{}/judge/notify'.format(cb),
    #                             content_type='html/text')
    #     soup = BeautifulSoup(response.data, 'html.parser')
    #     self.assertNotEqual(None, soup.form)

    def test_create_round_form_exists(self):
        """ Checks that the create round form exists. """
        cb = 0
        response = self.app.get('/chorusbattle/{}/entries/createround/'.format(cb),
                                content_type='html/text')
        soup = BeautifulSoup(response.data, 'html.parser')
        self.assertNotEqual(None, soup.form)
