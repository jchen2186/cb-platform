import unittest
import cbapp
from unittest.mock import patch, DEFAULT, mock

class TestCBAppUnit(unittest.TestCase):

	def test_login_gets_login_template(self):
		with patch.multiple("cbapp.routes",
							request=DEFAULT,
							render_template=DEFAULT) as mock_funcs:
			cbapps.routes.login()
			render_template = mock_funcs["render_template"]
			self.assertTrue(render_template.called)
			calls_args = render_template.call_args
			file_name = call_args[0][0]
			self.assertEqual(file_name, "login.html")