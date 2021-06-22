from django.forms import PasswordInput


class CustomPasswordInput(PasswordInput):
    """
    Provides a wrapper on password field to render a custom string,
    so that the user can feel a value exists
    """

    def __init__(self, attrs=None, render_value=False, render_string=None):
        super().__init__(attrs, render_value)
        self.render_string = render_string

    def get_context(self, name, value, attrs):
        if self.render_string:
            value = self.render_string
        return super().get_context(name, value, attrs)