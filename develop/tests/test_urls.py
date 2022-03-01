from django.test import SimpleTestCase
from django.urls import reverse, resolve

from develop.views import buyer_seller_option, sign_up


class TestUrls(SimpleTestCase):
    """
       This class test the respective urls lead to their corresponding views functions
       """

    def test_option_url_is_resolved(self):
        url = reverse('option')
        self.assertEquals(resolve(url).func, buyer_seller_option)  # Testing that the option page url does  lead to
        # option for buyer and seller function

    # def test_accounts_url_is_resolved(self):
    #     url = reverse('/sign_up')
    #     self.assertEquals(resolve(url).func, sign_up)  # Testing that the signup url  does  lead to signup function
    #     self.assertNotEquals(resolve(url).func, buyer_seller_option)  # Testing that the url signup does not lead to option function
