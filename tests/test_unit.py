"""
This module contains the unit tests that should be run to ensure that
our app works as intended.
"""

#note: comment out garbage in __init__ py to run pytest without other errors

# pylint: disable=C0103

import unittest
from unittest.mock import patch, DEFAULT, Mock
# from bs4 import BeautifulSoup
import cbapp
import os.path as op
import os

class TestCBAppUnit(unittest.TestCase):
    """Class of unit tests that checks if the templates exist."""
    
    def setUp(self):
        """
        Set up class for testing
        """
        cbapp.app.config['TESTING'] = True
        self.app = cbapp.app.test_client()
        self.dir = os.path.dirname(os.path.abspath(__file__))

    ##### check if the files located in the cbapp directory exist #####

    def test_check_init(self):
        """
        Checks if the __init__ file exists.
        """
        file_exists = op.exists(op.join(self.dir,
                                        '..',
                                        'cbapp',
                                        '__init__.py'))
        self.assertTrue(file_exists)

    def test_check_forms(self):
        """
        Checks if the forms file exists.
        """
        file_exists = op.exists(op.join(self.dir,
                                        '..',
                                        'cbapp',
                                        'forms.py'))
        self.assertTrue(file_exists)

    def test_check_manage(self):
        """
        Checks if the manage file exists.
        """
        file_exists = op.exists(op.join(self.dir,
                                        '..',
                                        'cbapp',
                                        'manage.py'))
        self.assertTrue(file_exists)

    def test_check_models(self):
        """
        Checks if the models file exists.
        """
        file_exists = op.exists(op.join(self.dir,
                                        '..',
                                        'cbapp',
                                        'models.py'))
        self.assertTrue(file_exists)

    def test_check_routes(self):
        """
        Checks if the routes file exists.
        """
        file_exists = op.exists(op.join(self.dir,
                                        '..',
                                        'cbapp',
                                        'routes.py'))
        self.assertTrue(file_exists)

    ##### check if the files located in the cbapp/templates directory exist #####

    def test_check_index(self):
        """
        Checks if the index file exists.
        """
        file_exists = op.exists(op.join(self.dir,
                                        '..',
                                        'cbapp',
                                        'templates',
                                        'index.html'))
        self.assertTrue(file_exists)

    def test_check_base(self):
        """
        Checks if the base file exists.
        """
        file_exists = op.exists(op.join(self.dir,
                                        '..',
                                        'cbapp',
                                        'templates',
                                        'base.html'))
        self.assertTrue(file_exists)   



    # def test_login_gets_login_template(self):
    #     """Checks if the login route exists. The test passes if it does."""
    #     with patch.multiple("cbapp.routes",
    #                         request=DEFAULT,
    #                         render_template=DEFAULT) as mock_functions:
    #         cbapp.routes.login()
    #         render_template = mock_functions["render_template"]

    #         # session['username'] = None

    #         #makes sure we are rendering a template on the login route
    #         self.assertTrue(render_template.called)
    #         call_args = render_template.call_args
    #         file_name = call_args[0][0]
    #         #makes sure we are rendering the correct template on the login route
    #         self.assertEqual(file_name, "login.html")

    # def test_index_get_index_template(self):
    #     """Checks if the index route exists. The test passes if it does."""
    #     # Create mock functions
    #     with patch.multiple('cbapp.routes',
    #                         request=DEFAULT,
    #                         render_template=DEFAULT) as mock_functions:
    #         cbapp.routes.index()
    #         # Check if render_template is called when index route is visited
    #         render_template = mock_functions['render_template']
    #         self.assertTrue(render_template.called)

    #         # Check if the template rendered is index.html
    #         call_args = render_template.call_args
    #         file_name = call_args[0][0]
    #         self.assertEqual(file_name, "index.html")

    # def test_signup_get_singup_template(self):
    #     """Checks if the signup route exists. The test passes if it does."""
    #     with patch.multiple("cbapp.routes",
    #                         request=DEFAULT,
    #                         render_template=DEFAULT) as mock_functions:
    #         cbapp.routes.signup()
    #         render_template = mock_functions["render_template"]
    #         self.assertTrue(render_template.called)
    #         call_args = render_template.call_args
    #         file_name = call_args[0][0]
    #         self.assertEqual(file_name, "signup.html")

    # def test_home_get_home_template(self):
    #     """Checks if the home route exists. The test passes if it does."""
    #     with patch.multiple("cbapp.routes",
    #                         request=DEFAULT,
    #                         render_template=DEFAULT) as mock_functions:
    #         cbapp.routes.home()
    #         render_template = mock_functions["render_template"]
    #         self.assertTrue(render_template.called)
    #         call_args = render_template.call_args
    #         file_name = call_args[0][0]
    #         self.assertEqual(file_name, "home.html")

    # def test_cbinfo_get_cbinfo_template(self):
    #     """Checks if the chorusinfo route exists. The test passes if it does."""
    #     with patch.multiple("cbapp.routes",
    #                         request=DEFAULT,
    #                         render_template=DEFAULT) as mock_functions:
    #         cbapp.routes.chorusInfo()
    #         render_template = mock_functions["render_template"]
    #         self.assertTrue(render_template.called)
    #         call_args = render_template.call_args
    #         file_name = call_args[0][0]
    #         self.assertEqual(file_name, "chorusinfo.html")

    # def test_cbinfo_get_entries_template(self):
    #     """Checks if the chorusinfo entries route exists. The test passes if it does."""
    #     with patch.multiple("cbapp.routes",
    #                         request=DEFAULT,
    #                         render_template=DEFAULT) as mock_functions:
    #         cbapp.routes.chorusEntries()
    #         render_template = mock_functions["render_template"]
    #         self.assertTrue(render_template.called)
    #         call_args = render_template.call_args
    #         file_name = call_args[0][0]
    #         self.assertEqual(file_name, "entries.html")

    # def test_team_get_team_template(self):
    #     """Checks if the team/<name> route exists. The test passes if it does."""
    #     with patch.multiple("cbapp.routes",
    #                         request=DEFAULT,
    #                         render_template=DEFAULT) as mock_functions:
    #         cbapp.routes.team()
    #         render_template = mock_functions["render_template"]
    #         self.assertTrue(render_template.called)
    #         call_args = render_template.call_args
    #         file_name = call_args[0][0]
    #         self.assertEqual(file_name, "team.html")

    # def test_chorusbattles_get_chorusbattles_template(self):
    #     """Checks if the chorusBattle route exists. The test passes if it does."""
    #     with patch.multiple("cbapp.routes",
    #                         request=DEFAULT,
    #                         render_template=DEFAULT) as mock_functions:
    #         cbapp.routes.chorusBattleAll()
    #         render_template = mock_functions["render_template"]
    #         self.assertTrue(render_template.called)
    #         call_args = render_template.call_args
    #         file_name = call_args[0][0]
    #         self.assertEqual(file_name, "chorusbattles.html")

    # # def test_tournament_get_tournament_template(self):
    # #     """Checks if the tournament route exists. The test passes if it does."""
    # #     with patch.multiple("cbapp.routes",
    # #                         request=DEFAULT,
    # #                         render_template=DEFAULT) as mock_functions:
    # #         cbapp.routes.chorusBattle()
    # #         render_template = mock_functions["render_template"]
    # #         self.assertTrue(render_template.called)
    # #         call_args = render_template.call_args
    # #         file_name = call_args[0][0]
    # #         self.assertEqual(file_name, "tournament.html")

    # def test_createcb_get_createcb_template(self):
    #     """Checks if the createcb route exists. The test passes if it does."""
    #     with patch.multiple("cbapp.routes",
    #                         request=DEFAULT,
    #                         render_template=DEFAULT) as mock_functions:
    #         cbapp.routes.createChorusBattle()
    #         render_template = mock_functions["render_template"]
    #         self.assertTrue(render_template.called)
    #         call_args = render_template.call_args
    #         file_name = call_args[0][0]
    #         self.assertEqual(file_name, "createchorusbattle.html")

    # def test_userprofile_get_userprofile_template(self):
    #     """Checks if the user profile route exists. The test passes if it does."""
    #     with patch.multiple("cbapp.routes",
    #                         request=DEFAULT,
    #                         render_template=DEFAULT) as mock_functions:
    #         cbapp.routes.getUserProfile()
    #         render_template = mock_functions["render_template"]
    #         self.assertTrue(render_template.called)
    #         call_args = render_template.call_args
    #         file_name = call_args[0][0]
    #         self.assertEqual(file_name, "userprofile.html")

    # def test_faq_get_faq_template(self):
    #     """Checks if the faq route exists. The test passes if it does."""
    #     with patch.multiple("cbapp.routes",
    #                         request=DEFAULT,
    #                         render_template=DEFAULT) as mock_functions:
    #         cbapp.routes.faq()
    #         render_template = mock_functions["render_template"]
    #         self.assertTrue(render_template.called)
    #         call_args = render_template.call_args
    #         file_name = call_args[0][0]
    #         self.assertEqual(file_name, "faq.html")
