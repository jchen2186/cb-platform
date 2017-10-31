#note: comment out garbage in __init__ py to run pytest without other errors

import unittest
import cbapp

from unittest.mock import patch, DEFAULT, Mock

class TestCBAppUnit(unittest.TestCase):

	#checks login route
	def test_login_gets_login_template(self):
		with patch.multiple("cbapp.routes",
							request=DEFAULT,
							render_template=DEFAULT) as mock_funcs:
			cbapp.routes.login()
			render_template = mock_funcs["render_template"]
			#makes sure we are rendering a template on the login route
			self.assertTrue(render_template.called)
			call_args = render_template.call_args
			file_name = call_args[0][0]
			#makes sure we are rendering the correct template on the login route
			self.assertEqual(file_name, "login.html")

	# Test for getting the index template
	def test_index_get_index_template(self):
		# Create mock functions
		with patch.multiple('cbapp.routes',
							request=DEFAULT,
							render_template=DEFAULT) as mock_functions:
			cbapp.routes.index()
			
			# Check if render_template is called when index route is visited
			render_template = mock_functions['render_template']
			self.assertTrue(render_template.called)

			# Check if the template rendered is index.html
			call_args = render_template.call_args
			template_filename = call_args[0][0]
			self.assertEqual(template_name, "index.html")