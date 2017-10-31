import unittest
import cbapp
from unittest.mock import patch, DEFAULT, Mock

class TestCBAppUnit(unittest.TestCase):

	def test_index_get_index_template(self):
		with patch.multiple('cbapp.routes',
							request=DEFAULT
							render_template=DEFAULT) as mock_funcs:
		cbapp.routes.index()
		render_template = mock_func['render_template']
		self.assertTrue(render_template.called)
		call_args = render_template.call_args
		template_filename = call_args[0][0]
		self.assertEqual(template_name, "index.html")
