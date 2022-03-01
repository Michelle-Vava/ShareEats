from django.test import TestCase
from develop.models import BuyerInfo, User

"""
Run the command : python manage.py test
"""


# Implementing Unit Testing
# Create your tests_models.py here.
# unit testing for our models
class TestModels(TestCase):
    def setUp(self):
        self.user = User.objects.create(username='alex', password='2421djfes')
        self.buyer_profile = BuyerInfo.objects.create(firstname='alex', lastname='peters', phone='9023188172',
                                                      user=self.user)

    def test_buyer_creation(self):
        buyer = self.buyer_profile
        self.assertTrue(isinstance(buyer, BuyerInfo))
        # testing to see if the firstname is a string
        self.assertIsInstance(self.buyer_profile.firstname, str)

    def test_uer(self):
        username = 'jane'
        password = 'hello'
        u = User(username=username)
        u.set_password(password)
        u.save()
        self.assertEqual(u.username,username)
        self.assertTrue(u.check_password(password))

    # TODO: add more tests : for dishes and also seller
