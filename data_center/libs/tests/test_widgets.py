from django.test import SimpleTestCase, tag

from libs.widgets import CustomPasswordInput


@tag('CustomPasswordInput')
class TestCustomPasswordInput(SimpleTestCase):
    """TestCases for api url service class"""

    def test_get_context__empty_render_string(self):
        result = {
            'widget': {
                'attrs': {
                    'extra': 's'
                 },
                'is_hidden': False,
                'name': 'test',
                'required': False,
                'template_name': 'django/forms/widgets/password.html',
                'type': 'password',
                'value': 's'
            }
        }

        self.assertEqual(CustomPasswordInput(render_value=True).get_context('test', value='s', attrs={'extra': 's'}), result)

    def test_get_context_with_render_string(self):
        result = {
            'widget': {
                'attrs': {
                    'extra': 's'
                 },
                'is_hidden': False,
                'name': 'test',
                'required': False,
                'template_name': 'django/forms/widgets/password.html',
                'type': 'password',
                'value': 'render_str'
            }
        }

        self.assertEqual(CustomPasswordInput(render_string='render_str', render_value=True).
                         get_context('test', value='a', attrs={'extra': 's'}), result)