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
        """ Set up class for testing. """
        cbapp.app.config['TESTING'] = True
        self.app = cbapp.app.test_client()
        self.dir = os.path.dirname(os.path.abspath(__file__))

    ##### check if the files located in the cbapp directory exist #####

    def test_check_init(self):
        """ Checks if the __init__ file exists. """
        file_exists = op.exists(op.join(self.dir,
                                        '..',
                                        'cbapp',
                                        '__init__.py'))
        self.assertTrue(file_exists)

    def test_check_forms(self):
        """ Checks if the forms file exists. """
        file_exists = op.exists(op.join(self.dir,
                                        '..',
                                        'cbapp',
                                        'forms.py'))
        self.assertTrue(file_exists)

    def test_check_manage(self):
        """ Checks if the manage file exists. """
        file_exists = op.exists(op.join(self.dir,
                                        '..',
                                        'cbapp',
                                        'manage.py'))
        self.assertTrue(file_exists)

    def test_check_models(self):
        """ Checks if the models file exists. """
        file_exists = op.exists(op.join(self.dir,
                                        '..',
                                        'cbapp',
                                        'models.py'))
        self.assertTrue(file_exists)

    def test_check_routes(self):
        """ Checks if the routes file exists. """
        file_exists = op.exists(op.join(self.dir,
                                        '..',
                                        'cbapp',
                                        'routes.py'))
        self.assertTrue(file_exists)

    ##### check if the files located in the cbapp/static directory exist #####

    def test_check_main_css(self):
        """ Checks if the main.css file exists. """
        file_exists = op.exists(op.join(self.dir,
                                        '..',
                                        'cbapp',
                                        'static',
                                        'css',
                                        'main.css'))
        self.assertTrue(file_exists)

    def test_check_script_js(self):
        """ Checks if the script.js file exists. """
        file_exists = op.exists(op.join(self.dir,
                                        '..',
                                        'cbapp',
                                        'static',
                                        'js',
                                        'script.js'))
        self.assertTrue(file_exists)

    def test_check_img_folder(self):
        """ Checks if the img folder/directory exists. """
        folder_exists = op.exists(op.join(self.dir,
                                          '..',
                                          'cbapp',
                                          'static',
                                          'img'))
        self.assertTrue(folder_exists)

    ##### check if the files located in the cbapp/templates directory exist #####

    def test_check_index(self):
        """ Checks if the index.html file exists. """
        file_exists = op.exists(op.join(self.dir,
                                        '..',
                                        'cbapp',
                                        'templates',
                                        'index.html'))
        self.assertTrue(file_exists)

    def test_check_base(self):
        """ Checks if the base.html file exists. """
        file_exists = op.exists(op.join(self.dir,
                                        '..',
                                        'cbapp',
                                        'templates',
                                        'base.html'))
        self.assertTrue(file_exists)

    def test_check_chorusbattles(self):
        """ Checks if the chorusbattles.html file exists. """
        file_exists = op.exists(op.join(self.dir,
                                        '..',
                                        'cbapp',
                                        'templates',
                                        'chorusbattles.html'))
        self.assertTrue(file_exists)

    def test_check_chorusheader(self):
        """ Checks if the chorusheader.html file exists. """
        file_exists = op.exists(op.join(self.dir,
                                        '..',
                                        'cbapp',
                                        'templates',
                                        'chorusheader.html'))
        self.assertTrue(file_exists)

    def test_check_chorusinfo(self):
        """ Checks if the chorusinfo.html file exists. """
        file_exists = op.exists(op.join(self.dir,
                                        '..',
                                        'cbapp',
                                        'templates',
                                        'chorusinfo.html'))
        self.assertTrue(file_exists)

    def test_check_createchorusbattle(self):
        """ Checks if the createchorusbattle.html file exists. """
        file_exists = op.exists(op.join(self.dir,
                                        '..',
                                        'cbapp',
                                        'templates',
                                        'createchorusbattle.html'))
        self.assertTrue(file_exists)

    def test_check_createentry(self):
        """ Checks if the createentry.html file exists. """
        file_exists = op.exists(op.join(self.dir,
                                        '..',
                                        'cbapp',
                                        'templates',
                                        'createentry.html'))
        self.assertTrue(file_exists)

    def test_check_createround(self):
        """ Checks if the createround.html file exists. """
        file_exists = op.exists(op.join(self.dir,
                                        '..',
                                        'cbapp',
                                        'templates',
                                        'createround.html'))
        self.assertTrue(file_exists)

    def test_check_createteam(self):
        """ Checks if the createteam.html file exists. """
        file_exists = op.exists(op.join(self.dir,
                                        '..',
                                        'cbapp',
                                        'templates',
                                        'createteam.html'))
        self.assertTrue(file_exists)

    def test_check_entries(self):
        """ Checks if the entries.html file exists. """
        file_exists = op.exists(op.join(self.dir,
                                        '..',
                                        'cbapp',
                                        'templates',
                                        'entries.html'))
        self.assertTrue(file_exists)

    def test_check_faq(self):
        """ Checks if the faq.html file exists. """
        file_exists = op.exists(op.join(self.dir,
                                        '..',
                                        'cbapp',
                                        'templates',
                                        'faq.html'))
        self.assertTrue(file_exists)

    def test_check_home(self):
        """ Checks if the home.html file exists. """
        file_exists = op.exists(op.join(self.dir,
                                        '..',
                                        'cbapp',
                                        'templates',
                                        'home.html'))
        self.assertTrue(file_exists)

    def test_check_judgingtool(self):
        """ Checks if the judgingtool.html file exists. """
        file_exists = op.exists(op.join(self.dir,
                                        '..',
                                        'cbapp',
                                        'templates',
                                        'judgingtool.html'))
        self.assertTrue(file_exists)

    def test_check_login(self):
        """ Checks if the login.html file exists. """
        file_exists = op.exists(op.join(self.dir,
                                        '..',
                                        'cbapp',
                                        'templates',
                                        'login.html'))
        self.assertTrue(file_exists)

    def test_check_signup(self):
        """ Checks if the signup.html file exists. """
        file_exists = op.exists(op.join(self.dir,
                                        '..',
                                        'cbapp',
                                        'templates',
                                        'signup.html'))
        self.assertTrue(file_exists)

    def test_check_team(self):
        """ Checks if the team.html file exists. """
        file_exists = op.exists(op.join(self.dir,
                                        '..',
                                        'cbapp',
                                        'templates',
                                        'team.html'))
        self.assertTrue(file_exists)

    def test_check_tournament(self):
        """ Checks if the tournament.html file exists. """
        file_exists = op.exists(op.join(self.dir,
                                        '..',
                                        'cbapp',
                                        'templates',
                                        'tournament.html'))
        self.assertTrue(file_exists)

    def test_check_userprofile(self):
        """ Checks if the userprofile.html file exists. """
        file_exists = op.exists(op.join(self.dir,
                                        '..',
                                        'cbapp',
                                        'templates',
                                        'userprofile.html'))
        self.assertTrue(file_exists)

    def test_index_page_loads(self):
        """ Checks if the index page loads correctly. """
        tester = cbapp.app.test_client(self)
        response = tester.get('/', content_type='html/text')
        self.assertTrue(b'Login' in response.data)


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
