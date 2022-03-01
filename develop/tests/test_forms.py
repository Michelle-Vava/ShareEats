from django.contrib.auth.forms import UserCreationForm
from django.test import SimpleTestCase


class TestForms(SimpleTestCase):
    """
    The function validates the form with empty data is not submitted
    """

    def test_user_form_valid(self):
        form = UserCreationForm(data={})

        self.assertFalse(form.is_valid())
        self.assertEquals(len(form.errors), 3)  # django password validators are 3