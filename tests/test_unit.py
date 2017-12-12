"""
This module contains the unit tests that should be run to ensure that
our app works as intended.
"""

#note: comment out garbage in __init__ py to run pytest without other errors

# pylint: disable=C0103

import unittest
from unittest.mock import patch, DEFAULT, Mock
import cbapp
import os.path as op
import os
from flask_testing import TestCase
import flask # for test_request_context

class TestCBAppUnitFilesExist(unittest.TestCase):
    """Class of unit tests for the chorus battle app that checks if files exist."""
    
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

    def test_check_search(self):
        """ Checks if the search file exists. """
        file_exists = op.exists(op.join(self.dir,
                                        '..',
                                        'cbapp',
                                        'templates',
                                        'searchresult.html'))
        self.assertTrue(file_exists)

class TestCBAppUnitRoutesExist(unittest.TestCase):
    """Class of unit tests for the chorus battle app that checks if routes exist."""
    
    def setUp(self):
        """ Set up class for testing. """
        cbapp.app.config['TESTING'] = True
        self.app = cbapp.app.test_client()

    def test_index_get_index_template(self):
        """ Checks if the index route exists. """
        with cbapp.app.test_request_context('/', method='GET'):
            self.assertEqual(flask.request.path, '/')
            self.assertEqual(flask.request.method, 'GET')

            with patch.multiple('cbapp.routes',
                                request=DEFAULT,
                                render_template=DEFAULT,
                                redirect=DEFAULT,
                                url_for=DEFAULT) as mock_functions:
                cbapp.routes.index()
                # Check if render_template is called when index route is visited
                render_template = mock_functions['render_template']
                redirect = mock_functions['redirect']
                url_for = mock_functions['url_for']
                self.assertTrue(render_template.called)

            # Check if the template rendered is index.html
            call_args = render_template.call_args
            file_name = call_args[0][0]
            self.assertEqual(file_name, "index.html")

    def test_login_get_login_template(self):
        """Checks if the login route exists when the request method is GET.
        The user can't already be logged in."""
        with cbapp.app.test_request_context('/login/', method='GET'):
            self.assertEqual(flask.request.path, '/login/')
            self.assertEqual(flask.request.method, 'GET')

            with patch.multiple("cbapp.routes",
                                # request=DEFAULT,
                                render_template=DEFAULT,
                                # validate=DEFAULT,
                                redirect=DEFAULT,
                                url_for=DEFAULT,
                                flash=DEFAULT) as mock_functions:
                cbapp.routes.login()
                render_template = mock_functions["render_template"]
                # validate = mock_functions['validate']
                redirect = mock_functions['redirect']
                url_for = mock_functions['url_for']
                flash = mock_functions['flash']

                # makes sure we are rendering a template on the login route
                self.assertTrue(render_template.called)
                call_args = render_template.call_args
                file_name = call_args[0][0]
                # makes sure we are rendering the correct template on the login route
                self.assertEqual(file_name, "login.html")

    def test_login_post_login_template(self):
        """Checks if the login route exists when the request method is POST,
        but the form does not validate.
        The user can't already be logged in."""
        with cbapp.app.test_request_context('/login/', method='POST'):
            self.assertEqual(flask.request.path, '/login/')
            self.assertEqual(flask.request.method, 'POST')

            with patch.multiple("cbapp.routes",
                                # request=DEFAULT,
                                render_template=DEFAULT,
                                # validate=DEFAULT,
                                redirect=DEFAULT,
                                url_for=DEFAULT,
                                flash=DEFAULT) as mock_functions:
                cbapp.routes.login()
                render_template = mock_functions["render_template"]
                # validate = mock_functions['validate']
                redirect = mock_functions['redirect']
                url_for = mock_functions['url_for']
                flash = mock_functions['flash']

                # makes sure we are rendering a template on the login route
                self.assertTrue(render_template.called)
                call_args = render_template.call_args
                file_name = call_args[0][0]
                # makes sure we are rendering the correct template on the login route
                self.assertEqual(file_name, "login.html")

    def test_signup_get_signup_template(self):
        """Checks if the signup route exists when the request method is GET. The test passes if it does.
        The user can't already be logged in."""
        with cbapp.app.test_request_context('/signup/', method='GET'):
            self.assertEqual(flask.request.path, '/signup/')
            self.assertEqual(flask.request.method, 'GET')

            with patch.multiple("cbapp.routes",
                                # request=DEFAULT,
                                render_template=DEFAULT,
                                # validate=DEFAULT,
                                redirect=DEFAULT,
                                url_for=DEFAULT,
                                flash=DEFAULT) as mock_functions:
                cbapp.routes.signup()
                render_template = mock_functions["render_template"]
                # validate = mock_functions['validate']
                redirect = mock_functions['redirect']
                url_for = mock_functions['url_for']
                flash = mock_functions['flash']

                self.assertTrue(render_template.called)
                call_args = render_template.call_args
                file_name = call_args[0][0]
                self.assertEqual(file_name, "signup.html")

    def test_signup_post_signup_template(self):
        """Checks if the signup route exists when the request method is POST. The test passes if it does.
        The user can't already be logged in."""
        with cbapp.app.test_request_context('/signup/', method='POST'):
            self.assertEqual(flask.request.path, '/signup/')
            self.assertEqual(flask.request.method, 'POST')

            with patch.multiple("cbapp.routes",
                                # request=DEFAULT,
                                render_template=DEFAULT,
                                # validate=DEFAULT,
                                redirect=DEFAULT,
                                url_for=DEFAULT,
                                flash=DEFAULT) as mock_functions:
                cbapp.routes.signup()
                render_template = mock_functions["render_template"]
                # validate = mock_functions['validate']
                redirect = mock_functions['redirect']
                url_for = mock_functions['url_for']
                flash = mock_functions['flash']

                self.assertTrue(render_template.called)
                call_args = render_template.call_args
                file_name = call_args[0][0]
                self.assertEqual(file_name, "signup.html")
    
    def test_home_redirect_login_template(self):
        """Checks if the home route redirects the user to login when the user is not logged in.
        The test passes if it does."""
        with cbapp.app.test_request_context('/home/', method='GET'):
            self.assertEqual(flask.request.path, '/home/')
            self.assertEqual(flask.request.method, 'GET')

            with patch.multiple("cbapp.routes",
                                request=DEFAULT,
                                render_template=DEFAULT,
                                redirect=DEFAULT,
                                url_for=DEFAULT) as mock_functions:
                cbapp.routes.home()
                render_template = mock_functions["render_template"]
                redirect = mock_functions['redirect']
                url_for = mock_functions['url_for']

                self.assertTrue(redirect.called)
                self.assertTrue(url_for.called)

                call_args = url_for.call_args
                file_name = call_args[0][0]
                self.assertEqual(file_name, "login")

    def test_search_redirect_search_template(self):
        """Checks if the home route redirects the user to login when the user is not logged in.
        The test passes if it does."""
        with cbapp.app.test_request_context('/search/', method='POST'):
            self.assertEqual(flask.request.path, '/search/')
            self.assertEqual(flask.request.method, 'POST')

            with patch.multiple("cbapp.routes",
                                request=DEFAULT,
                                render_template=DEFAULT) as mock_functions:
                cbapp.routes.search()
                render_template = mock_functions["render_template"]

                call_args = render_template.call_args
                file_name = call_args[0][0]
                self.assertEqual(file_name, "searchresult.html")

    # # need to fix this so it generates home when a user is logged in
    # def test_home_get_home_template(self):
    #     """Checks if the home route exists. The test passes if it does."""
    #     with self.app.session_transaction() as sess:
    #         sess['username'] = 'testuser'

    #         with patch.multiple("cbapp.routes",
    #                             # request=DEFAULT,
    #                             render_template=DEFAULT) as mock_functions:
    #             cbapp.routes.home()
    #             render_template = mock_functions["render_template"]
    #             self.assertTrue(render_template.called)
    #             # call_args = render_template.call_args
    #             # file_name = call_args[0][0]
    #             # self.assertEqual(file_name, "home.html")

    # # does not work because it can't query the database for a row
    # def test_cbinfo_get_cbinfo_template(self):
    #     """Checks if the chorusinfo route exists. The test passes if it does."""
    #     cb = 0
    #     with cbapp.app.test_request_context('/chorusbattle/{}/'.format(cb), method='GET'):
    #         self.assertEqual(flask.request.path, '/chorusbattle/{}/'.format(cb))
    #         self.assertEqual(flask.request.method, 'GET')

    #         with patch.multiple("cbapp.routes",
    #                             render_template=DEFAULT,
    #                             query=DEFAULT,
    #                             filter_by=DEFAULT,
    #                             first=DEFAULT,
    #                             all=DEFAULT,
    #                             print=DEFAULT,
    #                             len=DEFAULT,
    #                             range=DEFAULT,
    #                             append=DEFAULT,
    #                             b64encode=DEFAULT,
    #                             is_subscribed=DEFAULT,
    #                             getUserIcon=DEFAULT) as mock_functions:
    #             cbapp.routes.chorusInfo(0)
    #             render_template = mock_functions["render_template"]
    #             query = mock_functions['query']
    #             filter_by = mock_functions['filter_by']
    #             first = mock_functions['first']
    #             all = mock_functions['all']
    #             print = mock_functions['print']
    #             len = mock_functions['len']
    #             range = mock_functions['range']
    #             append = mock_functions['append']
    #             b64encode = mock_functions['b64encode']
    #             is_subscribed = mock_functions['is_subscribed']
    #             getUserIcon = mock_functions['getUserIcon']

    #             self.assertTrue(render_template.called)
    #             call_args = render_template.call_args
    #             file_name = call_args[0][0]
    #             self.assertEqual(file_name, "chorusinfo.html")

    # def test_cbinfo_get_entries_template(self):
    #     """Checks if the chorusinfo entries route exists. The test passes if it does."""
    #     with cbapp.app.test_request_context('/home/', method='GET'):
    #         self.assertEqual(flask.request.path, '/home/')
    #         self.assertEqual(flask.request.method, 'GET')

    #         with patch.multiple("cbapp.routes",
    #                             request=DEFAULT,
    #                             render_template=DEFAULT) as mock_functions:
    #             cbapp.routes.chorusEntries()
    #             render_template = mock_functions["render_template"]
    #             self.assertTrue(render_template.called)
    #             call_args = render_template.call_args
    #             file_name = call_args[0][0]
    #             self.assertEqual(file_name, "entries.html")

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


class TestCBAppUnitModels(unittest.TestCase):
    """Class of unit tests for the chorus battle app that checks models work."""
    
    def setUp(self):
        """ Set up class for testing. """
        cbapp.app.config['TESTING'] = True
        self.app = cbapp.app.test_client()


