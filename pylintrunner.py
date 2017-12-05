"""
Run this file to get the average pylint scores of all of the relevant Python files in this repo.
"""

from pylint.lint import Run

files = ['application.py',
         'cbapp/__init__.py',
         'cbapp/forms.py',
         # 'cbapp/manage.py',
         # 'cbapp/models.py',
         'cbapp/routes.py',
         'tests/test_unit.py',
         'tests/test_integration.py',
         'tests/test_acceptance.py']

results = Run(files, exit=False)
