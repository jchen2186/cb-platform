import unittest
import cbapp
from unittest.mock import patch, DEFAULT, Mock

class TestCBAppUnit(unittest.TestCase):

	# Test for getting the index template
	def test_index_get_index_template(self):
		# Create mock functions
		with patch.multiple('cbapp.routes',
							request=DEFAULT
							render_template=DEFAULT) as mock_functions:
		cbapp.routes.index()
		
		# Check if render_template is called when index route is visited
		render_template = mock_functions['render_template']
		self.assertTrue(render_template.called)

		# Check if the template rendered is index.html
		call_args = render_template.call_args
		template_filename = call_args[0][0]
		self.assertEqual(template_name, "index.html")

	def test_index_successful_render(self):
